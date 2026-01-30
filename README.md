# Course Portal

A Flask-based web application for managing group projects, student submissions, and course materials for CMSC 173 (Machine Learning) and CMSC 178 courses at UP Cebu.

**Live Site:** [https://presenter-app.vercel.app](https://presenter-app.vercel.app)

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

## Project Structure

```
course-portal/
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
└── requirements.txt          # Python dependencies
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

## License

Private - University of the Philippines Cebu
