# Version Control Guidelines

This document outlines the version control standards and workflow for the CitiBike Rider Probability Application.

## Git Workflow

### Branch Strategy
- **`main`** - Production-ready code, always deployable
- **`develop`** - Integration branch for features, staging environment
- **`feature/*`** - Individual feature branches (e.g., `feature/station-map`)
- **`hotfix/*`** - Emergency fixes for production (e.g., `hotfix/critical-bug`)

### Branch Naming Conventions
- Feature branches: `feature/description-of-feature`
- Bug fixes: `fix/description-of-bug`
- Hotfixes: `hotfix/description-of-fix`
- Documentation: `docs/description-of-docs`

## Commit Message Standards

### Conventional Commits Format
All commit messages must follow the conventional commits format:
```
type(scope): description
```

### Types
- **`feat`** - New features
- **`fix`** - Bug fixes
- **`docs`** - Documentation changes
- **`style`** - Code style changes (formatting, etc.)
- **`refactor`** - Code refactoring
- **`test`** - Adding or updating tests
- **`chore`** - Maintenance tasks

### Scopes
- **`frontend`** - Frontend/Next.js changes
- **`backend`** - Backend/FastAPI changes
- **`data`** - Data processing or database changes
- **`docs`** - Documentation changes
- **`infra`** - Infrastructure/deployment changes

### Examples
```
feat(frontend): add station map component
fix(backend): resolve probability calculation bug
docs: update README with deployment instructions
refactor(data): optimize data ingestion process
test(backend): add unit tests for probability module
chore: update dependencies
```

## Pre-commit Hooks

### Automatic Checks
The following checks run automatically before each commit:

1. **Cursor Rules Compliance**
   - Ensures all `.mdc` files are in `.cursor/rules/` directory
   - Prevents cursor rule files from being placed incorrectly

2. **Large File Detection**
   - Warns about files larger than 10MB
   - Helps prevent accidentally committing large data files

3. **Common File Checks**
   - Warns about `.env` files and `__pycache__` directories
   - Ensures these are properly ignored

### Commit Message Validation
- Provides guidance for conventional commit format
- Shows examples of proper commit messages
- Allows commits but encourages proper formatting

## File Organization Standards

### Cursor Rules
- All cursor rule files (`.mdc`) must be placed in `.cursor/rules/`
- Follow kebab-case naming convention
- Make names descriptive of the rule's purpose

### Project Structure
```
CitiBike/
├── .cursor/rules/          # Cursor rule files
├── backend/                # FastAPI backend
├── frontend/               # Next.js frontend
├── data/                   # Data files and processing
├── project-docs/           # Project documentation
└── .gitignore             # Git ignore rules
```

## .gitignore Rules

The project includes comprehensive `.gitignore` rules for:
- Python dependencies and cache files
- Node.js dependencies
- Environment variables
- IDE files
- OS-specific files
- Large data files (CSV files in `data/citibike_data/`)

## Best Practices

### Before Committing
1. Run `git status` to see what files are staged
2. Review changes with `git diff --cached`
3. Ensure commit message follows conventional format
4. Check that no sensitive data is being committed

### Branch Management
1. Always create feature branches from `develop`
2. Keep feature branches focused on single features
3. Delete feature branches after merging
4. Regularly sync with `develop` to avoid conflicts

### Code Review
1. All changes should be reviewed before merging
2. Use pull requests for feature branches
3. Ensure tests pass before merging
4. Update documentation as needed

## Troubleshooting

### Common Issues
- **Large files**: Add to `.gitignore` or use Git LFS
- **Cursor rules in wrong location**: Move to `.cursor/rules/`
- **Commit message format**: Use conventional commits format
- **Pre-commit hook failures**: Address the warnings before committing

### Useful Commands
```bash
# Check current status
git status

# See commit history
git log --oneline

# Create and switch to feature branch
git checkout -b feature/new-feature

# Sync with develop
git checkout develop
git pull origin develop
git checkout feature/new-feature
git merge develop

# Clean up merged branches
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
```

## Integration with Cursor Rules

This version control system integrates with the established cursor rules:
- **File organization**: Enforces proper placement of cursor rule files
- **Task labeling**: Supports sequential task numbering in documentation
- **Project structure**: Maintains clear separation of concerns

For more details on cursor rules, see `.cursor/rules/cursor-rules-location.mdc`. 