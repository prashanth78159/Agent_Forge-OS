
from app.config.database import db

def test_database_connection():
    try:
        # Attempt to fetch data from a known table to test connectivity
        result = (
            db.client
            .table("workflow_approvals")
            .select("id")
            .limit(1)
            .execute()
        )
        assert result.data is not None, "Database connection failed or table is inaccessible"
        print("✅ Database Connection Test Passed")
    except Exception as e:
        print(f"❌ Database Connection Test Failed: {e}")
        raise

# Run the test
test_database_connection()
