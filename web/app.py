#
# Flask web application for Pseudochecker.

import os
import sys
from pathlib import Path
import logging
import time

from flask import Flask, jsonify, render_template, request

# Optional Firebase Admin for verifying ID tokens
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth, credentials as fb_credentials
except Exception:
    firebase_admin = None
    firebase_auth = None
    fb_credentials = None

# Optional Sentry integration (enabled when SENTRY_DSN env var is set)
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FlaskIntegration()], traces_sample_rate=0.0)
        logging.info('Sentry initialized')
    except Exception:
        logging.exception('Failed to initialize Sentry SDK')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Ensure project root is on sys.path so 'src' package can be imported when running this file directly
sys.path.insert(0, str(PROJECT_ROOT))

from src.checker import PseudocodeChecker

# Application start time for uptime reporting
APP_START_TIME = time.time()

# Configure basic logging (console + file)
try:
    logs_dir = PROJECT_ROOT / 'logs'
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / 'pseudochecker.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(str(log_file), encoding='utf-8')
        ]
    )
except Exception:
    logging.basicConfig(level=logging.INFO)
    logging.exception('Failed to configure file logging; falling back to console only')


def _project_id_from_service_account(path):
    try:
        import json
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            return data.get('project_id')
    except Exception:
        return None


def init_firebase_admin():
    """Attempt to initialize firebase_admin using Application Default Credentials.
    Ensures a project ID is provided to avoid "A project ID is required" errors.
    Strategy:
      1. If already initialized, return True.
      2. Try ADC (google.auth.default) to obtain project_id and credentials.
      3. Try GOOGLE_APPLICATION_CREDENTIALS (service account file) and extract project_id.
      4. Fallback: search for local service-account JSON files in repo and use the first that works.

    Returns True if initialized, False otherwise.
    """
    if firebase_admin is None:
        logging.warning("firebase_admin package not available")
        return False

    # If already initialized elsewhere in this process, treat as initialized
    try:
        firebase_admin.get_app()
        logging.info("Firebase Admin already initialized in this process")
        return True
    except Exception:
        pass

    # Helper to perform initialize_app with optional project_id
    def try_initialize(cred, project_id=None, source=""):
        try:
            opts = {}
            if project_id:
                opts['projectId'] = project_id
            firebase_admin.initialize_app(cred, opts or None)
            logging.info(f"Firebase Admin initialized using {source} (project_id={project_id})")
            return True
        except Exception:
            logging.exception(f"Failed to initialize Firebase Admin using {source}")
            return False

    # 1) Try google.auth.default() to get ADC and project id
    try:
        try:
            import google.auth
            adc_creds, adc_project = google.auth.default()
            if adc_creds:
                # Wrap ADC in firebase credential
                try:
                    cred = fb_credentials.ApplicationDefault()
                    if try_initialize(cred, project_id=adc_project, source='Application Default Credentials'):
                        return True
                except Exception:
                    logging.exception('Failed to initialize with fb_credentials.ApplicationDefault()')
        except Exception:
            logging.info('google.auth.default() not available or returned no project id')
    except Exception:
        logging.exception('Error while trying ADC')

    # 2) If explicit env var set, try it and extract project id. Also check a common keys folder on Windows (C:\keys) if env var wasn't set.
    candidate_paths = []
    env_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if env_path:
        candidate_paths.append(env_path)
    # common fallback path where the key was moved earlier
    default_key = r'C:\keys\pesudochecker-service-account.json'
    if os.path.exists(default_key):
        candidate_paths.append(default_key)

    for pth in candidate_paths:
        if not os.path.exists(pth):
            continue
        proj = _project_id_from_service_account(pth)
        try:
            cred = fb_credentials.Certificate(pth)
            if try_initialize(cred, project_id=proj, source=f'GOOGLE_APPLICATION_CREDENTIALS fallback {pth}'):
                return True
        except Exception:
            logging.exception(f'Failed initializing from service account file {pth}')

    # 3) Fallback: search for a local service account file in repo root
    try:
        candidates = list(Path(__file__).resolve().parent.parent.glob('*firebase*.json'))
        candidates += list(Path(__file__).resolve().parent.parent.glob('*adminsdk*.json'))
        for p in candidates:
            proj = _project_id_from_service_account(str(p))
            try:
                cred = fb_credentials.Certificate(str(p))
                if try_initialize(cred, project_id=proj, source=f'local candidate {p.name}'):
                    logging.warning(f'Initialized from local service account {p}; ensure it is secured')
                    return True
            except Exception:
                logging.exception(f'Failed initializing from local candidate {p}')
    except Exception:
        logging.exception('Error searching for local service account files')

    # 4) Last resort: check GOOGLE_CLOUD_PROJECT env var and try ADC without project
    env_proj = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if env_proj:
        try:
            cred = fb_credentials.ApplicationDefault()
            if try_initialize(cred, project_id=env_proj, source='ADC with GOOGLE_CLOUD_PROJECT'):
                return True
        except Exception:
            logging.exception('Failed to initialize ADC with GOOGLE_CLOUD_PROJECT')

    logging.error('Could not initialize Firebase Admin SDK with a project ID')
    return False


def verify_firebase_id_token(req):
    """Extract Bearer token from Authorization header and verify it with Firebase Admin.
    Returns (decoded_token, None) on success or (None, (message, status_code)) on failure.
    """
    if firebase_auth is None:
        return None, ("Firebase Admin SDK not available on server", 500)
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, ("Missing or malformed Authorization header", 401)
    token = auth_header.split(" ", 1)[1].strip()
    try:
        decoded = firebase_auth.verify_id_token(token)
        # Log minimal user info for auditing (email or uid)
        uid = decoded.get('email') or decoded.get('uid')
        logging.info(f"Verified Firebase ID token for user: {uid}")
        return decoded, None
    except Exception as e:
        logging.exception("Failed to verify Firebase ID token")
        return None, (str(e), 401)

EXAMPLES_DIR = PROJECT_ROOT / "examples"
DOCS_DIR = PROJECT_ROOT / "docs"


def create_app():
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )

    # Initialize Firebase Admin SDK (uses Application Default Credentials / GOOGLE_APPLICATION_CREDENTIALS)
    app.config['FIREBASE_ADMIN_INITIALIZED'] = init_firebase_admin()

    # Health check endpoint
    @app.route('/health')
    def health():
        uptime = int(time.time() - APP_START_TIME)
        return jsonify({
            'status': 'ok',
            'uptime_seconds': uptime,
            'firebase_admin_initialized': app.config.get('FIREBASE_ADMIN_INITIALIZED', False),
        }), 200

    checker = PseudocodeChecker(
        treat_warnings_as_failure=False,
        include_python_preview=True,
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/reference")
    def reference():
        quick_ref = DOCS_DIR / "QUICK_REFERENCE.md"
        content = ""
        if quick_ref.exists():
            content = quick_ref.read_text(encoding="utf-8")
        return render_template("reference.html", reference_content=content)

    @app.route("/api/check", methods=["POST"])
    def api_check():
        # Require server-side Firebase Admin to be initialized for token verification
        if not app.config.get('FIREBASE_ADMIN_INITIALIZED', False):
            return jsonify({"ok": False, "message": "Server not configured for Firebase token verification."}), 500

        decoded, err = verify_firebase_id_token(request)
        if err:
            msg, code = err
            return jsonify({"ok": False, "message": f"Authentication failed: {msg}"}), code

        data = request.get_json(silent=True) or {}
        source = data.get("source", "")
        if not source.strip():
            return jsonify(
                {
                    "ok": False,
                    "errors": [
                        {
                            "type": "ValidationError",
                            "severity": "ERROR",
                            "line": 1,
                            "column": 1,
                            "message": "No pseudocode provided.",
                            "suggestion": "Type or paste pseudocode in the editor.",
                        }
                    ],
                    "warnings": [],
                    "stats": {},
                    "python_preview": None,
                    "stage": "input",
                    "message": "Empty input.",
                }
            )

        include_preview = data.get("include_python_preview", True)
        # Optionally, user info from decoded token can be used (e.g., decoded.get('email'))
        result = PseudocodeChecker(
            treat_warnings_as_failure=False,
            include_python_preview=include_preview,
        ).check(source, filename="editor")
        return jsonify(result.to_dict())

    @app.route("/api/examples")
    def api_examples_list():
        names = []
        if EXAMPLES_DIR.exists():
            names = sorted(
                p.stem for p in EXAMPLES_DIR.glob("*.txt")
            )
        return jsonify({"examples": names})

    @app.route("/api/examples/<name>")
    def api_example(name):
        safe_name = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
        path = EXAMPLES_DIR / f"{safe_name}.txt"
        if not path.exists():
            return jsonify({"error": "Example not found"}), 404
        return jsonify({"name": safe_name, "source": path.read_text(encoding="utf-8")})

    return app


app = create_app()


if __name__ == "__main__":
    # Development entrypoint: run with python web/app.py
    # Respect environment variables for production readiness
    debug_val = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    # Secret key (set via environment in production)
    app.secret_key = os.environ.get("SECRET_KEY", getattr(app, "secret_key", ""))
    app.run(debug=debug_val, host=host, port=port)
