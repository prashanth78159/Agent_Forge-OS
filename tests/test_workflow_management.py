
import pytest
from app.services.workflow_service import WorkflowService
from app.config.database import db
import uuid
import time

# Helper function to clear test data if necessary
def clear_test_workflows(name_prefix="Test Workflow"): 
    # Delete from workflow_versions first due to foreign key constraints
    db.client.table("workflow_versions").delete().neq("workflow_id", "00000000-0000-0000-0000-000000000000").execute()
    db.client.table("workflows").delete().like("name", f"%{name_prefix}%").execute()


@pytest.fixture(autouse=True)
def setup_teardown_db():
    # Setup: Clear any lingering test data before each test
    clear_test_workflows()
    yield
    # Teardown: Clear test data after each test
    clear_test_workflows()

def test_save_new_workflow():
    workflow_name = f"Test Workflow {uuid.uuid4()}"
    workflow_json = {"nodes": [{"id": "start"}], "edges": []}

    # Save a new workflow
    result = WorkflowService.save_workflow(workflow_name, workflow_json)
    assert result is not None
    assert result["name"] == workflow_name

    workflow_id = result["id"]

    # Verify workflow is in the database
    retrieved_workflow = db.client.table("workflows").select("*").eq("id", workflow_id).execute().data
    assert len(retrieved_workflow) == 1
    assert retrieved_workflow[0]["name"] == workflow_name

    # Verify first version is created
    versions = db.client.table("workflow_versions").select("*").eq("workflow_id", workflow_id).execute().data
    assert len(versions) == 1
    assert versions[0]["version_number"] == 1
    assert versions[0]["workflow_json"] == workflow_json
    print(f"✅ Saved new workflow '{workflow_name}' and verified version 1")

def test_update_existing_workflow():
    workflow_name = f"Test Workflow {uuid.uuid4()}"
    initial_workflow_json = {"nodes": [{"id": "start"}], "edges": []}

    # Save initial workflow
    initial_result = WorkflowService.save_workflow(workflow_name, initial_workflow_json)
    workflow_id = initial_result["id"]
    print(f"Created initial workflow '{workflow_name}' with ID: {workflow_id}")

    # Introduce a small delay to ensure created_at timestamps are distinct for versioning
    time.sleep(1)

    # Update the workflow
    updated_workflow_json = {"nodes": [{"id": "start"}, {"id": "end"}], "edges": [{"source": "start", "target": "end"}]}
    update_result = WorkflowService.save_workflow(workflow_name, updated_workflow_json)
    assert update_result is not None
    assert update_result["workflow_json"] == updated_workflow_json # Should return the updated workflow directly

    # Verify workflow is updated in the database
    retrieved_workflow = db.client.table("workflows").select("*").eq("id", workflow_id).execute().data
    assert len(retrieved_workflow) == 1
    assert retrieved_workflow[0]["workflow_json"] == updated_workflow_json
    print(f"✅ Updated existing workflow '{workflow_name}'")

    # Verify a new version is created
    versions = db.client.table("workflow_versions").select("*").eq("workflow_id", workflow_id).order("version_number", desc=True).execute().data
    assert len(versions) == 2
    assert versions[0]["version_number"] == 2
    assert versions[0]["workflow_json"] == updated_workflow_json
    assert versions[1]["version_number"] == 1
    assert versions[1]["workflow_json"] == initial_workflow_json
    print(f"✅ Verified new version created for '{workflow_name}'")

# Test for get_workflows (assuming CurrentUserService is not mocking user_id, so it fetches all)
def test_get_workflows():
    # Ensure there's at least one workflow to fetch
    workflow_name_1 = f"Test Workflow {uuid.uuid4()}-1"
    workflow_name_2 = f"Test Workflow {uuid.uuid4()}-2"
    WorkflowService.save_workflow(workflow_name_1, {"nodes": [], "edges": []})
    WorkflowService.save_workflow(workflow_name_2, {"nodes": [], "edges": []})

    workflows = WorkflowService.get_workflows()
    assert len(workflows) >= 2 # Should contain at least the two we just created
    assert any(w["name"] == workflow_name_1 for w in workflows)
    assert any(w["name"] == workflow_name_2 for w in workflows)
    print("✅ get_workflows returns workflows")
