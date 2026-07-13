
import pytest
from unittest.mock import MagicMock, patch
import sys
import importlib # Import importlib for module reloading

# Create specific MagicMock instances for Streamlit functions
# This ensures that `st.button` and `st.rerun` always refer to these same mocks.
mock_st_button_func = MagicMock(name="mock_st_button_func")
mock_st_rerun_func = MagicMock(name="mock_st_rerun_func")
mock_st_session_state = MagicMock(name="mock_st_session_state") # Explicit mock for session_state
mock_st_selectbox_func = MagicMock(name="mock_st_selectbox_func")
mock_st_expander_func = MagicMock(name="mock_st_expander_func")
mock_st_text_area_func = MagicMock(name="mock_st_text_area_func")
mock_st_success_func = MagicMock(name="mock_st_success_func")
mock_st_warning_func = MagicMock(name="mock_st_warning_func")
mock_st_info_func = MagicMock(name="mock_st_info_func")
mock_st_error_func = MagicMock(name="mock_st_error_func")
mock_st_json_func = MagicMock(name="mock_st_json_func")
mock_st_write_func = MagicMock(name="mock_st_write_func")


# Mock Streamlit to prevent it from running during tests
class MockStreamlit:
    # Assign specific mocks directly
    button = mock_st_button_func
    rerun = mock_st_rerun_func
    session_state = mock_st_session_state # Use the explicit session_state mock
    selectbox = mock_st_selectbox_func
    expander = mock_st_expander_func
    text_area = mock_st_text_area_func
    success = mock_st_success_func
    warning = mock_st_warning_func
    info = mock_st_info_func
    error = mock_st_error_func
    json = mock_st_json_func
    write = mock_st_write_func

    def __getattr__(self, name):
        # This __getattr__ will only be called for attributes not explicitly defined above
        print(f"DEBUG (MockStreamlit): Fallback __getattr__ for '{name}'")
        return MagicMock(name=f"Mocked st.{name}")

st = MockStreamlit()

# Mock Supabase client
mock_supabase_client_instance = MagicMock()
mock_supabase_client_instance.table.return_value.select.return_value.order.return_value.execute.return_value.data = []
mock_supabase_client_instance.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
mock_supabase_client_instance.table.return_value.update.return_value.eq.return_value.execute.return_value.data = []

@pytest.fixture
def mock_approval_center_dependencies(monkeypatch):
    # Ensure app.ui_pages.approval_center is removed from sys.modules to force re-import
    if 'app.ui_pages.approval_center' in sys.modules:
        del sys.modules['app.ui_pages.approval_center']

    # Patch Streamlit to use our mock object by modifying sys.modules
    monkeypatch.setitem(sys.modules, 'streamlit', st)

    # Patch db.client
    monkeypatch.setattr('app.config.database.db.client', mock_supabase_client_instance)

    # Mock ApprovalService
    mock_approval_service = MagicMock()
    mock_approval_service.approve = MagicMock()
    mock_approval_service.reject = MagicMock()
    mock_approval_service.add_comment = MagicMock()
    monkeypatch.setattr('app.services.approval_service.ApprovalService', mock_approval_service)

    # Mock ExecutionStateService
    mock_execution_state_service = MagicMock()
    mock_execution_state_service.save_state = MagicMock()
    monkeypatch.setattr('app.services.execution_state_service.ExecutionStateService', mock_execution_state_service)

    # Mock WorkflowResumeService
    mock_workflow_resume_service = MagicMock()
    mock_workflow_resume_service.mark_resumed = MagicMock()
    monkeypatch.setattr('app.services.workflow_resume_service.WorkflowResumeService', mock_workflow_resume_service)

    # Mock ResumeExecutionService
    mock_resume_execution_service = MagicMock()
    mock_resume_execution_service.resume_execution = MagicMock(return_value={"success": True})
    monkeypatch.setattr('app.services.resume_execution_service.ResumeExecutionService', mock_resume_execution_service)

    # Mock ApprovalRoutingService
    mock_approval_routing_service = MagicMock()
    mock_approval_routing_service.process_next_level = MagicMock(return_value={"final_level": True, "next_level": 4}) # Return final_level=True to trigger st.rerun
    monkeypatch.setattr('app.services.approval_routing_service.ApprovalRoutingService', mock_approval_routing_service)

    # Mock AuthService
    mock_auth_service = MagicMock()
    monkeypatch.setattr('app.services.auth_service.AuthService', mock_auth_service)

    # Mock RBACService
    mock_rbac_service = MagicMock()
    monkeypatch.setattr('app.services.rbac_service.RBACService', mock_rbac_service)

    # Dynamically import render AFTER all patching and force reload
    # This ensures it picks up the mocked 'streamlit' module
    import app.ui_pages.approval_center
    importlib.reload(app.ui_pages.approval_center)
    render = app.ui_pages.approval_center.render

    return {
        "render": render,
        "AuthService": mock_auth_service,
        "RBACService": mock_rbac_service,
        "ApprovalService": mock_approval_service,
        "ExecutionStateService": mock_execution_state_service,
        "WorkflowResumeService": mock_workflow_resume_service,
        "ResumeExecutionService": mock_resume_execution_service,
        "ApprovalRoutingService": mock_approval_routing_service,
        "db_client": mock_supabase_client_instance,
        "mock_st_button_func": mock_st_button_func,
        "mock_st_rerun_func": mock_st_rerun_func, # Return the specific rerun mock
        "mock_st_session_state": mock_st_session_state
    }

# --- Test Cases ---

def test_admin_sees_all_approvals_and_can_act(mock_approval_center_dependencies):
    render = mock_approval_center_dependencies["render"]
    AuthService = mock_approval_center_dependencies["AuthService"]
    RBACService = mock_approval_center_dependencies["RBACService"]
    ApprovalService = mock_approval_center_dependencies["ApprovalService"]
    mock_st_button_func = mock_approval_center_dependencies["mock_st_button_func"]
    mock_st_rerun_func = mock_approval_center_dependencies["mock_st_rerun_func"]
    mock_st_session_state = mock_approval_center_dependencies["mock_st_session_state"]

    # Simulate an admin user
    AuthService.get_user_roles.return_value = ["admin"]
    RBACService.has_role.side_effect = lambda role: role == "admin" # Admin has admin role

    # Mock Streamlit session state and functions
    mock_st_session_state.logged_in = True
    mock_st_session_state.user = {"email": "admin@example.com", "roles": ["admin"]}
    mock_st_session_state.current_page = "Approval Center" # Mimic being on the approval page

    st.selectbox.return_value = "ALL"
    st.expander.return_value.__enter__.return_value = True # Simulate expander being open
    st.text_area.return_value = "Test comment"
    st.success.return_value = None # Suppress Streamlit success messages
    st.warning.return_value = None # Suppress Streamlit warning messages
    st.info.return_value = None # Suppress Streamlit info messages
    st.error.return_value = None # Suppress Streamlit error messages
    st.json.return_value = None # Suppress Streamlit json display
    st.write.return_value = None

    # Sample approval requests
    mock_requests = [
        {"id": 1, "execution_id": "exec1", "node_id": "nodeA", "status": "PENDING", "approval_level": 1, "approver_group": "Manager"},
        {"id": 2, "execution_id": "exec2", "node_id": "nodeB", "status": "PENDING", "approval_level": 2, "approver_group": "Director"},
        {"id": 3, "execution_id": "exec3", "node_id": "nodeC", "status": "PENDING", "approval_level": 3, "approver_group": "Finance"},
        {"id": 4, "execution_id": "exec4", "node_id": "nodeD", "status": "APPROVED", "approval_level": 1, "approver_group": "Manager"}
    ]
    ApprovalService.get_requests.return_value = mock_requests

    print(f"DEBUG (Test): id(st) in test: {id(st)}")
    print(f"DEBUG (Test): AuthService.get_user_roles.return_value: {AuthService.get_user_roles.return_value}")
    print(f"DEBUG (Test): ApprovalService.get_requests.return_value: {ApprovalService.get_requests.return_value}")
    print(f"DEBUG (Test): st.selectbox.return_value: {st.selectbox.return_value}")

    # Configure the specific mock for st.button using side_effect for precise control
    button_calls = []
    first_approve_clicked = False
    def custom_mock_st_button(label, disabled=False, key=None):
        nonlocal first_approve_clicked
        button_calls.append((label, disabled, key))
        is_approve_label = "Approve-" in label
        is_not_first_clicked = not first_approve_clicked
        print(f"DEBUG (Mock Button): label: '{label}', disabled: {disabled}, first_approve_clicked: {first_approve_clicked}")
        print(f"DEBUG (Mock Button): is_approve_label={is_approve_label}, is_not_first_clicked={is_not_first_clicked}")

        if is_approve_label and is_not_first_clicked:
            first_approve_clicked = True
            print(f"DEBUG (Mock Button): Simulating click on Approve button: {label}. Returning True.")
            return True # Simulate a click on the first 'Approve' button
        print(f"DEBUG (Mock Button): Not simulating click for label='{label}'. Returning False.")
        return False # Don't trigger other button clicks

    mock_st_button_func.side_effect = custom_mock_st_button

    # Configure the specific mock for st.rerun to be a no-op (remove side_effect) and clear calls
    mock_st_rerun_func.reset_mock() # Ensure it's clean and doesn't have a side_effect
    mock_st_rerun_func.return_value = None # Ensure it returns None if called directly

    print("DEBUG (Test): Calling render()...")
    render() # Call render without expecting an exception to be raised to the test scope

    # Verify that mock_st_rerun_func was indeed called once
    mock_st_rerun_func.assert_called_once()

    print("DEBUG (Test): render() execution path complete.")
    assert mock_st_button_func.call_count > 0, "st.button was never called."

    # Verify that all pending requests were processed (ApprovalService.get_requests was called)
    ApprovalService.get_requests.assert_called_once() # Should only be called once at the beginning of render

    # Verify st.selectbox was called with correct options for admin
    expected_group_options = ["ALL", "Manager", "Director", "Finance"]
    st.selectbox.assert_called_with("Approver Group", expected_group_options)

    # Verify that buttons for pending approvals are ENABLED for admin
    pending_request_ids = [r['id'] for r in mock_requests if r['status'] == 'PENDING']
    for req_id in pending_request_ids:
        # Check for Approve button being rendered and enabled
        assert any(f'Approve-{req_id}' in label and not disabled for label, disabled, _ in button_calls)
        # Check for Reject button being rendered and enabled
        assert any(f'Reject-{req_id}' in label and not disabled for label, disabled, _ in button_calls)
        # Check for Escalate button being rendered and enabled
        assert any(f'Escalate-{req_id}' in label and not disabled for label, disabled, _ in button_calls)

    print(f"DEBUG (Test): Final button_calls list: {button_calls}")
    print("✅ Admin user sees all approvals and can act on them.")
