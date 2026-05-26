#!/usr/bin/env python3
# Start the Pseudochecker web application.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.app import app

if __name__ == "__main__":
    print("Pseudochecker web app: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop.")
    app.run(host="127.0.0.1", port=5000, debug=True)
