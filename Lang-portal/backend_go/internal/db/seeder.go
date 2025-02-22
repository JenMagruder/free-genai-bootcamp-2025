package db

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"path/filepath"
)

type SeedConfig struct {
	Groups          []GroupConfig         `json:"groups"`
	StudyActivities []StudyActivityConfig `json:"study_activities"`
}

type GroupConfig struct {
	Name       string `json:"name"`
	SourceFile string `json:"source_file"`
}

type StudyActivityConfig struct {
	Name         string `json:"name"`
	ThumbnailURL string `json:"thumbnail_url"`
	Description  string `json:"description"`
}

type Word struct {
	Japanese string `json:"japanese"`
	Romaji   string `json:"romaji"`
	English  string `json:"english"`
}

type Seeder struct {
	db        *sql.DB
	seedsPath string
}

func NewSeeder(db *sql.DB, seedsPath string) *Seeder {
	return &Seeder{
		db:        db,
		seedsPath: seedsPath,
	}
}

func (s *Seeder) LoadAndSeed() error {
	// Read config file
	configPath := filepath.Join(s.seedsPath, "config.json")
	configData, err := ioutil.ReadFile(configPath)
	if err != nil {
		return fmt.Errorf("failed to read config file: %v", err)
	}

	var config SeedConfig
	if err := json.Unmarshal(configData, &config); err != nil {
		return fmt.Errorf("failed to parse config file: %v", err)
	}

	// Begin transaction
	tx, err := s.db.Begin()
	if err != nil {
		return fmt.Errorf("failed to start transaction: %v", err)
	}
	defer tx.Rollback()

	// Seed study activities
	if err := s.seedStudyActivities(tx, config.StudyActivities); err != nil {
		return fmt.Errorf("failed to seed study activities: %v", err)
	}

	// Seed groups and their words
	if err := s.seedGroups(tx, config.Groups); err != nil {
		return fmt.Errorf("failed to seed groups: %v", err)
	}

	// Commit transaction
	if err := tx.Commit(); err != nil {
		return fmt.Errorf("failed to commit transaction: %v", err)
	}

	return nil
}

func (s *Seeder) seedStudyActivities(tx *sql.Tx, activities []StudyActivityConfig) error {
	stmt, err := tx.Prepare(`
		INSERT INTO study_activities (name, thumbnail_url, description)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for _, activity := range activities {
		if _, err := stmt.Exec(activity.Name, activity.ThumbnailURL, activity.Description); err != nil {
			return err
		}
	}
	return nil
}

func (s *Seeder) seedGroups(tx *sql.Tx, groups []GroupConfig) error {
	// Prepare statements
	groupStmt, err := tx.Prepare(`
		INSERT INTO groups (name)
		VALUES (?)
		RETURNING id
	`)
	if err != nil {
		return err
	}
	defer groupStmt.Close()

	wordStmt, err := tx.Prepare(`
		INSERT INTO words (japanese, romaji, english)
		VALUES (?, ?, ?)
		RETURNING id
	`)
	if err != nil {
		return err
	}
	defer wordStmt.Close()

	wordGroupStmt, err := tx.Prepare(`
		INSERT INTO words_groups (word_id, group_id)
		VALUES (?, ?)
	`)
	if err != nil {
		return err
	}
	defer wordGroupStmt.Close()

	// Process each group
	for _, group := range groups {
		// Insert group
		var groupID int
		if err := groupStmt.QueryRow(group.Name).Scan(&groupID); err != nil {
			return fmt.Errorf("failed to insert group %s: %v", group.Name, err)
		}

		// Read and parse words file
		wordsPath := filepath.Join(s.seedsPath, group.SourceFile)
		wordsData, err := ioutil.ReadFile(wordsPath)
		if err != nil {
			return fmt.Errorf("failed to read words file %s: %v", group.SourceFile, err)
		}

		var words []Word
		if err := json.Unmarshal(wordsData, &words); err != nil {
			return fmt.Errorf("failed to parse words file %s: %v", group.SourceFile, err)
		}

		// Insert words and create relationships
		for _, word := range words {
			var wordID int
			if err := wordStmt.QueryRow(
				word.Japanese,
				word.Romaji,
				word.English,
			).Scan(&wordID); err != nil {
				return fmt.Errorf("failed to insert word %s: %v", word.Japanese, err)
			}

			if _, err := wordGroupStmt.Exec(wordID, groupID); err != nil {
				return fmt.Errorf("failed to create word-group relationship: %v", err)
			}
		}
	}

	return nil
}
