# Contributing to Study Time Optimizer

First off, thank you for considering contributing to Study Time Optimizer! 🎉

It's people like you that make Study Time Optimizer such a great tool for students worldwide.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- **Python 3.11+** installed
- **Node.js 18+** and npm
- **Git** for version control
- A **GitHub account**
- Basic knowledge of:
  - Python (FastAPI)
  - JavaScript/TypeScript (React)
  - SQL (SQLite/PostgreSQL)
  - Machine Learning (scikit-learn) - for ML contributions

### First Steps

1. **Fork the repository**
   - Visit [our GitHub repo](https://github.com/fannen-prt1/study-time-optimizer)
   - Click the "Fork" button in the top right

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/study-time-optimizer.git
   cd study-time-optimizer
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/fannen-prt1/study-time-optimizer.git
   ```

4. **Run the setup script**
   ```bash
   # Windows
   .\scripts\setup.ps1
   
   # Linux/macOS
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

---

## 🤝 How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check the [issue tracker](https://github.com/fannen-prt1/study-time-optimizer/issues) to avoid duplicates
- Gather relevant information about the bug
- Test with the latest version

**How to submit a good bug report:**

Use the bug report template and include:
- **Clear title** - Describe the problem concisely
- **Steps to reproduce** - Exact steps to trigger the bug
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Screenshots** - If applicable
- **Environment**:
  - OS (Windows/macOS/Linux)
  - Browser (if frontend issue)
  - Python version
  - Node version

**Example:**
```markdown
**Title:** Timer doesn't pause when clicking pause button

**Steps to reproduce:**
1. Start a study session
2. Click the "Pause" button after 5 minutes
3. Observe that timer continues counting

**Expected:** Timer should stop counting
**Actual:** Timer continues running

**Environment:**
- OS: Windows 11
- Browser: Chrome 120
- Python: 3.11.5
```

### Suggesting Features

We love new ideas! Before suggesting:
- Check [existing feature requests](https://github.com/fannen-prt1/study-time-optimizer/discussions)
- Ensure it aligns with the project's goals
- Think about how it benefits users

**Feature request template:**
```markdown
**Feature:** [Brief description]

**Problem it solves:** [What user pain point does this address?]

**Proposed solution:** [How should it work?]

**Alternatives considered:** [Other approaches you thought about]

**Additional context:** [Screenshots, mockups, examples]
```

### Contributing Code

**Types of contributions we're looking for:**
- 🐛 Bug fixes
- ✨ New features
- 🎨 UI/UX improvements
- ⚡ Performance optimizations
- 📝 Documentation improvements
- 🧪 Test coverage
- ♿ Accessibility enhancements

**Good first issues:**
Look for issues labeled:
- `good first issue` - Great for newcomers
- `help wanted` - We need help on this
- `documentation` - Docs improvements

---

## 💻 Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests (Vitest)
cd frontend
npm test
```

---

## 📝 Coding Guidelines

### Python (Backend)

**Style Guide:** Follow PEP 8

```python
# Good
def calculate_productivity_score(session_data: dict) -> float:
    """
    Calculate productivity score based on session data.
    
    Args:
        session_data: Dictionary containing session metrics
        
    Returns:
        Productivity score (0-100)
    """
    if not session_data:
        return 0.0
    
    focus_weight = 0.6
    completion_weight = 0.4
    
    return (
        session_data['focus_score'] * focus_weight +
        session_data['completion_rate'] * completion_weight
    )
```

**Best Practices:**
- Use type hints
- Write docstrings for functions/classes
- Keep functions small and focused
- Use meaningful variable names
- Handle errors gracefully
- Log important events

**Code Formatting:**
```bash
# Format with Black
black app/

# Lint with Flake8
flake8 app/

# Sort imports
isort app/
```

### TypeScript/React (Frontend)

**Style Guide:** Use ESLint + Prettier

```typescript
// Good
interface StudySessionProps {
  sessionId: string;
  onComplete: (feedback: SessionFeedback) => void;
}

export const StudySession: React.FC<StudySessionProps> = ({
  sessionId,
  onComplete,
}) => {
  const [isActive, setIsActive] = useState(false);
  
  const handleComplete = useCallback(() => {
    // Implementation
    onComplete({
      productivityScore: 85,
      focusScore: 90,
    });
  }, [onComplete]);
  
  return (
    <div className="study-session">
      {/* Component JSX */}
    </div>
  );
};
```

**Best Practices:**
- Use functional components with hooks
- Extract custom hooks for reusable logic
- Keep components small (< 200 lines)
- Use TypeScript for type safety
- Memoize expensive computations
- Handle loading and error states

**Code Formatting:**
```bash
# Lint
npm run lint

# Fix issues
npm run lint -- --fix

# Format
npm run format
```

### Database

**Naming Conventions:**
- Tables: plural, snake_case (e.g., `study_sessions`)
- Columns: snake_case (e.g., `created_at`)
- Foreign keys: `{table}_id` (e.g., `user_id`)

**Migrations:**
```bash
# Create migration
alembic revision --autogenerate -m "Add productivity_score column"

# Review the generated migration file
# Edit if necessary

# Apply migration
alembic upgrade head
```

---

## 📋 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
# Feature
feat(dashboard): add weekly progress chart

Implements a bar chart showing daily study hours for the current week.
Uses Recharts library for visualization.

Closes #123

# Bug fix
fix(timer): prevent timer from continuing when paused

Timer was not properly stopping when pause button was clicked.
Added check in tick handler to verify session status.

Fixes #456

# Documentation
docs(api): update authentication endpoint examples

Added missing request/response examples for login endpoint.

# Refactor
refactor(analytics): extract calculation logic to service layer

Moved productivity calculation from controller to service for
better testability and reusability.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow coding guidelines
   - Add tests for new features
   - Update documentation

4. **Test thoroughly**
   ```bash
   # Backend
   pytest
   
   # Frontend
   npm test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

### Submitting the PR

1. **Push to your fork**
   ```bash
   git push origin feat/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### PR Template

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
[Describe testing approach]

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Closes #[issue number]
```

### Review Process

- Maintainers will review your PR within 3-5 days
- Address any requested changes
- Once approved, a maintainer will merge your PR

**What happens next:**
1. Automated tests run (CI/CD)
2. Code review by maintainers
3. Requested changes (if any)
4. Approval and merge
5. Your contribution is live! 🎉

---

## 🧪 Testing Guidelines

### Backend Tests

```python
# tests/test_sessions.py
import pytest
from app.services.session_service import SessionService

def test_create_session(db_session, test_user):
    """Test creating a new study session"""
    service = SessionService(db_session)
    
    session_data = {
        "user_id": test_user.id,
        "subject_id": "subject_123",
        "session_type": "focused_study",
        "planned_duration_minutes": 90
    }
    
    session = service.create_session(session_data)
    
    assert session.id is not None
    assert session.status == "active"
    assert session.planned_duration_minutes == 90

def test_complete_session_with_feedback(db_session, active_session):
    """Test completing a session with feedback"""
    service = SessionService(db_session)
    
    feedback = {
        "productivity_score": 85,
        "focus_score": 88,
        "notes": "Great session!"
    }
    
    session = service.complete_session(active_session.id, feedback)
    
    assert session.status == "completed"
    assert session.productivity_score == 85
    assert session.end_time is not None
```

### Frontend Tests

The frontend uses **Vitest** as the test runner (not Jest).

```typescript
// components/session/SessionTimer.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { SessionTimer } from './SessionTimer';

describe('SessionTimer', () => {
  it('renders timer with initial duration', () => {
    render(<SessionTimer duration={90} />);
    expect(screen.getByText('1:30:00')).toBeInTheDocument();
  });
  
  it('pauses timer when pause button clicked', () => {
    const onPause = vi.fn();
    render(<SessionTimer duration={90} onPause={onPause} />);
    
    const pauseButton = screen.getByRole('button', { name: /pause/i });
    fireEvent.click(pauseButton);
    
    expect(onPause).toHaveBeenCalled();
  });
});
```

---

## 📚 Documentation

### When to Update Docs

- Adding a new feature
- Changing API endpoints
- Modifying database schema
- Updating dependencies
- Changing configuration

### Documentation Structure

```
docs/
├── API.md              # API reference
├── DATABASE_SCHEMA.md  # Database documentation
├── ML_MODELS.md        # ML model details
├── USER_GUIDE.md       # End-user guide
└── CONTRIBUTING.md     # This file
```

### Writing Good Documentation

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep it up-to-date with code changes
- Use proper markdown formatting

---

## 🎯 Project Roadmap

Check our [project roadmap](https://github.com/fannen-prt1/study-time-optimizer/projects) to see:
- What we're currently working on
- Upcoming features
- Long-term plans

---

## 🏆 Recognition

Contributors will be:
- Mentioned in release notes
- Celebrated on our Discord server!

---

## ❓ Questions?

- 💬 [Join our Discord](https://discord.gg/study-optimizer)
- 📧 Email: dev@studytimeoptimizer.com
- 💡 [GitHub Discussions](https://github.com/fannen-prt1/study-time-optimizer/discussions)

---

Thank you for contributing! Together, we're helping students worldwide study smarter! 🚀📚

**Happy Coding!** 💻✨
