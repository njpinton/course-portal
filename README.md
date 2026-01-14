# Presenter App

A Flask-based web application for managing group projects, student submissions, and course materials for CMSC 173 (Machine Learning) and CMSC 178 courses.

## Features

- **Group Management**: Create and manage student groups for projects
- **Submission Portal**: Groups can submit project work with presentations and summaries
- **Admin Dashboard**: Manage students, groups, and view submissions
- **Course Hub**: Access course materials and presentations
- **Class Records**: Track exam submissions and scores

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Jinja2 templates with vanilla JavaScript
- **Deployment**: Vercel

## Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright tests)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd presenter_app
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with required environment variables:
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
FLASK_SECRET_KEY=your_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your_password_hash
```

5. Run the development server:
```bash
PYTHONPATH=. python3 -c "import sys; sys.path.insert(0, '.'); import api.index; api.index.app.run(debug=True, port=8788)"
```

The app will be available at `http://localhost:8788`

## Testing

### Playwright E2E Tests

Install Playwright:
```bash
npm install
npx playwright install
```

Run all tests:
```bash
npx playwright test --project=chromium --workers=1
```

Run specific test files:
```bash
# Group portal tests (51 tests)
npx playwright test tests/integration/group-portal.spec.js

# Group workflow tests (6 tests)
npx playwright test tests/integration/group-workflow.spec.js
```

### Test Coverage

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| group-portal.spec.js | 51 | Page load, buttons, forms, search, modal, accessibility, API |
| group-workflow.spec.js | 6 | Create group, login, add member, submit, verify |

## Project Structure

```
presenter_app/
├── api/
│   ├── index.py              # Main Flask app
│   ├── config.py             # Configuration
│   ├── routes/               # Route blueprints
│   │   ├── groups.py         # Group management
│   │   ├── admin.py          # Admin routes
│   │   └── courses.py        # Course routes
│   ├── utils/
│   │   ├── auth.py           # Authentication
│   │   └── validation.py     # Input validation
│   └── templates/            # Jinja2 templates
├── static/
│   ├── css/                  # Stylesheets
│   └── js/                   # JavaScript files
├── supabase/
│   └── migrations/           # Database migrations
├── tests/
│   └── integration/          # Playwright tests
├── supabase_client.py        # Database operations
├── requirements.txt          # Python dependencies
├── package.json              # Node dependencies
└── playwright.config.js      # Playwright config
```

## Key Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/group_portal` | Create/view groups |
| `/group_login` | Group authentication |
| `/group_submission_portal` | Submit project work |
| `/admin_login` | Admin authentication |
| `/admin_dashboard` | Admin management |
| `/course_hub` | Course materials |

## Deployment

The app is configured for Vercel deployment. Push to the main branch to trigger automatic deployment.

```bash
vercel --prod
```

## License

Private - University of the Philippines Cebu
