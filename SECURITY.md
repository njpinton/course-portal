# Security Policy

## Sensitive Files & Directories

### Environment Variables (.gitignore ✓)
- `.env` - Production environment variables
- `.env.local` - Local development environment variables
- Contains: Database URLs, API keys, service keys

**What's Protected:**
- `SUPABASE_URL` - Database connection URL
- `SUPABASE_ANON_KEY` - Public API key for client-side access
- `SUPABASE_SERVICE_KEY` - Admin key with elevated privileges
- `FLASK_SECRET_KEY` - Session encryption key
- `JWT_SECRET` - JWT token signing key
- `ADMIN_PASSWORD` - Admin panel password hash

### Database Client (.gitignore ✓)
- `api/utils/supabase_client.py` - Database connection logic
- **Never commit this file to version control**
- Contains database abstraction and CRUD operations
- Manages both public client and admin-level access

### Student Data (.gitignore ✓)
- `data/` directory - Student submissions and enrollment data
- **CRITICAL**: Contains 71+ student exam submissions
- **NOT BACKED UP IN GIT** - Manual backup required
- See [data/README.md](data/README.md) for details

**Contents:**
- `data/CMSC173 Midterm Attachments/` - Student exam submissions
- `data/students/` - CSV enrollment files

### Exam Materials (.gitignore ✓)
- `**/finals_exam/admin/` - Answer keys
- `*ANSWER_KEY*` - Any answer key files
- These are excluded via pattern matching in .gitignore

---

## Best Practices

### 1. Environment Management
- ✓ Use `.env.local` for local development (never commit)
- ✓ Use `.env` template with placeholder values (can commit)
- ✓ Rotate service keys regularly
- ✓ Use different credentials for dev/staging/production

### 2. Data Backup
- **Regularly backup `data/` directory** to external storage
- Backup destinations:
  - External drive
  - Cloud storage (Dropbox, Google Drive)
  - Time Machine (macOS)
- Schedule: Weekly minimum, daily recommended

### 3. Code Review
- Review `.gitignore` before commits
- Use `git status --ignored` to check for sensitive files
- Never use `git add .` without verification
- Always check `git diff --staged` before committing

### 4. Production Deployment
- Use service keys only in production environment
- Enable RLS (Row Level Security) in Supabase
- Use HTTPS for all production traffic
- Enable CSP (Content Security Policy) headers
- Configure Talisman security headers in Flask

---

## Incident Response

### If Sensitive Data is Accidentally Committed:

#### 1. Remove from Git History
```bash
# Option A: Using git filter-branch (older method)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# Option B: Using BFG Repo-Cleaner (recommended - faster)
brew install bfg
bfg --delete-files sensitive-file.env
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

#### 2. Rotate All Exposed Credentials
- **Immediately** rotate all exposed API keys, passwords, and secrets
- Update `.env.local` with new credentials
- Update production environment variables on Vercel
- Update Supabase project keys if database credentials were exposed

#### 3. Review Commit History
```bash
# Check for other potential exposures
git log --all --full-history -- "*sensitive*"
git log --all --full-history -- "*.env*"
```

#### 4. Force Push (if repository is private)
```bash
git push origin --force --all
git push origin --force --tags
```

#### 5. Notify Team
- Alert all team members about the security incident
- Document the incident for future reference
- Review and update security practices

---

## Verifying Security

### Check for Exposed Secrets
```bash
# Scan for potentially sensitive files
find . -name "*.env*" -not -path "./.git/*"
find . -name "*secret*" -not -path "./.git/*"
find . -name "*password*" -not -path "./.git/*"

# Check what's staged
git status
git status --ignored

# Verify .gitignore is working
git check-ignore -v api/utils/supabase_client.py
git check-ignore -v .env.local
git check-ignore -v data/
```

### Pre-Commit Checklist
- [ ] `.env.local` is not staged
- [ ] `api/utils/supabase_client.py` is not modified (or changes are intentional)
- [ ] No files in `data/` directory are staged
- [ ] No answer key files are staged
- [ ] `git diff --staged` shows only intended changes

---

## Contact

For security concerns or to report vulnerabilities:
- **Internal**: Contact the project maintainer
- **Email**: [Add contact email]

---

**Last Updated**: February 2, 2026
