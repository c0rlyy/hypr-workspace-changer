# workspace_script

A small Hyprland helper that lets you switch workspaces using only the keys
`1`-`5`, no matter which monitor is focused.

## Why

Hyprland assigns workspaces to monitors statically in `monitors.conf`
(e.g. workspaces `1-5` on the left monitor, `6-10` on the right one). By
default that means you have to remember different key ranges depending on
which monitor you're using — `SUPER+1` on the left monitor, but `SUPER+6` to
get the equivalent workspace on the right one.

This script removes that mental overhead: it always uses the same 5 keys.
Pressing `SUPER+1` through `SUPER+5` jumps to "the 1st through 5th workspace
of whichever monitor currently has focus," resolved by:

1. Reading `~/.config/hypr/monitors.conf` to find out which workspaces belong
   to which monitor.
2. Asking Hyprland (`hyprctl monitors -j`) which monitor is currently
   focused.
3. Mapping the pressed key to the Nth workspace of that monitor and
   dispatching `hyprctl dispatch workspace <n>`.

## Requirements

- Python 3.10+
- `hyprctl` on `PATH` (ships with Hyprland)
- A `monitors.conf` with static workspace-to-monitor assignments, e.g.:

  ```
  workspace = 1, monitor:HDMI-A-1
  workspace = 2, monitor:HDMI-A-1
  workspace = 3, monitor:HDMI-A-1
  workspace = 4, monitor:HDMI-A-1
  workspace = 5, monitor:HDMI-A-1
  workspace = 6, monitor:DVI-D-1
  workspace = 7, monitor:DVI-D-1
  workspace = 8, monitor:DVI-D-1
  workspace = 9, monitor:DVI-D-1
  workspace = 10, monitor:DVI-D-1
  ```

  Each monitor you want to use this on needs at least 5 `workspace =` lines.

## Usage

```bash
python3 main.py <key>
```

`<key>` is whichever of `1`-`5` was pressed. The script resolves the focused
monitor and dispatches the correct real workspace number for it.

## Setting it up in Hyprland

The default Omarchy/Hyprland workspace binds (`SUPER+1` .. `SUPER+5`) live in
`~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf`, sourced from
`hyprland.conf`. That file is managed by Omarchy and gets overwritten on
updates, so don't edit it directly — override the binds in your own
`~/.config/hypr/bindings.conf` instead.

Add this to `~/.config/hypr/bindings.conf`:

```
# Route workspace switching through main.py, passing the pressed key
unbind = SUPER, code:10
unbind = SUPER, code:11
unbind = SUPER, code:12
unbind = SUPER, code:13
unbind = SUPER, code:14

bindd = SUPER, code:10, Switch to workspace 1, exec, python3 /home/cenjoyer/workspace/python-projects/workspace_script/main.py 1
bindd = SUPER, code:11, Switch to workspace 2, exec, python3 /home/cenjoyer/workspace/python-projects/workspace_script/main.py 2
bindd = SUPER, code:12, Switch to workspace 3, exec, python3 /home/cenjoyer/workspace/python-projects/workspace_script/main.py 3
bindd = SUPER, code:13, Switch to workspace 4, exec, python3 /home/cenjoyer/workspace/python-projects/workspace_script/main.py 4
bindd = SUPER, code:14, Switch to workspace 5, exec, python3 /home/cenjoyer/workspace/python-projects/workspace_script/main.py 5
```

`code:10`-`code:14` are the physical keycodes for `1`-`5` (layout-independent,
matches how Omarchy's own default binds are written). Keys `6`-`0` are left
untouched, so they keep Hyprland's normal workspace-switch behavior.

Reload Hyprland to apply:

```bash
hyprctl reload
```

Then test with `SUPER+1` through `SUPER+5` on each monitor.
