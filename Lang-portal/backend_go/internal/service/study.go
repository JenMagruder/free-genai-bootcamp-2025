package service

import (
	"time"

	"lang-portal/internal/models"
)

type StudyService struct {
	db *models.DB
}

func NewStudyService(db *models.DB) *StudyService {
	return &StudyService{db: db}
}

type StudyActivity struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	ThumbnailURL string `json:"thumbnail_url"`
	Description  string `json:"description"`
}

type StudySession struct {
	ID              int       `json:"id"`
	ActivityName    string    `json:"activity_name"`
	GroupName       string    `json:"group_name"`
	StartTime       time.Time `json:"start_time"`
	EndTime         time.Time `json:"end_time"`
	ReviewItemCount int       `json:"review_items_count"`
}

type PaginatedResponse struct {
	Items         interface{} `json:"items"`
	CurrentPage   int        `json:"current_page"`
	TotalPages    int        `json:"total_pages"`
	TotalItems    int        `json:"total_items"`
	ItemsPerPage  int        `json:"items_per_page"`
}

func (s *StudyService) GetActivity(id int) (*StudyActivity, error) {
	query := `
		SELECT id, name, thumbnail_url, description
		FROM study_activities
		WHERE id = ?
	`
	
	var activity StudyActivity
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

func (s *StudyService) GetActivitySessions(activityID, page int) (*PaginatedResponse, error) {
	const itemsPerPage = 100
	offset := (page - 1) * itemsPerPage

	query := `
		SELECT 
			ss.id,
			sa.name as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			MAX(wri.created_at) as end_time,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE sa.id = ?
		GROUP BY ss.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	countQuery := `
		SELECT COUNT(DISTINCT ss.id)
		FROM study_sessions ss
		WHERE ss.study_activity_id = ?
	`

	rows, err := s.db.Query(query, activityID, itemsPerPage, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sessions []StudySession
	for rows.Next() {
		var session StudySession
		if err := rows.Scan(
			&session.ID,
			&session.ActivityName,
			&session.GroupName,
			&session.StartTime,
			&session.EndTime,
			&session.ReviewItemCount,
		); err != nil {
			return nil, err
		}
		sessions = append(sessions, session)
	}

	var totalItems int
	if err := s.db.QueryRow(countQuery, activityID).Scan(&totalItems); err != nil {
		return nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage

	return &PaginatedResponse{
		Items:        sessions,
		CurrentPage:  page,
		TotalPages:   totalPages,
		TotalItems:   totalItems,
		ItemsPerPage: itemsPerPage,
	}, nil
}

func (s *StudyService) CreateStudySession(groupID, activityID int) (*models.StudySession, error) {
	query := `
		INSERT INTO study_sessions (group_id, study_activity_id, created_at)
		VALUES (?, ?, CURRENT_TIMESTAMP)
		RETURNING id, group_id, study_activity_id, created_at
	`
	
	var session models.StudySession
	err := s.db.QueryRow(query, groupID, activityID).Scan(
		&session.ID,
		&session.GroupID,
		&session.StudyActivityID,
		&session.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &session, nil
}
