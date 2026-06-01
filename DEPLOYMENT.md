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
