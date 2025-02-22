package service

import (
	"fmt"
	"lang-portal/internal/models"
	"time"
)

type StudySessionsService struct {
	db *models.DB
}

func NewStudySessionsService(db *models.DB) *StudySessionsService {
	return &StudySessionsService{db: db}
}

func (s *StudySessionsService) GetStudySessions(page int) ([]models.StudySessionResponse, *models.Pagination, error) {
	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	countQuery := `SELECT COUNT(*) FROM study_sessions`
	if err := s.db.QueryRow(countQuery).Scan(&totalItems); err != nil {
		return nil, nil, err
	}

	// Get study sessions
	query := `
		SELECT 
			ss.id,
			sa.name as activity_name,
			g.name as group_name,
			strftime('%Y-%m-%d %H:%M:%S', ss.created_at) as start_time,
			strftime('%Y-%m-%d %H:%M:%S', datetime(ss.created_at, '+10 minutes')) as end_time,
			(SELECT COUNT(*) FROM word_review_items WHERE study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []models.StudySessionResponse
	for rows.Next() {
		var session models.StudySessionResponse
		var startTimeStr, endTimeStr string

		if err := rows.Scan(
			&session.ID,
			&session.ActivityName,
			&session.GroupName,
			&startTimeStr,
			&endTimeStr,
			&session.ReviewItemsCount,
		); err != nil {
			return nil, nil, err
		}

		// Parse the time strings
		startTime, err := time.Parse("2006-01-02 15:04:05", startTimeStr)
		if err != nil {
			return nil, nil, fmt.Errorf("failed to parse start time: %v", err)
		}
		session.StartTime = startTime

		endTime, err := time.Parse("2006-01-02 15:04:05", endTimeStr)
		if err != nil {
			return nil, nil, fmt.Errorf("failed to parse end time: %v", err)
		}
		session.EndTime = endTime

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

func (s *StudySessionsService) GetStudySession(id int) (*models.StudySessionResponse, error) {
	query := `
		SELECT 
			ss.id,
			sa.name as activity_name,
			g.name as group_name,
			strftime('%Y-%m-%d %H:%M:%S', ss.created_at) as start_time,
			strftime('%Y-%m-%d %H:%M:%S', datetime(ss.created_at, '+10 minutes')) as end_time,
			(SELECT COUNT(*) FROM word_review_items WHERE study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.id = ?
	`

	var session models.StudySessionResponse
	var startTimeStr, endTimeStr string

	err := s.db.QueryRow(query, id).Scan(
		&session.ID,
		&session.ActivityName,
		&session.GroupName,
		&startTimeStr,
		&endTimeStr,
		&session.ReviewItemsCount,
	)
	if err != nil {
		return nil, err
	}

	// Parse the time strings
	startTime, err := time.Parse("2006-01-02 15:04:05", startTimeStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse start time: %v", err)
	}
	session.StartTime = startTime

	endTime, err := time.Parse("2006-01-02 15:04:05", endTimeStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse end time: %v", err)
	}
	session.EndTime = endTime

	return &session, nil
}

func (s *StudySessionsService) GetStudySessionWords(sessionID, page int) ([]models.WordWithStats, *models.Pagination, error) {
	itemsPerPage := 100
	offset := (page - 1) * itemsPerPage

	// Get total count
	var totalItems int
	countQuery := `
		SELECT COUNT(DISTINCT wri.word_id)
		FROM word_review_items wri
		WHERE wri.study_session_id = ?
	`
	if err := s.db.QueryRow(countQuery, sessionID).Scan(&totalItems); err != nil {
		return nil, nil, err
	}

	// Get words with stats
	query := `
		SELECT 
			w.japanese,
			w.romaji,
			w.english,
			(SELECT COUNT(*) FROM word_review_items wri2 
				WHERE wri2.word_id = w.id 
				AND wri2.study_session_id = ? 
				AND wri2.correct = 1) as correct_count,
			(SELECT COUNT(*) FROM word_review_items wri2 
				WHERE wri2.word_id = w.id 
				AND wri2.study_session_id = ? 
				AND wri2.correct = 0) as wrong_count
		FROM word_review_items wri
		JOIN words w ON wri.word_id = w.id
		WHERE wri.study_session_id = ?
		GROUP BY w.id
		ORDER BY w.japanese
		LIMIT ? OFFSET ?
	`

	rows, err := s.db.Query(query, sessionID, sessionID, sessionID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var words []models.WordWithStats
	for rows.Next() {
		var word models.WordWithStats
		if err := rows.Scan(
			&word.Japanese,
			&word.Romaji,
			&word.English,
			&word.CorrectCount,
			&word.WrongCount,
		); err != nil {
			return nil, nil, err
		}
		words = append(words, word)
	}

	pagination := &models.Pagination{
		CurrentPage:  page,
		TotalPages:  (totalItems + itemsPerPage - 1) / itemsPerPage,
		TotalItems:  totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return words, pagination, nil
}

func (s *StudySessionsService) ReviewWord(sessionID, wordID int, correct bool) error {
	// Verify session exists
	var sessionExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM study_sessions WHERE id = ?)", sessionID).Scan(&sessionExists); err != nil {
		return err
	}
	if !sessionExists {
		return fmt.Errorf("study session with ID %d does not exist", sessionID)
	}

	// Verify word exists
	var wordExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM words WHERE id = ?)", wordID).Scan(&wordExists); err != nil {
		return err
	}
	if !wordExists {
		return fmt.Errorf("word with ID %d does not exist", wordID)
	}

	// Insert review
	query := `
		INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
		VALUES (?, ?, ?, CURRENT_TIMESTAMP)
	`

	if _, err := s.db.Exec(query, wordID, sessionID, correct); err != nil {
		return err
	}

	return nil
}

func (s *StudySessionsService) ResetHistory() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Delete all word review items
	if _, err := tx.Exec("DELETE FROM word_review_items"); err != nil {
		return err
	}

	// Delete all study sessions
	if _, err := tx.Exec("DELETE FROM study_sessions"); err != nil {
		return err
	}

	if err := tx.Commit(); err != nil {
		return err
	}

	return nil
}

func (s *StudySessionsService) FullReset() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Delete all data
	tables := []string{
		"word_review_items",
		"study_sessions",
		"words_groups",
		"words",
		"groups",
		"study_activities",
	}

	for _, table := range tables {
		if _, err := tx.Exec(fmt.Sprintf("DELETE FROM %s", table)); err != nil {
			return err
		}
	}

	// Insert test data
	// Insert words with specific IDs
	wordQuery := `
		INSERT INTO words (id, japanese, romaji, english) VALUES
		(1, '犬', 'inu', 'dog'),
		(2, '猫', 'neko', 'cat'),
		(3, '鳥', 'tori', 'bird')
	`
	if _, err := tx.Exec(wordQuery); err != nil {
		return err
	}

	// Insert groups with specific IDs
	groupQuery := `
		INSERT INTO groups (id, name) VALUES
		(1, 'Animals'),
		(2, 'Basic Words')
	`
	if _, err := tx.Exec(groupQuery); err != nil {
		return err
	}

	// Insert study activities with specific IDs
	studyActivitiesQuery := `
		INSERT INTO study_activities (id, name, thumbnail_url, description) VALUES
		(1, 'Flashcards', 'https://example.com/flashcards.png', 'Practice with flashcards'),
		(2, 'Multiple Choice', 'https://example.com/quiz.png', 'Test your knowledge with multiple choice questions')
	`
	if _, err := tx.Exec(studyActivitiesQuery); err != nil {
		return err
	}

	// Insert words_groups with specific IDs
	wordsGroupsQuery := `
		INSERT INTO words_groups (word_id, group_id) VALUES
		(1, 1),
		(2, 1),
		(3, 1)
	`
	if _, err := tx.Exec(wordsGroupsQuery); err != nil {
		return err
	}

	if err := tx.Commit(); err != nil {
		return err
	}

	return nil
}
