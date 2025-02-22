package service

import (
	"fmt"
	"lang-portal/internal/models"
	"time"
)

type StudyActivitiesService struct {
	db *models.DB
}

func NewStudyActivitiesService(db *models.DB) *StudyActivitiesService {
	return &StudyActivitiesService{db: db}
}

func (s *StudyActivitiesService) GetStudyActivity(id int) (*models.StudyActivity, error) {
	query := `
		SELECT id, name, thumbnail_url, description
		FROM study_activities
		WHERE id = ?
	`

	var activity models.StudyActivity
	err := s.db.QueryRow(query, id).Scan(
		&activity.ID,
		&activity.Name,
		&activity.ThumbnailURL,
		&activity.Description,
	)
	if err != nil {
		return nil, err
	}
	return &activity, nil
}

func (s *StudyActivitiesService) GetStudyActivitySessions(activityID, page int) ([]models.StudyActivitySessionResponse, *models.Pagination, error) {
	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	countQuery := `
		SELECT COUNT(*)
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.study_activity_id = ?
	`
	if err := s.db.QueryRow(countQuery, activityID).Scan(&totalItems); err != nil {
		return nil, nil, err
	}

	// Get sessions
	query := `
		SELECT 
			ss.id,
			ss.group_id,
			strftime('%Y-%m-%d %H:%M:%S', ss.created_at) as created_at,
			ss.study_activity_id
		FROM study_sessions ss
		WHERE ss.study_activity_id = ?
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, activityID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []models.StudyActivitySessionResponse
	for rows.Next() {
		var session models.StudyActivitySessionResponse
		var createdAtStr string

		if err := rows.Scan(
			&session.ID,
			&session.GroupID,
			&createdAtStr,
			&session.StudyActivityID,
		); err != nil {
			return nil, nil, err
		}

		// Parse the time string
		createdAt, err := time.Parse("2006-01-02 15:04:05", createdAtStr)
		if err != nil {
			return nil, nil, fmt.Errorf("failed to parse created_at time: %v", err)
		}
		session.CreatedAt = createdAt

		sessions = append(sessions, session)
	}

	pagination := &models.Pagination{
		CurrentPage:  page,
		TotalPages:  (totalItems + itemsPerPage - 1) / itemsPerPage,
		TotalItems:  totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return sessions, pagination, nil
}

func (s *StudyActivitiesService) CreateStudySession(groupID, activityID int) (*models.StudySession, error) {
	// Verify group and activity exist
	if err := s.verifyGroupAndActivity(groupID, activityID); err != nil {
		return nil, err
	}

	query := `
		INSERT INTO study_sessions (group_id, study_activity_id, created_at)
		VALUES (?, ?, CURRENT_TIMESTAMP)
		RETURNING id, group_id, created_at, study_activity_id
	`

	var session models.StudySession
	err := s.db.QueryRow(query, groupID, activityID).Scan(
		&session.ID,
		&session.GroupID,
		&session.CreatedAt,
		&session.StudyActivityID,
	)
	if err != nil {
		return nil, err
	}

	return &session, nil
}

func (s *StudyActivitiesService) verifyGroupAndActivity(groupID, activityID int) error {
	// Check if group exists
	var groupExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)", groupID).Scan(&groupExists); err != nil {
		return err
	}
	if !groupExists {
		return fmt.Errorf("group with ID %d does not exist", groupID)
	}

	// Check if activity exists
	var activityExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM study_activities WHERE id = ?)", activityID).Scan(&activityExists); err != nil {
		return err
	}
	if !activityExists {
		return fmt.Errorf("study activity with ID %d does not exist", activityID)
	}

	return nil
}
