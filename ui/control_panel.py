"""Compatibility wrapper.

Some local checkouts still import `ui.control_panel` directly.
Keep this module tiny and delegate to `ui.control_panel_app`.
"""

from ui.control_panel_app import run_control_panel

if __name__ == "__main__":
    run_control_panel()
