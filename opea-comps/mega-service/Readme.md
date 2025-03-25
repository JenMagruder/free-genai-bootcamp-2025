# Mega Service: Containerized AI System

A production-ready AI system combining Ollama LLM server, PostgreSQL database, and Jaeger tracing.

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Run:
```bash
docker compose up -d
```

## Features

### 🤖 LLM Service (Ollama)
- Serves AI models via REST API
- Supports multiple model types
- Easy model management
- [Learn more about LLM setup](TUTORIAL.md#4-testing-ollama-llm-server)

### 📊 Database (PostgreSQL)
- Stores conversations and messages
- JSONB support for flexible metadata
- Optimized indexes for performance
- [Database setup guide](TUTORIAL.md#2-database-setup)

### 📈 Monitoring (Jaeger)
- Distributed tracing
- Performance monitoring
- Request visualization
- [Monitoring guide](TUTORIAL.md#5-monitoring-with-jaeger)

## Detailed Documentation

See our [comprehensive tutorial](TUTORIAL.md) for:
- [System Overview](TUTORIAL.md#system-overview)
- [Detailed Setup Guide](TUTORIAL.md#detailed-setup-guide)
- [Advanced Usage](TUTORIAL.md#advanced-usage)
- [Troubleshooting](TUTORIAL.md#troubleshooting)
- [Best Practices](TUTORIAL.md#best-practices)

## Environment Variables

Create a `.env` file with:
```bash
# LLM Configuration
LLM_ENDPOINT_PORT=9000
LLM_MODEL_ID=llama3.2:1b

# Database Configuration
POSTGRES_DB=conversations_db
POSTGRES_USER=megaservice_user
POSTGRES_PASSWORD=your_secure_password
```

## Common Commands

### Start Services
```bash
docker compose up -d
```

### Check Status
```bash
docker compose ps
```

### View Logs
```bash
docker compose logs
```

### Connect to Database
```bash
docker exec -it postgres psql -U postgres
```

## Useful Links
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Jaeger UI](http://localhost:16686)

## Contributing
See [TUTORIAL.md](TUTORIAL.md#best-practices) for development best practices.

## Next Steps
Check our [tutorial](TUTORIAL.md#next-steps) for:
- Scaling with Kubernetes
- Adding more AI models
- Implementing caching
- Setting up authentication

## How to Run the LLM Service

We are using Ollama which is being delivered via docker compose.

We can set the port that the LLM will listening on.
`9000` is ideal when looking at many existing OPEA megasservice default ports.
This will default to 8008 if not set.

```sh
LLM_ENDPOINT_PORT=9000 docker compose up
```

When you start the Ollama it doesn't have the model downloade.
So we'll need to download the model via the API for ollama.

### Download (Pull) a model

```sh
curl http://localhost:9000/api/pull -d '{
  "model": "llama3.2:1b"
}'
```

## How to access the Jaeger UI

When you run docker compose it should start up Jager.

```sh
http://localhost:16686/
```

## How to Run the Mega Service Example

```sh
python app.py
```

## Extended Features

### Database Integration
The service includes a PostgreSQL database for storing conversations. See [TUTORIAL.md](TUTORIAL.md) for a detailed guide on:
- Setting up the database
- Managing conversations
- Integrating with the LLM service

### Additional Resources
- [Detailed Tutorial](TUTORIAL.md) - Step-by-step guide for setting up and extending the service
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Database Service

The service includes a PostgreSQL database for storing conversations and related data. To use it:

1. Copy `.env.example` to `.env` and set your database credentials
2. Start the services with docker compose:
```sh
docker compose up
```

The database will be accessible at:
- Host: localhost
- Port: 5432
- Database: defined in your .env file

### Connecting to the Database

Using psql (after installing PostgreSQL client):
```sh
psql -h localhost -U your_username -d your_database_name
```

## Testing the App

Install Jq so we can pretty JSON on output.
```sh
sudo apt-get install jq
```
https://jqlang.org/download/


cd opea-comps/mega-service
```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "messages": "Hello, how are you?"
  }' | jq '.' > output/$(date +%s)-response.json
```

```sh
  curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Hello, this is a test message"
      }
    ],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7
  }' | jq '.' > output/$(date +%s)-response.json
```