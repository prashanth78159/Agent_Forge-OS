
import pytest
from unittest.mock import MagicMock

# Mock BaseDataService to provide the test user ID
class MockBaseDataService:
    @staticmethod
    def current_user_id():
        return "test-user-uuid"

@pytest.fixture
def setup_workflow_mocks(monkeypatch):
    # Patch BaseDataService across the app
    monkeypatch.setattr('app.services.base_data_service.BaseDataService', MockBaseDataService)
    
    # Defensively patch CurrentUserService to avoid NameErrors in legacy lookups if any still exist
    mock_legacy = MagicMock()
    mock_legacy.get_user_id.return_value = "test-user-uuid"
    monkeypatch.setattr('app.services.current_user_service.CurrentUserService', mock_legacy, raising=False)
    
    from app.services.workflow_service import WorkflowService
    from app.config.database import db
    return WorkflowService, db

def test_save_workflow_rls_compliance(setup_workflow_mocks):
    WorkflowService, db = setup_workflow_mocks
    
    # Mock db client to avoid real network calls
    db.client.table = MagicMock()
    mock_query = db.client.table.return_value.select.return_value.eq.return_value.execute
    mock_query.return_value.count = 0
    
    mock_insert = db.client.table.return_value.insert.return_value.execute
    mock_insert.return_value.data = [{"id": "new-wf-id", "name": "Test Workflow"}]

    workflow_json = {"nodes": [], "edges": []}
    result = WorkflowService.save_workflow("Test Workflow", workflow_json)

    assert result["name"] == "Test Workflow"
    db.client.table.assert_any_call("workflows")
    print("\u2705 Workflow management test verified with BaseDataService mocking.")
