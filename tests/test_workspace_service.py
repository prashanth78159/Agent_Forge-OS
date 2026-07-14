
import pytest
from unittest.mock import MagicMock

class MockBaseDataService:
    @staticmethod
    def current_user_id(): return "test-uuid"
    @staticmethod
    def get_user_id(): return "test-uuid"

@pytest.fixture
def setup_mocks(monkeypatch):
    mock_db = MagicMock()
    import app.services.workspace_service as ws_module
    # Patch the local reference in the service module
    monkeypatch.setattr(ws_module, 'db', mock_db)
    monkeypatch.setattr(ws_module, 'BaseDataService', MockBaseDataService)
    return ws_module.WorkspaceService, mock_db

def test_create_workspace(setup_mocks):
    WorkspaceService, mock_db = setup_mocks
    mock_resp = MagicMock()
    mock_resp.data = [{"id": "ws-new", "name": "New WS"}]
    
    chain = MagicMock()
    chain.insert.return_value = chain
    chain.execute.return_value = mock_resp
    mock_db.client.table.return_value = chain

    res = WorkspaceService.create_workspace("New WS")
    assert res["id"] == "ws-new"

def test_get_workspaces(setup_mocks):
    WorkspaceService, mock_db = setup_mocks

    members_chain = MagicMock()
    members_chain.select.return_value = members_chain
    members_chain.eq.return_value = members_chain
    members_chain.execute.return_value = MagicMock(data=[{"workspace_id": "ws-1"}])

    workspaces_chain = MagicMock()
    workspaces_chain.select.return_value = workspaces_chain
    workspaces_chain.in_.return_value = workspaces_chain
    workspaces_chain.execute.return_value = MagicMock(data=[{"id": "ws-1", "name": "WS1"}])

    def router(table_name):
        if table_name == "workspace_members":
            return members_chain
        if table_name == "workspaces":
            return workspaces_chain
        return MagicMock()

    mock_db.client.table.side_effect = router

    res = WorkspaceService.get_workspaces()
    
    assert len(res) == 1, f"Expected 1 workspace, got {len(res)}"
    assert res[0]["name"] == "WS1"

def test_get_workspaces_empty(setup_mocks):
    WorkspaceService, mock_db = setup_mocks
    mock_empty_resp = MagicMock(data=[])
    
    chain = MagicMock()
    chain.select.return_value = chain
    chain.eq.return_value = chain
    chain.execute.return_value = mock_empty_resp
    mock_db.client.table.return_value = chain

    res = WorkspaceService.get_workspaces()
    assert res == []
