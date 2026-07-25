import json
import subprocess
import sys
from typing import Any


def get_focused_monitor() -> Any:
    result = subprocess.run(
        ["hyprctl", "monitors", "-j"], capture_output=True, text=True, check=True
    )
    monitors: list[dict[str, Any]] = json.loads(result.stdout)
    for m in monitors:
        if m["focused"]:
            return m["name"]


def get_config_from_cmd():
    monitors_workspaces = {}
    result = subprocess.run(
        ["hyprctl", "workspacerules", "-j"], capture_output=True, text=True, check=True
    )
    monitros_config: list[dict[str, Any]] = json.loads(result.stdout)
    for config in monitros_config:
        monitor = config["monitor"]
        workspace = config["workspaceString"]
        monitors_workspaces.setdefault(monitor, []).append(workspace)
    return monitors_workspaces


def notify(msg: str) -> None:
    subprocess.run(["notify-send", "workspace-changanger", msg], check=False)

def switch_workspace(
    key: str, current_monitor: str, parsed_config: dict[str, list[str]]
):
    system_workspaces = parsed_config[current_monitor]
    index = int(key) - 1
    workspace_active_number = system_workspaces[index]
    key = workspace_active_number
    subprocess.run(["hyprctl", "dispatch", "workspace", key], check=True)


if __name__ == "__main__":
    try:
        parsed_config = get_config_from_cmd()
        key = sys.argv[1]
        current_monitor = get_focused_monitor()
        switch_workspace(key, current_monitor, parsed_config)
    except Exception as e:
        msg = "error: " + str(e)
        notify(msg)
        sys.exit(1)
