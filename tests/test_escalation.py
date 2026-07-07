
from app.services.approval_escalation_service import (
    ApprovalEscalationService
)

def test_escalation_service():
    assert hasattr(
        ApprovalEscalationService,
        "process_overdue_approvals"
    )
    print(
        "✅ Escalation Service Test Passed")

test_escalation_service()
