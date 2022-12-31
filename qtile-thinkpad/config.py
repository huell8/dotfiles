from libqtile import qtile
from libqtile import bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.widget import base
import csv
import re
import os
import subprocess

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

mod = "mod1"
terminal = "alacritty"
browser = "firefox"
task_manager = "alacritty -e htop"

# colors
bar_bg          = "#282c34" 
border_focus    = "#e1acff" # focused window border color
border_normal   = "#1D2330" # unfocused window border color
dmenu_color     = "#e1acff" # selected in dmenu

#keybinds
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    ### for a multi-monitor setup
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # dmenu
    Key([mod], "space", lazy.run_extension(extension.DmenuRun(
        background=bar_bg,
        foreground='#ffffff',
        selected_background=bar_bg,
        selected_foreground=dmenu_color,
        dmenu_bottom=True,
        font='SFMono Nerd Font Mono',
        fontsize=10,
    ))),
    # screenshots
    Key([mod], "u", lazy.spawn('escrotum --select --clipboard'), desc="Screenshot to clipboard"),
    Key([mod, "shift"], "u", lazy.spawn('escrotum --select ~/Downloads/screenshot.png'), desc="screenshot to ~/Downloads"),
    # spawn shortcuts 
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Return", lazy.group['scratchpad'].dropdown_toggle('term'), desc="Scrachpad terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn("emacsclient -c -a 'emacs'"), desc="Launch emacs"),
]

# groups
groups = [Group(i) for i in "asdf"]
for i in groups:
    keys.extend(
        [
            # mod + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + letter of group = Move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

# scrachpad functionality
groups.append(ScratchPad('scratchpad', [
    DropDown('term', terminal, width=0.4, height=0.5, x=0.3, y=0.2, opacity=1.0),
]))

# layouts
layout_theme = {"border_width": 2,
                "margin": 3,
                "border_focus": border_focus,
                "border_normal": border_normal
                }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
]

# widgets
widget_defaults = dict(
    font="SFMono Nerd Font Mono",
    fontsize=12,
    padding=3,
    background=bar_bg
)
extension_defaults = widget_defaults.copy()

def init_widgets_list0():
    widgets_list = [
                # left side
                widget.CurrentLayout(),
                widget.GroupBox(
                    highlight_method='line',
                    disable_drag=True,
                                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                # right side
                widget.TextBox(text="|"),
                widget.WidgetBox(
                    text_open   = '[>]',
                    text_closed = '[<]',
                    close_button_location='right',
                    mouse_callbacks={
                        'Button3': lambda: qtile.cmd_spawn(task_manager),
                    },
                    widgets=[
                        widget.Net(format="up:{up} down:{down}", interface='enp34s0', mouse_callbacks={
                                    'Button1': lambda: qtile.cmd_spawn(task_manager),
                                    'Button3': lambda: qtile.cmd_spawn(task_manager),
                                   }),
                        widget.TextBox(text=";"),
                        widget.Memory(format="RAM: {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}", mouse_callbacks={
                                    'Button1': lambda: qtile.cmd_spawn(task_manager),
                                    'Button3': lambda: qtile.cmd_spawn(task_manager),
                                   }),
                        widget.TextBox(text=";"),
                        widget.CPU(format="CPU: {freq_current}GHz {load_percent}% ", max_chars=16, mouse_callbacks={
                                    'Button1': lambda: qtile.cmd_spawn(task_manager),
                                    'Button3': lambda: qtile.cmd_spawn(task_manager),
                                   }),
                    ]
                                 ),
                widget.TextBox(text="|"),
                widget.Battery(),
                widget.TextBox(text="|"),
                widget.Volume(cardid=0, channel='Master', fmt='vol: {}',
                              mouse_callbacks={
                                  'Button3': lambda: qtile.cmd_spawn(terminal + ' -e alsamixer'),
                              }),
                widget.TextBox(text="|"),
                widget.Clock(format="%A, %Y-%m-%d %H:%M UTC",
                             mouse_callbacks={
                                 'Button1': lambda: qtile.cmd_spawn(terminal + ' -e calcurse'),
                                 'Button3': lambda: qtile.cmd_spawn(terminal + ' -e shutdown'),
                             }),
                widget.Sep(foreground=bar_bg, linewidth=2),
    ]
    return widgets_list

screens = [
    Screen(
        bottom=bar.Bar(
            init_widgets_list0(),
            24,
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_focus = border_focus,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
