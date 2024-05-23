import os
SECRET_KEY = os.environ.get("PARCELTONGUE_SECRET_KEY") or "secret"

DB_NAME = os.environ.get("PARCELTONGUE_DB_NAME") or "parceltongue"
DB_USER = os.environ.get("PARCELTONGUE_DB_USER") or "executor"
DB_PASSWORD = os.environ.get("PARCELTONGUE_DB_PASSWORD") or "123456"
DB_HOST = os.environ.get("PARCELTONGUE_DB_HOST") or "localhost"
DB_PORT = os.environ.get("PARCELTONGUE_DB_PORT") or "5432"
DEFAULT_PROFILE_PIC_PATH = os.environ.get("PARCELTONGUE_DEFAULT_PROFILE_PIC") or "testav.jpg"