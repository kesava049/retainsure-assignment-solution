## CHANGES.md
### Major Issues Identified
- Original code was vulnerable to SQL Injection due to unsafe use of f-strings in SQL queries.
- The app had no clear separation of concerns, mixing routing, database access, and utilities in one file.
- User passwords were stored in plain text, a critical security issue.
- There was minimal error handling or input validation.
- API responses lacked consistent use of HTTP status codes and structured JSON payloads.

### Changes Made
- Modularized the codebase into separate components:
- routes/ for Flask endpoints, further divided into user and auth routes.
- models.py managing database queries.
- db.py handling SQLite connections.
- utils.py with functions for secure password hashing and verification.
- config.py for configuration settings.
- Replaced all SQL queries with parameterized queries to prevent injection.
- Implemented password hashing with werkzeug.security to store passwords securely.
- Created a migration script to hash existing passwords without needing to recreate the database.
- Added input validation on all endpoints handling user input, returning appropriate error messages.
- Improved API responses with consistent JSON format and meaningful HTTP status codes (200, 201, 400, 401, 404, 409).
- Added simple error handling for missing users, invalid data, and duplicates.

### Architectural Decisions and Justifications
- Separated concerns to enhance code readability, maintainability, and testability.
- Chose parameterized raw SQL over an ORM for simplicity and to minimize dependencies.
- Selected werkzeug.security utilities for password hashing as it’s built-in Flask dependency and secure.
- Maintained SQLite for lightweight storage, sufficient for the app’s scale.
- Deferred token-based authentication and session management due to scope constraints.

### Trade-offs Made
Chose to keep input validation manual and minimal to avoid adding external dependencies.
Did not introduce advanced authentication (JWT/sessions) to focus on securing password storage and fixing injection issues firt.
Allowed potential duplicates in user emails in current schema; improving constraints can be done in future database migrations.
Omitted logging and monitoring features; planned for later iterations.
Continued synchronous DB calls despite SQLite concurrency limitations, prioritizing simplicity.

🤖 AI Assistance Disclosure
- Utilized OpenAI ChatGPT to:
- Brainstorm and refine project structure and security improvements.
- Generate example code snippets for password hashing, modular routing, and error handling.
- Draft explanations and this CHANGES.md file.
- All AI-generated content was manually reviewed and adapted to fit the project’s specific requirements.
- Unusable or irrelevant generated code was rejected or rewritten.

This documentation balances thoroughness and clarity, explaining what was done and why, acknowledging compromises, and being transparent about AI assistance.