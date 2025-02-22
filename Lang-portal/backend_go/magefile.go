// +build mage

package main

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/magefile/mage/mg"
	"github.com/magefile/mage/sh"
	_ "github.com/mattn/go-sqlite3"
	"lang-portal/internal/models"
)

// Default target to run when none is specified
var Default = Run

// Install installs project dependencies
func Install() error {
	fmt.Println("Installing dependencies...")
	if err := sh.Run("go", "mod", "tidy"); err != nil {
		return err
	}
	return nil
}

// Run starts the development server
func Run() error {
	mg.Deps(Install)
	fmt.Println("Starting server...")
	cmd := exec.Command("go", "run", "cmd/server/main.go")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

// Build builds the application
func Build() error {
	mg.Deps(Install)
	fmt.Println("Building...")
	return sh.Run("go", "build", "-o", "bin/server", "./cmd/server")
}

// InitDB initializes the database and runs migrations
func InitDB() error {
	fmt.Println("Initializing database...")

	// Initialize database
	db, err := models.NewDB("words.db")
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	// Create tables
	schema := `
	CREATE TABLE IF NOT EXISTS words (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		japanese TEXT NOT NULL,
		romaji TEXT NOT NULL,
		english TEXT NOT NULL
	);

	CREATE TABLE IF NOT EXISTS groups (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL
	);

	CREATE TABLE IF NOT EXISTS words_groups (
		word_id INTEGER NOT NULL,
		group_id INTEGER NOT NULL,
		PRIMARY KEY (word_id, group_id),
		FOREIGN KEY (word_id) REFERENCES words(id),
		FOREIGN KEY (group_id) REFERENCES groups(id)
	);

	CREATE TABLE IF NOT EXISTS study_activities (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		thumbnail_url TEXT,
		description TEXT
	);

	CREATE TABLE IF NOT EXISTS study_sessions (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		group_id INTEGER NOT NULL,
		study_activity_id INTEGER NOT NULL,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (group_id) REFERENCES groups(id),
		FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
	);

	CREATE TABLE IF NOT EXISTS word_review_items (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		word_id INTEGER NOT NULL,
		study_session_id INTEGER NOT NULL,
		correct BOOLEAN NOT NULL,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (word_id) REFERENCES words(id),
		FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
	);
	`

	if _, err := db.Exec(schema); err != nil {
		return fmt.Errorf("failed to create tables: %v", err)
	}

	fmt.Println("Database initialization completed successfully")
	return nil
}

// Seed seeds the database with initial data from JSON files
func Seed() error {
	fmt.Println("Seeding database...")

	// Initialize database
	db, err := models.NewDB("words.db")
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	// Insert seed data
	if _, err := db.Exec(`
		INSERT INTO words (japanese, romaji, english)
		VALUES 
		('こんにちは', 'konnichiwa', 'hello'),
		('さようなら', 'sayounara', 'goodbye'),
		('ありがとう', 'arigatou', 'thank you')
	`); err != nil {
		return fmt.Errorf("failed to seed database: %v", err)
	}

	fmt.Println("Database seeding completed successfully")
	return nil
}

// Reset resets the database by removing the database file
func Reset() error {
	fmt.Println("Resetting database...")
	if err := os.Remove("words.db"); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to remove database: %v", err)
	}
	fmt.Println("Database reset completed successfully")
	return nil
}

// ResetAndSeed resets the database and seeds it with initial data
func ResetAndSeed() error {
	mg.SerialDeps(Reset, InitDB, Seed)
	return nil
}

// TestDB initializes the test database with test data
func TestDB() error {
	fmt.Println("Initializing test database...")

	// Remove existing test database
	os.Remove("words.test.db")

	// Initialize database
	db, err := models.NewDB("words.test.db")
	if err != nil {
		return fmt.Errorf("failed to open test database: %v", err)
	}
	defer db.Close()

	// Apply schema
	schema, err := os.ReadFile("db/migrations/001_initial_schema.sql")
	if err != nil {
		return fmt.Errorf("failed to read schema: %v", err)
	}

	if _, err := db.Exec(string(schema)); err != nil {
		return fmt.Errorf("failed to apply schema: %v", err)
	}

	// Apply test data
	testData, err := os.ReadFile("db/test_data.sql")
	if err != nil {
		return fmt.Errorf("failed to read test data: %v", err)
	}

	if _, err := db.Exec(string(testData)); err != nil {
		return fmt.Errorf("failed to apply test data: %v", err)
	}

	fmt.Println("Test database initialized successfully")
	return nil
}
