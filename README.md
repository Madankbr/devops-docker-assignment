# DevOps Assignment — Express Frontend + Flask Backend + MongoDB (Dockerized)

This project demonstrates a two-tier web application:

- **Frontend:** Node.js + Express (form submission UI)
- **Backend:** Flask (handles form data, saves to MongoDB)
- **Database:** MongoDB
- **Orchestration:** Docker Compose (all 3 services on one custom bridge network)

## 📁 Folder Structure

```
devops-assignment/
├── frontend/
│   ├── views/
│   │   └── index.ejs
│   ├── public/
│   │   └── style.css
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── .dockerignore
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 How It Works

1. The user opens the Express frontend (`http://localhost:3000`) and fills out a form (Name, Email, Message).
2. Express forwards the form data via `axios.post()` to the Flask backend (`http://backend:5000/submit` inside Docker network).
3. Flask validates the data and inserts it into MongoDB.
4. Flask responds with a success/error JSON, which Express renders back on the page.

## 🐳 Running with Docker Compose

```bash
# Build and start all 3 containers (frontend, backend, mongo)
docker-compose up --build

# Visit the app
http://localhost:3000

# Stop everything
docker-compose down
```

## 🔧 Running Without Docker (local dev)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
node server.js
```

> When running locally without Docker, set `BACKEND_URL=http://localhost:5000` (default already set as fallback).

## 🐋 Docker Hub Images

```bash
docker pull madankbr/devops-assignment-frontend:latest
docker pull madankbr/devops-assignment-backend:latest
```

## 🌐 API Endpoints (Flask Backend)

| Method | Route      | Description                          |
|--------|-----------|---------------------------------------|
| GET    | `/`       | Health/info message                   |
| GET    | `/health` | Health check                          |
| POST   | `/submit` | Accepts form data, saves to MongoDB   |
| GET    | `/api`    | Returns all stored submissions        |

## 📡 Network

Both services + MongoDB run on a single Docker bridge network (`app-network`), defined in `docker-compose.yml`, allowing the frontend to reach the backend via its service name (`http://backend:5000`) and the backend to reach MongoDB via (`mongodb://mongo:27017`).
