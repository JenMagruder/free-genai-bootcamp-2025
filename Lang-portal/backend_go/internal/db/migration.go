package db

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"
	"sort"
	"strings"
)

// Migration represents a database migration
type Migration struct {
	ID      int
	Name    string
	Content string
}

// MigrationManager handles database migrations
type MigrationManager struct {
	db *sql.DB
}

// NewMigrationManager creates a new migration manager
func NewMigrationManager(db *sql.DB) *MigrationManager {
	return &MigrationManager{db: db}
}

// Initialize creates the migrations table if it doesn't exist
func (m *MigrationManager) Initialize() error {
	query := `
		CREATE TABLE IF NOT EXISTS migrations (
			id INTEGER PRIMARY KEY,
			name TEXT NOT NULL,
			applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`
	_, err := m.db.Exec(query)
	return err
}

// LoadMigrations loads all migration files from the specified directory
func (m *MigrationManager) LoadMigrations(migrationsDir string) ([]Migration, error) {
	files, err := ioutil.ReadDir(migrationsDir)
	if err != nil {
		return nil, err
	}

	var migrations []Migration
	for _, file := range files {
		if !strings.HasSuffix(file.Name(), ".sql") {
			continue
		}

		content, err := ioutil.ReadFile(filepath.Join(migrationsDir, file.Name()))
		if err != nil {
			return nil, err
		}

		var id int
		fmt.Sscanf(file.Name(), "%d_", &id)

		migrations = append(migrations, Migration{
			ID:      id,
			Name:    file.Name(),
			Content: string(content),
		})
	}

	sort.Slice(migrations, func(i, j int) bool {
		return migrations[i].ID < migrations[j].ID
	})

	return migrations, nil
}

// ApplyMigrations applies all pending migrations
func (m *MigrationManager) ApplyMigrations(migrations []Migration) error {
	for _, migration := range migrations {
		applied, err := m.isMigrationApplied(migration.ID)
		if err != nil {
			return err
		}

		if !applied {
			log.Printf("Applying migration: %s", migration.Name)
			
			tx, err := m.db.Begin()
			if err != nil {
				return err
			}

			if _, err := tx.Exec(migration.Content); err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to apply migration %s: %v", migration.Name, err)
			}

			if _, err := tx.Exec("INSERT INTO migrations (id, name) VALUES (?, ?)", 
				migration.ID, migration.Name); err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to record migration %s: %v", migration.Name, err)
			}

			if err := tx.Commit(); err != nil {
				return fmt.Errorf("failed to commit migration %s: %v", migration.Name, err)
			}
		}
	}
	return nil
}

// isMigrationApplied checks if a migration has already been applied
func (m *MigrationManager) isMigrationApplied(id int) (bool, error) {
	var count int
	err := m.db.QueryRow("SELECT COUNT(*) FROM migrations WHERE id = ?", id).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}
