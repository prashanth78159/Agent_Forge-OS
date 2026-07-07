
from app.services.approval_service import ApprovalService

def test_approval_service_methods():
    # Test if essential methods exist in ApprovalService
    assert hasattr(ApprovalService, "is_approval_node")
    assert hasattr(ApprovalService, "create_request")
    assert hasattr(ApprovalService, "get_requests")
    assert hasattr(ApprovalService, "approve")
    assert hasattr(ApprovalService, "reject")
    assert hasattr(ApprovalService, "add_comment")
    # Removed assertion for get_pending_requests as it no longer exists
    print("✅ All essential ApprovalService methods exist")

test_approval_service_methods()
print("✅ Approval Tests Passed")
