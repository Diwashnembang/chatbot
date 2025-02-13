# GadgetHub Chatbot

A real-time AI chatbot for GadgetHub's customer service using Flask, WebSocket, and OpenAI GPT-4.

## Quick Start

1. Setup environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

2. Install:
```bash
pip install flask openai flask-socketio psycopg2-binary python-dotenv
```

3. Initialize DB:
```bash
python db.py
```

4. Run:
```bash
python app.py
```

## Environment Variables
```
OPENAI_API_KEY=your_key
DB_HOST=localhost
DB_USER=user
DB_PASSWORD=pass
DB_NAME=gadgethub
```

## Features
- Real-time chat via WebSocket
- AI-powered responses using GPT-4
- PostgreSQL for FAQ storage
- Response caching