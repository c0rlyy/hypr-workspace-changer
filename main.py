import json
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "hypr" / "monitors.conf"


def read_config_file(path: Path):
    config_lines = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if ("workspace =" in line or "workspace=" in line) and "#" not in line:
                config_lines.append(line)
    return config_lines


def parse_config_lines(config_lines: list[str]) -> dict[str, str]:
    parsed_lines = {}
    for line in config_lines:
        parts = [p.strip() for p in line.split(",")]
        monitor = ""
        workspace = ""
        for part in parts:
            if part.startswith("monitor:"):
                monitor = part.split(":", 1)[1].strip()
            elif part.startswith("workspace"):
                workspace = part.split("=", 1)[1].strip()
        if monitor:
            parsed_lines.setdefault(monitor, []).append(workspace)
    return parsed_lines


def get_focused_monitor() -> str:
    result = subprocess.run(
        ["hyprctl", "monitors", "-j"], capture_output=True, text=True, check=True
    )
    monitors: list[dict[str, str]] = json.loads(result.stdout)
    for m in monitors:
        if m["focused"]:
            return m["name"]
    return ""


def switch_workspace(key: str, current_monitor: str, parsed_config: dict[str, str]):
    system_workspaces = parsed_config[current_monitor]
    index = int(key)
    index -= 1
    workspace_active_number = system_workspaces[index]
    key = workspace_active_number
    subprocess.run(["hyprctl", "dispatch", "workspace", key], check=True)


if __name__ == "__main__":
    config = read_config_file(CONFIG_PATH)
    parsed_config = parse_config_lines(config)
    key = sys.argv[1]
    current_monitor = get_focused_monitor()
    switch_workspace(key, current_monitor, parsed_config)
