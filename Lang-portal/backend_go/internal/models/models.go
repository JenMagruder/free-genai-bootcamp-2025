package models

import (
	"database/sql"
	"time"
)

// Base Models
type Word struct {
	ID       int    `json:"id"`
	Japanese string `json:"japanese"`
	Romaji   string `json:"romaji"`
	English  string `json:"english"`
}

type Group struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type StudySession struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
}

type StudyActivity struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	ThumbnailURL string `json:"thumbnail_url"`
	Description  string `json:"description"`
}

type WordReviewItem struct {
	WordID         int       `json:"word_id"`
	StudySessionID int       `json:"study_session_id"`
	Correct        bool      `json:"correct"`
	CreatedAt      time.Time `json:"created_at"`
}

// Response Types
type Pagination struct {
	CurrentPage   int `json:"current_page"`
	TotalPages    int `json:"total_pages"`
	TotalItems    int `json:"total_items"`
	ItemsPerPage  int `json:"items_per_page"`
}

type WordWithStats struct {
	Japanese     string `json:"japanese"`
	Romaji       string `json:"romaji"`
	English      string `json:"english"`
	CorrectCount int    `json:"correct_count"`
	WrongCount   int    `json:"wrong_count"`
}

type WordDetailResponse struct {
	Japanese string `json:"japanese"`
	Romaji   string `json:"romaji"`
	English  string `json:"english"`
	Stats    struct {
		CorrectCount int `json:"correct_count"`
		WrongCount   int `json:"wrong_count"`
	} `json:"stats"`
	Groups []GroupWithStats `json:"groups"`
}

type GroupWithStats struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	WordCount int    `json:"word_count,omitempty"`
	Stats     struct {
		TotalWordCount int `json:"total_word_count,omitempty"`
	} `json:"stats,omitempty"`
}

type StudySessionResponse struct {
	ID               int       `json:"id"`
	ActivityName     string    `json:"activity_name"`
	GroupName        string    `json:"group_name"`
	StartTime        time.Time `json:"start_time"`
	EndTime          time.Time `json:"end_time"`
	ReviewItemsCount int       `json:"review_items_count"`
}

type StudyActivitySessionResponse struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
}

type LastStudySessionResponse struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
	GroupName       string    `json:"group_name"`
}

type StudyProgressResponse struct {
	TotalWordsStudied    int `json:"total_words_studied"`
	TotalAvailableWords int `json:"total_available_words"`
}

type QuickStatsResponse struct {
	SuccessRate       float64 `json:"success_rate"`
	TotalStudySessions int    `json:"total_study_sessions"`
	TotalActiveGroups  int    `json:"total_active_groups"`
	StudyStreakDays    int    `json:"study_streak_days"`
}

type WordsResponse struct {
	Items      []WordWithStats `json:"items"`
	Pagination *Pagination    `json:"pagination"`
}

type GroupsResponse struct {
	Items      []GroupWithStats `json:"items"`
	Pagination *Pagination     `json:"pagination"`
}

type DB struct {
	*sql.DB
}

func NewDB(dataSourceName string) (*DB, error) {
	db, err := sql.Open("sqlite3", dataSourceName)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return &DB{db}, nil
}
