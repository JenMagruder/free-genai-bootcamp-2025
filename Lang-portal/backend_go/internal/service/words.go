package service

import (
	"database/sql"
	"lang-portal/internal/models"
)

type WordService struct {
	db *models.DB
}

func NewWordService(db *models.DB) *WordService {
	return &WordService{db: db}
}

type WordWithStats struct {
	Japanese     string `json:"japanese"`
	Romaji       string `json:"romaji"`
	English      string `json:"english"`
	CorrectCount int    `json:"correct_count"`
	WrongCount   int    `json:"wrong_count"`
}

type WordDetails struct {
	Japanese string      `json:"japanese"`
	Romaji   string      `json:"romaji"`
	English  string      `json:"english"`
	Stats    WordStats   `json:"stats"`
	Groups   []GroupInfo `json:"groups"`
}

type WordStats struct {
	CorrectCount int `json:"correct_count"`
	WrongCount   int `json:"wrong_count"`
}

type GroupInfo struct {
	ID             int `json:"id"`
	Name           string `json:"name"`
	TotalWordCount int    `json:"total_word_count"`
}

func (s *WordService) GetWords(page int) (*models.WordsResponse, error) {
	const itemsPerPage = 100
	offset := (page - 1) * itemsPerPage

	query := `
		SELECT 
			w.japanese,
			w.romaji,
			w.english,
			COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
			COUNT(CASE WHEN NOT wri.correct THEN 1 END) as wrong_count
		FROM words w
		LEFT JOIN word_review_items wri ON w.id = wri.word_id
		GROUP BY w.id, w.japanese, w.romaji, w.english
		ORDER BY w.id
		LIMIT ? OFFSET ?
	`

	countQuery := `SELECT COUNT(*) FROM words`

	rows, err := s.db.Query(query, itemsPerPage, offset)
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

	var totalItems int
	if err := s.db.QueryRow(countQuery).Scan(&totalItems); err != nil {
		return nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage

	response := &models.WordsResponse{
		Items: words,
		Pagination: &models.Pagination{
			CurrentPage:  page,
			TotalPages:   totalPages,
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

func (s *WordService) GetWordByID(id int) (*models.WordDetailResponse, error) {
	wordQuery := `
		SELECT 
			w.japanese,
			w.romaji,
			w.english
		FROM words w
		WHERE w.id = ?
	`

	statsQuery := `
		SELECT
			COUNT(CASE WHEN correct THEN 1 END) as correct_count,
			COUNT(CASE WHEN NOT correct THEN 1 END) as wrong_count
		FROM word_review_items
		WHERE word_id = ?
	`

	groupsQuery := `
		SELECT 
			g.id,
			g.name,
			(SELECT COUNT(*) FROM words_groups WHERE group_id = g.id) as total_word_count
		FROM groups g
		JOIN words_groups wg ON g.id = wg.group_id
		WHERE wg.word_id = ?
	`

	// First check if word exists
	var exists bool
	checkQuery := `SELECT EXISTS(SELECT 1 FROM words WHERE id = ?)`
	if err := s.db.QueryRow(checkQuery, id).Scan(&exists); err != nil {
		return nil, err
	}
	if !exists {
		return nil, sql.ErrNoRows
	}

	var word models.WordDetailResponse
	word.Groups = make([]models.GroupWithStats, 0)

	if err := s.db.QueryRow(wordQuery, id).Scan(
		&word.Japanese,
		&word.Romaji,
		&word.English,
	); err != nil {
		return nil, err
	}

	if err := s.db.QueryRow(statsQuery, id).Scan(
		&word.Stats.CorrectCount,
		&word.Stats.WrongCount,
	); err != nil {
		return nil, err
	}

	rows, err := s.db.Query(groupsQuery, id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var group models.GroupWithStats
		if err := rows.Scan(
			&group.ID,
			&group.Name,
			&group.Stats.TotalWordCount,
		); err != nil {
			return nil, err
		}
		word.Groups = append(word.Groups, group)
	}

	return &word, nil
}
