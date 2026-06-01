#!/usr/bin/env python3
# Start the Pseudochecker web application.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.app import app

if __name__ == "__main__":
    print("Pseudochecker web app")
    print("Press Ctrl+C to stop.")
    # Respect environment variables for production readiness
    debug_val = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    # Secret key (set via environment in production)
    app.secret_key = os.environ.get("SECRET_KEY", getattr(app, "secret_key", ""))
    app.run(debug=debug_val, host=host, port=port)
