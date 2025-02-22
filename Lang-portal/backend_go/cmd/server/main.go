package main

import (
	"log"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"lang-portal/internal/handlers"
	"lang-portal/internal/middleware"
	"lang-portal/internal/models"
	"lang-portal/internal/service"
)

func main() {
	// Get database path from environment variable or use default
	dbPath := os.Getenv("DB_PATH")
	if dbPath == "" {
		dbPath = filepath.Join(".", "words.db")
	}
	dbDir := filepath.Dir(dbPath)
	if err := os.MkdirAll(dbDir, 0755); err != nil {
		log.Fatal("Failed to create database directory:", err)
	}

	// Initialize database
	db, err := models.NewDB(dbPath)
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()


	// Initialize services
	dashboardService := service.NewDashboardService(db)
	wordService := service.NewWordService(db)
	groupsService := service.NewGroupsService(db)
	studyActivitiesService := service.NewStudyActivitiesService(db)
	studySessionsService := service.NewStudySessionsService(db)

	// Initialize handlers
	h := handlers.NewHandlers(
		dashboardService,
		wordService,
		groupsService,
		studyActivitiesService,
		studySessionsService,
	)

	// Create Gin router
	r := gin.Default()

	// Add middleware
	r.Use(middleware.ErrorHandler())

	// Enable CORS
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	})

	// Register routes
	h.RegisterRoutes(r)

	log.Printf("Server starting on http://localhost:8081")
	if err := r.Run(":8081"); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}
