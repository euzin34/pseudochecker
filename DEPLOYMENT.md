Deployment notes

Recommended: deploy the full app to a Linux host (Heroku, Render, DigitalOcean App Platform, Docker, etc.) using Gunicorn as the WSGI server.

Heroku / general Gunicorn

1. Ensure dependencies include gunicorn: pip install gunicorn
2. Add a Procfile (already included) with:
   web: gunicorn web.app:app --bind 0.0.0.0:$PORT --workers $GUNICORN_WORKERS
3. Set environment variables in production:
   - FLASK_DEBUG=false
   - SECRET_KEY (set to a strong random value)
   - SENTRY_DSN (optional)
   - GOOGLE_APPLICATION_CREDENTIALS or rely on Application Default Credentials
4. Deploy (Heroku example):
   heroku create my-app
   git push heroku main
   heroku config:set FLASK_DEBUG=false SECRET_KEY="<secret>"

Systemd service example (Ubuntu)

[Unit]
Description=Pseudochecker Gunicorn service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/repo
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 web.app:app

[Install]
WantedBy=multi-user.target

Notes
- Gunicorn does not run on native Windows. Build and run on a Linux host (or use WSL/Docker locally).
- For container deployments, use the same gunicorn command in the container's CMD.
- Vercel supports static frontends and serverless functions; to publish the full Flask app prefer Render/Heroku/DO/App Platform or container-based hosts.

Security & Secrets (recommended)

- SECRET_KEY: Required to protect session cookies and signing. Set to a cryptographically secure random value in production. Example:
  export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

- REQUIRE_SECRET_KEY: Set to "1" in production to make the application refuse to start when SECRET_KEY is missing. This avoids accidental runs without session protection.

- GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON for Firebase Admin. Do NOT commit service account JSONs to the repository. Use a platform secret manager and mount files securely.

- Secret rotation: If credentials are committed accidentally, rotate them immediately and remove from git history (git filter-repo or BFG).

- CI secret scanning: The repository CI now runs gitleaks to detect common secret patterns. Address any findings before merging.

- Logging: Avoid logging full tokens, credentials, or PII. The application now avoids logging decoded tokens and limits detail in error messages.

- Recommended providers: Use managed secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) or platform config vars (Render/Heroku).

Checklist before production deploy:
- [ ] SECRET_KEY set and REQUIRE_SECRET_KEY=1
- [ ] GOOGLE_APPLICATION_CREDENTIALS provided via secret mount or ADC
- [ ] No service-account JSONs or secrets in repo (run local secret-scan to double-check)
- [ ] Rotate any potentially exposed credentials
- [ ] Ensure HTTPS terminated (HSTS header is added by the app)

Pre-commit and local secret scanning

- Install pre-commit locally and enable hooks:
  pip install pre-commit
  pre-commit install

- To run hooks on all files (useful in CI or before committing large changes):
  pre-commit run --all-files

- The repository ships a detect-secrets hook. If the initial run finds secrets, either rotate/remove them and add an exception to .secrets.baseline, or fix the cause before merging.
