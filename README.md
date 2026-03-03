# Study Time Optimizer

An AI-powered study tracking platform that helps students log sessions, monitor wellness, and get productivity predictions — built with **FastAPI**, **React**, and **scikit-learn**.

## Features

- **Authentication** — Register, login, JWT access + refresh tokens, password reset, email verification  
- **Subject Management** — Create colour-coded subjects, archive/unarchive  
- **Study Sessions** — Plan → start → complete workflow with duration, productivity, and focus tracking  
- **Goals & Deadlines** — Set study-hour targets, track progress, manage upcoming deadlines  
- **Daily Wellness** — Log sleep, stress, energy, and mood each day  
- **Analytics Dashboard** — Study-time stats, subject breakdown, productivity trends, streaks, wellness–productivity correlation  
- **ML Predictions** — Stacking ensemble model (GBR + Random Forest → Ridge) predicts productivity from study hours, sleep, stress, and focus  

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Redux Toolkit, Tailwind CSS |
| Backend | Python 3.13, FastAPI, SQLAlchemy 2, Pydantic v2, Alembic |
| ML Engine | scikit-learn (StackingRegressor), joblib |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Infra | Docker, docker-compose |

## Project Structure

```
study_time_optimizer/
├── backend/           # FastAPI REST API
│   ├── app/
│   │   ├── api/v1/    # Route handlers (auth, subjects, sessions, goals, …)
│   │   ├── config/    # Settings (env-driven)
│   │   ├── database/  # SQLAlchemy connection & dependencies
│   │   ├── middleware/ # Error handling
│   │   ├── models/    # ORM models (11 tables)
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   ├── services/  # Business logic
│   │   └── utils/     # Helpers (auth, email)
│   ├── alembic/       # Database migrations
│   └── tests/         # Pytest test suite
├── frontend/          # React SPA
│   └── src/
│       ├── components/  # AppLayout, ProtectedRoute, SessionTimer
│       ├── pages/       # Dashboard, Subjects, Sessions, Analytics, …
│       ├── services/    # API client + service modules
│       ├── store/       # Redux slices (auth, subjects, sessions)
│       └── types/       # Shared TypeScript definitions
├── ml-engine/         # Productivity prediction model
│   ├── config.py      # Centralised hyperparameters & paths
│   ├── data/          # Dataset + preprocessing pipeline
│   ├── models/        # ProductivityPredictor class
│   └── training/      # Trainer + evaluator modules
├── database/          # SQL schema & seed files
├── docker/            # Dockerfiles (backend, frontend, ml)
├── docs/              # API, database, ML, contributing & user guides
└── scripts/           # Setup & DB init scripts (PowerShell + Bash)
```

## Quick Start

### Prerequisites

- Python 3.11+  
- Node.js 18+  

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/study_time_optimiser.git
cd study_time_optimiser
```

**Backend:**
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

**ML Engine (only needed if you want AI predictions):**
```bash
cd ml-engine
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example and adjust if needed:

```bash
cp .env.example .env
cp .env.example backend/.env
cp frontend/.env.example frontend/.env
```

Key defaults that work out of the box for local dev:

| Variable | Default |
|----------|---------|
| `DATABASE_URL` | `sqlite:///./study_optimizer.db` |
| `BACKEND_PORT` | `5000` |
| `VITE_API_URL` | `http://localhost:5000/api/v1` || `EMAIL_ENABLED` | `false` |

**Email verification (optional):** To enable email verification, set `EMAIL_ENABLED=true` in your `.env` and provide valid Gmail SMTP credentials:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
EMAIL_ENABLED=true
```

You must generate a **Gmail App Password** (not your regular password) — go to [Google Account → Security → App Passwords](https://myaccount.google.com/apppasswords) to create one. Replace the placeholder values with your own credentials.
### 3. Run

**Backend** (creates the SQLite database on first start):
```bash
cd backend
uvicorn app.main:app --reload --port 5000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Open **http://localhost:3000** and register a new account.

### 4. (Optional) Train the ML model

The app works fully without the ML model — all study tracking, analytics, and wellness features are available. The AI prediction endpoint (`/api/v1/ai/predict-productivity`) will return a `503` until a model is trained.

To enable AI predictions:

```bash
cd ml-engine
python -m models.productivity_predictor
```

This trains a stacking ensemble on the bundled dataset and saves the model to `ml-engine/saved_models/`.

### 5. (Optional) Docker

```bash
docker-compose up --build
```

## API Docs

With the backend running, visit:

- **Swagger UI** — http://localhost:5000/docs  
- **ReDoc** — http://localhost:5000/redoc  
- **Health check** — http://localhost:5000/health  

Full endpoint reference: [docs/API.md](docs/API.md)

## Documentation

| Document | Description |
|----------|-------------|
| [API.md](docs/API.md) | Complete endpoint reference |
| [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | Table definitions & relationships |
| [ML_MODELS.md](docs/ML_MODELS.md) | Model architecture & training details |
| [USER_GUIDE.md](docs/USER_GUIDE.md) | Feature walkthrough |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Dev setup & contribution guidelines |

## Testing

```bash
cd backend
pytest -v
```

Individual test suites via PowerShell scripts:

```powershell
.\test_auth.ps1        # Authentication flow
.\test_crud.ps1        # All CRUD endpoints
.\test_analytics.ps1   # Analytics service
.\quick_test.ps1       # Quick smoke test
```

## License

[MIT](LICENSE)
