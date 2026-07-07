
from app.services.workflow_resume_service import (
    WorkflowResumeService
)
from app.services.execution_snapshot_service import (
    ExecutionSnapshotService
)
from app.services.resume_execution_service import (
    ResumeExecutionService
)
from app.services.resume_dag_service import (
    ResumeDAGService
)
from app.services.resume_node_executor import (
    ResumeNodeExecutor
)

def test_workflow_resume_service_methods():
    assert hasattr(WorkflowResumeService, "queue_resume")
    assert hasattr(WorkflowResumeService, "mark_resumed")
    assert hasattr(WorkflowResumeService, "get_resume_request")
    assert hasattr(WorkflowResumeService, "get_node_outputs")
    print("✅ WorkflowResumeService methods exist")

def test_execution_snapshot_service_methods():
    assert hasattr(ExecutionSnapshotService, "save_snapshot")
    assert hasattr(ExecutionSnapshotService, "get_snapshot")
    print("✅ ExecutionSnapshotService methods exist")

def test_resume_execution_service_methods():
    assert hasattr(ResumeExecutionService, "resume_execution")
    print("✅ ResumeExecutionService methods exist")

def test_resume_dag_service_methods():
    assert hasattr(ResumeDAGService, "get_remaining_nodes")
    print("✅ ResumeDAGService methods exist")

def test_resume_node_executor_methods():
    assert hasattr(ResumeNodeExecutor, "execute_node")
    # Removed assertion for get_provider_key as it's a module-level function
    print("✅ ResumeNodeExecutor methods exist")

test_workflow_resume_service_methods()
test_execution_snapshot_service_methods()
test_resume_execution_service_methods()
test_resume_dag_service_methods()
test_resume_node_executor_methods()

print("✅ Resume Tests Passed")
