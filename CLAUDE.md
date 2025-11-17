# CLAUDE.md - AI Assistant Guide for Grafici_web

## Project Overview

**Project Name:** Grafici_web
**Repository:** playloud679/Grafici_web
**Type:** Web Graphics Project (to be determined)
**Current Status:** Initial repository setup

This document provides comprehensive guidance for AI assistants working on this codebase.

---

## Repository Structure

### Current State (Minimal Setup)
```
Grafici_web/
├── .git/              # Git repository metadata
├── README.md          # Project overview (minimal)
└── CLAUDE.md          # This file - AI assistant guide
```

### Expected Future Structure
As this project develops, expect the following structure:

```
Grafici_web/
├── src/               # Source code
│   ├── components/    # UI components
│   ├── utils/         # Utility functions
│   ├── assets/        # Static assets (images, fonts)
│   └── styles/        # CSS/styling files
├── public/            # Public assets
├── tests/             # Test files
├── docs/              # Documentation
├── package.json       # Node.js dependencies (if applicable)
├── README.md          # Project overview
└── CLAUDE.md          # This file
```

---

## Technology Stack

### To Be Determined
The project name "Grafici_web" suggests a web-based graphics application. Common technology stacks for such projects include:

**Potential Frontend Frameworks:**
- React.js
- Vue.js
- Vanilla JavaScript with Canvas API
- Three.js for 3D graphics
- D3.js for data visualization
- P5.js for creative coding

**Potential Build Tools:**
- Webpack
- Vite
- Parcel
- npm/yarn/pnpm

**Note:** Once the technology stack is chosen, update this section with specific versions and configurations.

---

## Development Workflow

### Branch Strategy

**Current Branch:** `claude/claude-md-mi3bcf5c88l2fywk-01NfBK88UwtHd4EGgGc2k6nM`

**Branch Naming Convention:**
- Feature branches: `feature/<descriptive-name>`
- Bug fixes: `bugfix/<issue-description>`
- Claude AI branches: `claude/<session-id>`

### Git Operations

**Committing Changes:**
```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "type: descriptive message"

# Commit types:
# - feat: New feature
# - fix: Bug fix
# - docs: Documentation changes
# - style: Code style changes (formatting)
# - refactor: Code refactoring
# - test: Adding or updating tests
# - chore: Maintenance tasks
```

**Pushing Changes:**
```bash
# Always push to the correct branch with -u flag
git push -u origin claude/<session-id>

# If network errors occur, retry with exponential backoff:
# - 1st retry: wait 2s
# - 2nd retry: wait 4s
# - 3rd retry: wait 8s
# - 4th retry: wait 16s
```

**Important:** Claude branches must start with `claude/` and end with the matching session ID. Pushing to other branches will result in 403 errors.

---

## Code Conventions

### General Principles
1. **Write Clean Code:** Follow established patterns, use meaningful names
2. **Keep It DRY:** Don't Repeat Yourself - extract common logic
3. **SOLID Principles:** Single responsibility, open/closed, etc.
4. **Comment Wisely:** Explain "why", not "what"
5. **Test Coverage:** Write tests for critical functionality

### File Naming
- Use kebab-case for files: `my-component.js`
- Use PascalCase for React components: `MyComponent.jsx`
- Use camelCase for utilities: `myUtility.js`

### Code Style
Once a linter/formatter is added (e.g., ESLint, Prettier), follow its rules strictly.

**Recommended defaults:**
- Indent: 2 or 4 spaces (be consistent)
- Semicolons: Yes (for JavaScript)
- Quotes: Single quotes for strings (unless project uses double)
- Line length: Max 80-100 characters

---

## Security Best Practices

### Never Commit Sensitive Data
- API keys
- Passwords
- Private keys
- `.env` files with secrets
- Database credentials

### Use Environment Variables
```bash
# .env (add to .gitignore)
API_KEY=your_key_here
DATABASE_URL=your_db_url
```

### Common Vulnerabilities to Avoid
1. **XSS (Cross-Site Scripting):** Sanitize user input
2. **SQL Injection:** Use parameterized queries
3. **CSRF:** Implement CSRF tokens
4. **Command Injection:** Validate and sanitize system commands
5. **Insecure Dependencies:** Regularly update packages

---

## Testing Strategy

### Types of Tests
1. **Unit Tests:** Test individual functions/components
2. **Integration Tests:** Test component interactions
3. **End-to-End Tests:** Test complete user flows
4. **Visual Regression Tests:** For graphics/UI changes

### Testing Tools (Recommended)
- Jest or Vitest for unit tests
- React Testing Library for component tests
- Playwright or Cypress for E2E tests

---

## AI Assistant Responsibilities

### When Working on This Project

**1. Always Research First**
- Use `Grep` and `Glob` to understand existing code
- Read related files before making changes
- Check for existing patterns and follow them

**2. Use TodoWrite for Task Management**
- Break down complex tasks into steps
- Track progress with todo items
- Mark tasks as in_progress → completed

**3. Maintain Code Quality**
- Follow existing conventions
- Write clear commit messages
- Test changes when possible

**4. Communication**
- Be concise and clear
- Reference code locations: `file_path:line_number`
- Explain reasoning for architectural decisions

**5. Git Operations**
- Always develop on the designated Claude branch
- Commit frequently with descriptive messages
- Push when work is complete or at logical stopping points

### Tool Usage Priorities

**For File Operations:**
- ✅ Use `Read` to read files (not `cat`)
- ✅ Use `Edit` to modify files (not `sed`)
- ✅ Use `Write` to create files (not `echo >`)
- ✅ Use `Grep` to search content (not `grep`)
- ✅ Use `Glob` to find files (not `find`)

**For Exploration:**
- Use `Task` tool with `subagent_type=Explore` for codebase exploration
- Use parallel tool calls when operations are independent

---

## Documentation Standards

### Code Documentation
- Document public APIs and exported functions
- Include parameter types and return values
- Add usage examples for complex functions

### File Headers (Optional)
```javascript
/**
 * @file my-component.js
 * @description Brief description of what this file does
 * @author AI Assistant / Human Developer
 */
```

### README Updates
Keep README.md updated with:
- Project description
- Installation instructions
- Usage examples
- Contributing guidelines

---

## Project Roadmap

### Current Phase: Project Initialization
- [x] Create repository
- [x] Add README.md
- [x] Create CLAUDE.md guide
- [ ] Define project scope and requirements
- [ ] Choose technology stack
- [ ] Set up project structure
- [ ] Configure build tools
- [ ] Add linting and formatting
- [ ] Set up testing framework

### Future Phases
1. **Planning Phase:** Define features and architecture
2. **Development Phase:** Implement core functionality
3. **Testing Phase:** Comprehensive testing
4. **Deployment Phase:** Set up CI/CD and hosting
5. **Maintenance Phase:** Bug fixes and updates

---

## Troubleshooting

### Common Issues

**Git Push Failures:**
- Ensure branch name starts with `claude/` and has correct session ID
- Check network connection
- Retry with exponential backoff (up to 4 times)

**Build Errors:**
- Check for missing dependencies
- Verify Node.js version compatibility
- Clear cache and reinstall: `rm -rf node_modules && npm install`

**Test Failures:**
- Run tests in isolation to identify failures
- Check for environment-specific issues
- Verify test data and mocks are up to date

---

## Resources

### Project Resources
- **Repository:** https://github.com/playloud679/Grafici_web
- **Issues:** (Use GitHub issues when available)
- **Documentation:** (Add links when created)

### General Resources
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript.info](https://javascript.info/)
- [React Documentation](https://react.dev/) (if using React)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## Updates and Maintenance

**Last Updated:** 2025-11-17
**Updated By:** Claude AI Assistant

### Update Log
- **2025-11-17:** Initial CLAUDE.md creation for project setup

### When to Update This Document
- Technology stack is chosen or changed
- New conventions are established
- Project structure evolves significantly
- New tools or workflows are adopted
- Security practices are updated

---

## Quick Reference

### Essential Commands
```bash
# Check repository status
git status

# Create and switch to new branch
git checkout -b branch-name

# Stage and commit changes
git add .
git commit -m "feat: description"

# Push to remote
git push -u origin branch-name

# View recent commits
git log --oneline -10

# Check what changed
git diff
```

### File Operations
```bash
# Find files by pattern
Glob: "**/*.js"

# Search content
Grep: pattern="searchTerm" output_mode="content"

# Read file
Read: file_path="/path/to/file"

# Edit file
Edit: old_string="..." new_string="..."
```

---

## Notes for Future Development

### Decisions to Make
1. **Graphics Library:** What library/framework for graphics?
2. **State Management:** Redux, MobX, Context API, or other?
3. **Styling Approach:** CSS-in-JS, Sass, Tailwind, or plain CSS?
4. **Backend:** Static site or needs backend API?
5. **Deployment:** Vercel, Netlify, GitHub Pages, or custom hosting?

### Best Practices to Establish
- Code review process
- Version numbering scheme (SemVer recommended)
- Release process
- Documentation standards
- Contribution guidelines

---

**End of Document**

*This CLAUDE.md file should be treated as a living document and updated as the project evolves.*
