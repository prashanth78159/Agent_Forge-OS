
import os

from app.services.database_service import (
    DatabaseService
)

db = DatabaseService(

    os.environ[
        "SUPABASE_URL"
    ],

    os.environ[
        "SUPABASE_KEY"
    ]
)
