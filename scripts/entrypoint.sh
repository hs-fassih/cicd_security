#!/bin/sh
set -e

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')"

# Start gunicorn
exec gunicorn -b 0.0.0.0:8080 --workers=4 --worker-class=sync --timeout=120 app:app