
from app.ui_pages.dashboard import render as dashboard_render
from app.ui_pages.platform_dashboard import render as platform_dashboard_render
from app.ui_pages.error_dashboard import render as error_dashboard_render
from app.ui_pages.audit_dashboard import render as audit_dashboard_render
from app.ui_pages.approval_analytics import render as approval_analytics_render

def test_dashboard_render_functions_exist():
    assert hasattr(dashboard_render, '__call__'), "Dashboard render function is missing"
    assert hasattr(platform_dashboard_render, '__call__'), "Platform Dashboard render function is missing"
    assert hasattr(error_dashboard_render, '__call__'), "Error Dashboard render function is missing"
    assert hasattr(audit_dashboard_render, '__call__'), "Audit Dashboard render function is missing"
    assert hasattr(approval_analytics_render, '__call__'), "Approval Analytics render function is missing"
    print("✅ All dashboard render functions exist")

test_dashboard_render_functions_exist()
