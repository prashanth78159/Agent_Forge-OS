
import pytest
from unittest.mock import MagicMock
import uuid

# Updated Mock to use the correct source
class MockBaseDataService:
    @staticmethod
    def current_user_id():
        return "test-user-uuid"

    @staticmethod
    def get_user_id():
        return "test-user-uuid"

@pytest.fixture(autouse=True)
def mock_rls(monkeypatch):
    # Fix the import path for the service being tested
    monkeypatch.setattr('app.services.base_data_service.BaseDataService', MockBaseDataService)

def test_save_workflow_centralized_rls():
    from app.services.workflow_service import WorkflowService
    from app.config.database import db

    # Mock DB interaction
    db.client.table = MagicMock()
    db.client.table.return_value.select.return_value.eq.return_value.execute.return_value.count = 0
    db.client.table.return_value.insert.return_value.execute.return_value.data = [{"id": str(uuid.uuid4()), "name": "Test Workflow"}]

    workflow_json = {"nodes": [], "edges": []}
    result = WorkflowService.save_workflow("Test Workflow", workflow_json)

    assert result["name"] == "Test Workflow"
    db.client.table.assert_any_call("workflows")
    print("\u2705 Workflow management test verified with new BaseDataService import.")
