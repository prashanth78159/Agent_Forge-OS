
from app.services.approval_service import (
    ApprovalService
)
from app.services.notification_service import (
    NotificationService
)

def test_approval_service():
    assert hasattr(
        ApprovalService,
        "create_request"
    )
    assert hasattr(
        ApprovalService,
        "approve"
    )
    assert hasattr(
        ApprovalService,
        "reject"
    )
    print(
        "✅ Approval Service"
    )

def test_notification_service():
    assert hasattr(
        NotificationService,
        "create_notification"
    )
    print(
        "✅ Notification Service"
    )

test_approval_service()
test_notification_service()
print(
    "✅ Smoke Tests Passed")
