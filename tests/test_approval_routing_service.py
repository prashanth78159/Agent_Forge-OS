
import pytest
from unittest.mock import MagicMock
import sys

# Mock BaseDataService for RLS compliance
class MockBaseDataService:
    @staticmethod
    def current_user_id():
        return "test-user-uuid"

# Direct mock class to ensure we capture calls correctly
class MockApprovalService:
    create_request = MagicMock()

@pytest.fixture(autouse=True)
def setup_mocks(monkeypatch):
    # Ensure the target module is imported before patching its attributes
    import app.services.approval_routing_service as target_module
    monkeypatch.setattr(target_module, 'BaseDataService', MockBaseDataService)
    monkeypatch.setattr(target_module, 'ApprovalService', MockApprovalService)
    return target_module.ApprovalRoutingService

def test_process_next_level_routing(setup_mocks):
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
    # Verify the mock was called
    assert MockApprovalService.create_request.called
    print("\u2705 Approval routing mock assertion verified.")
