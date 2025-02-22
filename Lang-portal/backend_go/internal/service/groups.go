package service

import (
	"database/sql"
	"lang-portal/internal/models"
)

type GroupsService struct {
	db *models.DB
}

func NewGroupsService(db *models.DB) *GroupsService {
	return &GroupsService{db: db}
}

func (s *GroupsService) GetGroups(page int) (*models.GroupsResponse, error) {
	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	if err := s.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&totalItems); err != nil {
		return nil, err
	}

	// Get groups with word count
	query := `
		SELECT 
			g.id,
			g.name,
			(SELECT COUNT(*) FROM words_groups WHERE group_id = g.id) as total_word_count
		FROM groups g
		ORDER BY g.name
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, itemsPerPage, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	groups := make([]models.GroupWithStats, 0)
	for rows.Next() {
		var group models.GroupWithStats
		if err := rows.Scan(&group.ID, &group.Name, &group.Stats.TotalWordCount); err != nil {
			return nil, err
		}
		groups = append(groups, group)
	}

	response := &models.GroupsResponse{
		Items: groups,
		Pagination: &models.Pagination{
			CurrentPage:  page,
			TotalPages:   (totalItems + itemsPerPage - 1) / itemsPerPage,
			TotalItems:   totalItems,
			ItemsPerPage: itemsPerPage,
		},
	}

	// Ensure items is never nil
	if response.Items == nil {
		response.Items = make([]models.GroupWithStats, 0)
	}

	return response, nil
}

func (s *GroupsService) GetGroup(id int) (*models.GroupWithStats, error) {
	// First check if group exists
	var exists bool
	checkQuery := `SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)`
	if err := s.db.QueryRow(checkQuery, id).Scan(&exists); err != nil {
		return nil, err
	}
	if !exists {
		return nil, sql.ErrNoRows
	}

	query := `
		SELECT 
			g.id,
			g.name,
			(SELECT COUNT(*) FROM words_groups WHERE group_id = g.id) as total_word_count
		FROM groups g
		WHERE g.id = ?
	`

	var group models.GroupWithStats
	if err := s.db.QueryRow(query, id).Scan(
		&group.ID,
		&group.Name,
		&group.Stats.TotalWordCount,
	); err != nil {
		return nil, err
	}

	return &group, nil
}

func (s *GroupsService) GetGroupWords(groupID, page int) (*models.WordsResponse, error) {
	// First check if group exists
	var exists bool
	checkQuery := `SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)`
	if err := s.db.QueryRow(checkQuery, groupID).Scan(&exists); err != nil {
		return nil, err
	}
	if !exists {
		return nil, sql.ErrNoRows
	}

	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	countQuery := `
		SELECT COUNT(*)
		FROM words_groups wg
		JOIN words w ON wg.word_id = w.id
		WHERE wg.group_id = ?
	`
	if err := s.db.QueryRow(countQuery, groupID).Scan(&totalItems); err != nil {
		return nil, err
	}

	// Get words with stats
	query := `
		SELECT 
			w.japanese,
			w.romaji,
			w.english,
			(SELECT COUNT(*) FROM word_review_items wri 
				WHERE wri.word_id = w.id AND wri.correct = 1) as correct_count,
			(SELECT COUNT(*) FROM word_review_items wri 
				WHERE wri.word_id = w.id AND wri.correct = 0) as wrong_count
		FROM words_groups wg
		JOIN words w ON wg.word_id = w.id
		WHERE wg.group_id = ?
		ORDER BY w.japanese
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, groupID, itemsPerPage, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	words := make([]models.WordWithStats, 0)
	for rows.Next() {
		var word models.WordWithStats
		if err := rows.Scan(
			&word.Japanese,
			&word.Romaji,
			&word.English,
			&word.CorrectCount,
			&word.WrongCount,
		); err != nil {
			return nil, err
		}
		words = append(words, word)
	}

	response := &models.WordsResponse{
		Items: words,
		Pagination: &models.Pagination{
			CurrentPage:  page,
			TotalPages:   (totalItems + itemsPerPage - 1) / itemsPerPage,
			TotalItems:   totalItems,
			ItemsPerPage: itemsPerPage,
		},
	}

	// Ensure items is never nil
	if response.Items == nil {
		response.Items = make([]models.WordWithStats, 0)
	}

	return response, nil
}

func (s *GroupsService) GetGroupStudySessions(groupID, page int) ([]models.StudySessionResponse, *models.Pagination, error) {
	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	countQuery := `
		SELECT COUNT(*)
		FROM study_sessions ss
		WHERE ss.group_id = ?
	`
	if err := s.db.QueryRow(countQuery, groupID).Scan(&totalItems); err != nil {
		return nil, nil, err
	}

	// Get study sessions
	query := `
		SELECT 
			ss.id,
			sa.name as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			DATETIME(ss.created_at, '+10 minutes') as end_time,
			(SELECT COUNT(*) FROM word_review_items WHERE study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.group_id = ?
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, groupID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []models.StudySessionResponse
	for rows.Next() {
		var session models.StudySessionResponse
		if err := rows.Scan(
			&session.ID,
			&session.ActivityName,
			&session.GroupName,
			&session.StartTime,
			&session.EndTime,
			&session.ReviewItemsCount,
		); err != nil {
			return nil, nil, err
		}
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
