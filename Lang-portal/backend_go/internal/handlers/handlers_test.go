package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"lang-portal/internal/models"
)

func setupTestRouter() (*gin.Engine, *Handlers) {
	gin.SetMode(gin.TestMode)
	r := gin.Default()

	// Initialize test database
	db, err := models.NewDB("test.db")
	if err != nil {
		panic(err)
	}

	h := NewHandlers(db)
	h.RegisterRoutes(r)
	return r, h
}

func TestGetWords(t *testing.T) {
	router, _ := setupTestRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/words", nil)
	router.ServeHTTP(w, req)

	// Check status code
	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
	}

	// Check response structure
	var response struct {
		Items         []models.WordWithStats `json:"items"`
		CurrentPage   int                    `json:"current_page"`
		TotalPages    int                    `json:"total_pages"`
		TotalItems    int                    `json:"total_items"`
		ItemsPerPage  int                    `json:"items_per_page"`
	}

	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Errorf("Failed to parse response: %v", err)
	}
}

func TestGetGroups(t *testing.T) {
	router, _ := setupTestRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/groups", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
	}

	var response struct {
		Items         []models.GroupWithStats `json:"items"`
		CurrentPage   int                     `json:"current_page"`
		TotalPages    int                     `json:"total_pages"`
		TotalItems    int                     `json:"total_items"`
		ItemsPerPage  int                     `json:"items_per_page"`
	}

	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Errorf("Failed to parse response: %v", err)
	}
}

func TestGetStudySessions(t *testing.T) {
	router, _ := setupTestRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/study_sessions", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
	}

	var response struct {
		Items         []models.StudySession `json:"items"`
		CurrentPage   int                   `json:"current_page"`
		TotalPages    int                   `json:"total_pages"`
		TotalItems    int                   `json:"total_items"`
		ItemsPerPage  int                   `json:"items_per_page"`
	}

	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Errorf("Failed to parse response: %v", err)
	}
}

func TestGetDashboardStats(t *testing.T) {
	router, _ := setupTestRouter()

	// Test Quick Stats
	t.Run("QuickStats", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/api/dashboard/quick-stats", nil)
		router.ServeHTTP(w, req)

		if w.Code != http.StatusOK {
			t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
		}

		var response struct {
			TotalWords      int `json:"total_words"`
			WordsLearned    int `json:"words_learned"`
			WordsInProgress int `json:"words_in_progress"`
		}

		if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
			t.Errorf("Failed to parse response: %v", err)
		}
	})

	// Test Study Progress
	t.Run("StudyProgress", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/api/dashboard/study_progress", nil)
		router.ServeHTTP(w, req)

		if w.Code != http.StatusOK {
			t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
		}

		var response []struct {
			Date     string `json:"date"`
			Progress int    `json:"progress"`
		}

		if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
			t.Errorf("Failed to parse response: %v", err)
		}
	})
}

func TestErrorHandling(t *testing.T) {
	router, _ := setupTestRouter()

	// Test 404 Not Found
	t.Run("NotFound", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/api/nonexistent", nil)
		router.ServeHTTP(w, req)

		if w.Code != http.StatusNotFound {
			t.Errorf("Expected status %d; got %d", http.StatusNotFound, w.Code)
		}
	})

	// Test Invalid ID parameter
	t.Run("InvalidID", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/api/words/invalid", nil)
		router.ServeHTTP(w, req)

		if w.Code != http.StatusBadRequest {
			t.Errorf("Expected status %d; got %d", http.StatusBadRequest, w.Code)
		}
	})
}

func TestReviewWord(t *testing.T) {
	router, _ := setupTestRouter()

	// Create a study session first
	// This is a simplified example - in a real test, you'd want to properly set up test data
	sessionID := 1
	wordID := 1

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", 
		"/api/study_sessions/1/words/1/review?correct=true", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
	}
}

func TestResetHistory(t *testing.T) {
	router, _ := setupTestRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/reset_history", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d; got %d", http.StatusOK, w.Code)
	}
}

// Helper function to clean up test database after tests
func cleanupTestDB() {
	db, err := models.NewDB("test.db")
	if err != nil {
		return
	}
	defer db.Close()

	// Clean up tables
	tables := []string{
		"word_review_items",
		"study_sessions",
		"study_activities",
		"words_groups",
		"groups",
		"words",
	}

	for _, table := range tables {
		db.Exec("DELETE FROM " + table)
	}
}
