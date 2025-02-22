package middleware

import (
	"database/sql"
	"errors"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

// ErrorResponse represents a standardized error response
type ErrorResponse struct {
	Error string `json:"error"`
	Code  int    `json:"code"`
}

// ErrorHandler middleware handles errors in a consistent way
func ErrorHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		// Only handle errors if we have any
		if len(c.Errors) == 0 {
			return
		}

		err := c.Errors.Last().Err
		var statusCode int
		var message string

		switch {
		case errors.Is(err, sql.ErrNoRows):
			statusCode = http.StatusNotFound
			message = "Resource not found"
		case errors.Is(err, &ValidationError{}):
			statusCode = http.StatusBadRequest
			message = err.Error()
		default:
			statusCode = http.StatusInternalServerError
			message = "Internal server error"
			// Log the actual error for debugging
			log.Printf("Internal error: %v", err)
		}

		c.JSON(statusCode, ErrorResponse{
			Error: message,
			Code:  statusCode,
		})
	}
}

// ValidationError represents a validation error
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return e.Message
}

// NewValidationError creates a new validation error
func NewValidationError(field, message string) *ValidationError {
	return &ValidationError{
		Field:   field,
		Message: message,
	}
}
