
import pytest
from unittest.mock import MagicMock

# Mock the BaseDataService and ApprovalService
class MockBaseDataService:
    @staticmethod
    def current_user_id():
        return "test-user-uuid"

class MockApprovalService:
    create_request = MagicMock()

@pytest.fixture
def setup_mocks(monkeypatch):
    monkeypatch.setattr('app.services.base_data_service.BaseDataService', MockBaseDataService)
    monkeypatch.setattr('app.services.approval_service.ApprovalService', MockApprovalService)
    from app.services.approval_routing_service import ApprovalRoutingService
    return ApprovalRoutingService

def test_process_next_level_manager_to_director(setup_mocks):
    ApprovalRoutingService = setup_mocks
    MockApprovalService.create_request.reset_mock()

    manager_approval_row = {
        "execution_id": "test_exec_id_1",
        "node_id": "approval_node_1",
        "approval_level": 1,
        "approver_group": "Manager"
    }

    result = ApprovalRoutingService.process_next_level(manager_approval_row)

    assert not result.get("final_level")
    assert result["next_level"] == 2
    MockApprovalService.create_request.assert_called_once()
    print("✅ Approval routing test fixed and verified.")
