package handlers

import (
	"database/sql"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"lang-portal/internal/service"
)

type Handlers struct {
	dashboard      *service.DashboardService
	words          *service.WordService
	groups         *service.GroupsService
	studyActivities *service.StudyActivitiesService
	studySessions  *service.StudySessionsService
}

func NewHandlers(
	dashboard *service.DashboardService,
	words *service.WordService,
	groups *service.GroupsService,
	studyActivities *service.StudyActivitiesService,
	studySessions *service.StudySessionsService,
) *Handlers {
	return &Handlers{
		dashboard:       dashboard,
		words:          words,
		groups:         groups,
		studyActivities: studyActivities,
		studySessions:  studySessions,
	}
}

func (h *Handlers) RegisterRoutes(r *gin.Engine) {
	api := r.Group("/api")
	{
		// Dashboard endpoints
		dashboard := api.Group("/dashboard")
		{
			dashboard.GET("/last_study_session", h.GetLastStudySession)
			dashboard.GET("/study_progress", h.GetStudyProgress)
			dashboard.GET("/quick-stats", h.GetQuickStats)
		}

		// Words endpoints
		api.GET("/words", h.GetWords)
		api.GET("/words/:id", h.GetWord)

		// Groups endpoints
		api.GET("/groups", h.GetGroups)
		api.GET("/groups/:id", h.GetGroup)
		api.GET("/groups/:id/words", h.GetGroupWords)
		api.GET("/groups/:id/study_sessions", h.GetGroupStudySessions)

		// Study activities endpoints
		api.GET("/study_activities/:id", h.GetStudyActivity)
		api.GET("/study_activities/:id/study_sessions", h.GetStudyActivitySessions)
		api.POST("/study_activities", h.CreateStudySession)

		// Study sessions endpoints
		api.GET("/study_sessions", h.GetStudySessions)
		api.GET("/study_sessions/:id", h.GetStudySession)
		api.GET("/study_sessions/:id/words", h.GetStudySessionWords)
		api.POST("/study_sessions/:id/words/:word_id/review", h.ReviewWord)

		// System endpoints
		api.POST("/reset_history", h.ResetHistory)
		api.POST("/full_reset", h.FullReset)
	}
}

// Dashboard handlers
func (h *Handlers) GetLastStudySession(c *gin.Context) {
	session, err := h.dashboard.GetLastStudySession()
	if err != nil {
		if err.Error() == "no study sessions found" {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, session)
}

func (h *Handlers) GetStudyProgress(c *gin.Context) {
	progress, err := h.dashboard.GetStudyProgress()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, progress)
}

func (h *Handlers) GetQuickStats(c *gin.Context) {
	stats, err := h.dashboard.GetQuickStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, stats)
}

// Words handlers
func (h *Handlers) GetWords(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	response, err := h.words.GetWords(page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, response)
}

func (h *Handlers) GetWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	word, err := h.words.GetWordByID(id)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "word not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, word)
}

// Groups handlers
func (h *Handlers) GetGroups(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	if page < 1 {
		page = 1
	}

	response, err := h.groups.GetGroups(page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, response)
}

func (h *Handlers) GetGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	group, err := h.groups.GetGroup(id)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, group)
}

func (h *Handlers) GetGroupWords(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	if page < 1 {
		page = 1
	}

	response, err := h.groups.GetGroupWords(id, page)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, response)
}

func (h *Handlers) GetGroupStudySessions(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	sessions, pagination, err := h.groups.GetGroupStudySessions(id, page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"items":      sessions,
		"pagination": pagination,
	})
}

// Study activities handlers
func (h *Handlers) GetStudyActivity(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid study activity ID"})
		return
	}

	activity, err := h.studyActivities.GetStudyActivity(id)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "study activity not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, activity)
}

func (h *Handlers) GetStudyActivitySessions(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid study activity ID"})
		return
	}

	// First check if the study activity exists
	_, err = h.studyActivities.GetStudyActivity(id)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "study activity not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	sessions, pagination, err := h.studyActivities.GetStudyActivitySessions(id, page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":         sessions,
		"current_page":  pagination.CurrentPage,
		"total_pages":   pagination.TotalPages,
		"total_items":   pagination.TotalItems,
		"items_per_page": pagination.ItemsPerPage,
	})
}

func (h *Handlers) CreateStudySession(c *gin.Context) {
	var req struct {
		GroupID         int `json:"group_id"`
		StudyActivityID int `json:"study_activity_id"`
	}

	if err := c.BindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request body"})
		return
	}

	session, err := h.studyActivities.CreateStudySession(req.GroupID, req.StudyActivityID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, session)
}

// Study sessions handlers
func (h *Handlers) GetStudySessions(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	sessions, pagination, err := h.studySessions.GetStudySessions(page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"items":         sessions,
		"current_page":  pagination.CurrentPage,
		"total_pages":   pagination.TotalPages,
		"total_items":   pagination.TotalItems,
		"items_per_page": pagination.ItemsPerPage,
	})
}

func (h *Handlers) GetStudySession(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid study session ID"})
		return
	}

	session, err := h.studySessions.GetStudySession(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, session)
}

func (h *Handlers) GetStudySessionWords(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid study session ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	words, pagination, err := h.studySessions.GetStudySessionWords(id, page)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"items":      words,
		"pagination": pagination,
	})
}

func (h *Handlers) ReviewWord(c *gin.Context) {
	sessionID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid study session ID"})
		return
	}

	wordID, err := strconv.Atoi(c.Param("word_id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	correctStr := c.Query("correct")
	correct := correctStr == "true"

	if err := h.studySessions.ReviewWord(sessionID, wordID, correct); err != nil {
		if strings.Contains(err.Error(), "does not exist") {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success":          true,
		"word_id":         wordID,
		"study_session_id": sessionID,
		"correct":         correct,
		"created_at":      time.Now(),
	})
}

// System handlers
func (h *Handlers) ResetHistory(c *gin.Context) {
	if err := h.studySessions.ResetHistory(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Study history has been reset",
	})
}

func (h *Handlers) FullReset(c *gin.Context) {
	if err := h.studySessions.FullReset(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "System has been fully reset",
	})
}
