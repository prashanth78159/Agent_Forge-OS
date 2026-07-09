
import pytest
from unittest.mock import MagicMock

# Mock the ApprovalService to prevent actual database calls
class MockApprovalService:
    create_request = MagicMock()

# Patch ApprovalService for testing ApprovalRoutingService
@pytest.fixture
def mock_approval_service(monkeypatch):
    monkeypatch.setattr('app.services.approval_service.ApprovalService', MockApprovalService)
    # Import ApprovalRoutingService after patching
    from app.services.approval_routing_service import ApprovalRoutingService
    return ApprovalRoutingService

def test_process_next_level_manager_to_director(mock_approval_service):
    ApprovalRoutingService = mock_approval_service
    MockApprovalService.create_request.reset_mock() # Reset mock calls before each test

    # Simulate an approval row for a Manager (level 1)
    manager_approval_row = {
        "execution_id": "test_exec_id_1",
        "node_id": "approval_node_1",
        "approval_level": 1,
        "approver_group": "Manager"
    }

    result = ApprovalRoutingService.process_next_level(manager_approval_row)

    assert not result["final_level"]
    assert result["next_level"] == 2

    # Verify ApprovalService.create_request was called correctly for the next level
    MockApprovalService.create_request.assert_called_once_with(
        execution_id="test_exec_id_1",
        node_id="approval_node_1",
        approval_level=2,
        approver_group="Director"
    )
    print("✅ Manager to Director approval routing successful")

def test_process_next_level_director_to_finance(mock_approval_service):
    ApprovalRoutingService = mock_approval_service
    MockApprovalService.create_request.reset_mock()

    # Simulate an approval row for a Director (level 2)
    director_approval_row = {
        "execution_id": "test_exec_id_2",
        "node_id": "approval_node_2",
        "approval_level": 2,
        "approver_group": "Director"
    }

    result = ApprovalRoutingService.process_next_level(director_approval_row)

    assert not result["final_level"]
    assert result["next_level"] == 3
    MockApprovalService.create_request.assert_called_once_with(
        execution_id="test_exec_id_2",
        node_id="approval_node_2",
        approval_level=3,
        approver_group="Finance"
    )
    print("✅ Director to Finance approval routing successful")

def test_process_next_level_final_level(mock_approval_service):
    ApprovalRoutingService = mock_approval_service
    MockApprovalService.create_request.reset_mock()

    # Simulate an approval row for Finance (level 3 - max level)
    finance_approval_row = {
        "execution_id": "test_exec_id_3",
        "node_id": "approval_node_3",
        "approval_level": 3,
        "approver_group": "Finance"
    }

    result = ApprovalRoutingService.process_next_level(finance_approval_row)

    assert result["final_level"]
    assert "next_level" not in result
    MockApprovalService.create_request.assert_not_called() # No new request should be created
    print("✅ Final level approval correctly identified")

def test_process_next_level_invalid_level_default_to_manager(mock_approval_service):
    ApprovalRoutingService = mock_approval_service
    MockApprovalService.create_request.reset_mock()

    # Simulate an approval row with an invalid or missing approval_level
    invalid_level_row = {
        "execution_id": "test_exec_id_4",
        "node_id": "approval_node_4",
        "approver_group": "Manager" # Assuming this is the initial state
    }

    result = ApprovalRoutingService.process_next_level(invalid_level_row)

    assert not result["final_level"]
    assert result["next_level"] == 2 # Defaults to 1, then increments to 2
    MockApprovalService.create_request.assert_called_once_with(
        execution_id="test_exec_id_4",
        node_id="approval_node_4",
        approval_level=2,
        approver_group="Director"
    )
    print("✅ Invalid level defaults to Manager and routes correctly")
