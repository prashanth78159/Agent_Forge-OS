
import pytest
from unittest.mock import MagicMock

# Mocking dependencies for ExecutionEngine
# It's important to mock classes/modules that ExecutionEngine imports
# and interacts with, rather than trying to import and instantiate them directly
# unless they are simple data structures or pure functions.

# We'll mock the entire modules or services that ExecutionEngine depends on
# to isolate the ExecutionEngine logic for testing.

# Mock app.config.database.db.client
mock_supabase_client_instance = MagicMock()
mock_supabase_client_instance.table.return_value.select.return_value.limit.return_value.execute.return_value.data = []
mock_supabase_client_instance.table.return_value.update.return_value.eq.return_value.execute.return_value.data = []
mock_supabase_client_instance.table.return_value.insert.return_value.execute.return_value.data = []


# Mock services used by ExecutionEngine
MockLLMService = MagicMock()
MockWorkflowExecutionService = MagicMock()
MockWorkflowStatusService = MagicMock()
MockWorkflowMetricsService = MagicMock()
MockErrorService = MagicMock()
MockExecutionStateService = MagicMock()
MockDAGExecutor = MagicMock()
MockApprovalService = MagicMock()
MockAuditService = MagicMock()

# Helper for patching during tests
@pytest.fixture
def mock_execution_engine_dependencies(monkeypatch):
    # Correctly mock the 'db.client' attribute of 'app.config.database.db'
    monkeypatch.setattr('app.config.database.db.client', mock_supabase_client_instance)

    monkeypatch.setattr('app.services.llm_service.LLMService', MockLLMService)
    monkeypatch.setattr('app.services.workflow_execution_service.WorkflowExecutionService', MockWorkflowExecutionService)
    monkeypatch.setattr('app.services.workflow_status_service.WorkflowStatusService', MockWorkflowStatusService)
    monkeypatch.setattr('app.services.workflow_metrics_service.WorkflowMetricsService', MockWorkflowMetricsService)
    monkeypatch.setattr('app.services.error_service.ErrorService', MockErrorService)
    monkeypatch.setattr('app.services.execution_state_service.ExecutionStateService', MockExecutionStateService)
    monkeypatch.setattr('app.core.runtime.dag_executor.DAGExecutor', MockDAGExecutor)
    monkeypatch.setattr('app.services.approval_service.ApprovalService', MockApprovalService)
    monkeypatch.setattr('app.services.audit_service.AuditService', MockAuditService)

    # Dynamically import ExecutionEngine after patching
    from app.core.runtime.execution_engine import ExecutionEngine
    return ExecutionEngine, MockLLMService # Return MockLLMService to assert its calls

def test_execution_engine_instantiation(mock_execution_engine_dependencies):
    ExecutionEngine, MockLLMService = mock_execution_engine_dependencies
    engine = ExecutionEngine("test_provider", "test_api_key", "test_model")
    assert engine is not None
    MockLLMService.assert_called_once_with("test_provider", "test_api_key", "test_model")
    print("✅ ExecutionEngine instantiated successfully")

def test_execution_engine_methods_exist(mock_execution_engine_dependencies):
    ExecutionEngine, _ = mock_execution_engine_dependencies # We don't need MockLLMService here
    engine = ExecutionEngine("test_provider", "test_api_key", "test_model")
    assert hasattr(engine, "execute_node")
    assert callable(engine.execute_node)
    assert hasattr(engine, "run_workflow")
    assert callable(engine.run_workflow)
    print("✅ ExecutionEngine core methods exist and are callable")


