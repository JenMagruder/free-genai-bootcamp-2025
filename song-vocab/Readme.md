### How to run the server

```sh
uvicorn main:app --reload
```

### How to use the api

```sh
curl -X POST http://localhost:8000/api/agent \
    -H "Content-Type: application/json" \
    -d '{
        "message_request": "Find lyrics for YOASOBI Idol"
    }'
```

### Viewing Ollama Logs via Snap Install

```sh
sudo snap logs ollama
```

### Testing the SERP tool

```sh
python -m tests.serp-tool-test
```

### Testing the DGG tool

```sh
python -m tests.dgg-tool-test
```

### Testing Ollama SDK

```sh
python -m tests.ollama-test
```