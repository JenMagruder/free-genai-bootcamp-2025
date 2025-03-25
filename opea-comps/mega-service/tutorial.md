# Building a Production-Ready AI System with Docker: A Step-by-Step Guide

This tutorial demonstrates how to build a production-ready AI system using Docker containers, combining an LLM server (Ollama), PostgreSQL database, and distributed tracing with Jaeger.

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Setup Guide](#detailed-setup-guide)
5. [Testing the System](#testing-the-system)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## System Overview

Our system consists of three main services:
- **Ollama**: LLM server for AI model serving
- **PostgreSQL**: Database for conversation storage
- **Jaeger**: Distributed tracing for monitoring

### Architecture Diagram
```
┌─────────────┐     ┌─────────────┐
│   Client    │────▶│    Ollama   │
│  Requests   │     │  LLM Server │
└─────────────┘     └──────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ PostgreSQL │
                    │  Database  │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │   Jaeger   │
                    │  Tracing   │
                    └────────────┘
```

## Prerequisites
- Docker Desktop installed
- Git for version control
- Basic understanding of Docker and containers
- Terminal/Command Prompt access

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd mega-service
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker compose up -d
```

## Detailed Setup Guide

### 1. Environment Configuration

Create a `.env` file with these settings:
```bash
# LLM Configuration
LLM_ENDPOINT_PORT=9000
LLM_MODEL_ID=llama3.2:1b

# Database Configuration
POSTGRES_DB=conversations_db
POSTGRES_USER=megaservice_user
POSTGRES_PASSWORD=your_secure_password
```

### 2. Database Setup

The database automatically initializes with our schema:

```sql
-- Tables for storing conversations and messages
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    metadata JSONB
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);
```

### 3. Testing Database Connection

Connect to PostgreSQL:
```bash
# Connect to container
docker exec -it postgres bash

# Connect to database
psql -U postgres

# Create test data
INSERT INTO conversations (title, metadata) 
VALUES ('Test Conversation', '{"type": "test", "model": "llama3.2:1b"}');

# View data
SELECT * FROM conversations;
```

### 4. Testing Ollama LLM Server

Pull and test the model:
```bash
# Pull model
curl http://localhost:9000/api/pull -d '{
  "model": "llama3.2:1b"
}'

# Test generation
curl http://localhost:9000/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Hello, how are you?"
}'
```

### 5. Monitoring with Jaeger

1. Access Jaeger UI: http://localhost:16686
2. View traces and system performance
3. Monitor request latency and errors

## Advanced Usage

### Custom Model Configuration
Modify the LLM settings in `.env`:
```bash
LLM_MODEL_ID=your_custom_model
```

### Database Optimization
Add indexes for better performance:
```sql
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
```bash
# Check logs
docker logs postgres

# Verify environment
docker exec postgres env
```

2. **LLM Server Issues**
```bash
# Check model status
curl http://localhost:9000/api/tags

# Restart service
docker compose restart ollama-server
```

3. **Container Won't Start**
```bash
# Check logs
docker compose logs

# Verify ports
docker compose ps
```

## Best Practices

1. **Security**
   - Use strong passwords
   - Never commit .env files
   - Regularly update dependencies

2. **Monitoring**
   - Check Jaeger traces regularly
   - Monitor database performance
   - Set up alerts for errors

3. **Backup**
   - Regular database backups
   - Version control for configurations
   - Document all changes

## Next Steps

1. Scale with Kubernetes
2. Add more AI models
3. Implement caching with Redis
4. Add authentication
5. Set up CI/CD pipeline

## Resources
- [Docker Documentation](https://docs.docker.com/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)