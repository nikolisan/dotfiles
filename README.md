# Hyprland Configuration

A personal collection of dotfiles for a complete configuration of a Hyprland desktop environment.

Set to run using in `uwsm managed` mode.

All the autostart programs should be managed by uwsm. For more information consult the [Systemd startup](https://wiki.hypr.land/Useful-Utilities/Systemd-start/) wiki page.

## Configuration files

| Directory | Description |
|-----------|-------------|
| `desktop_apps` | Desktop application entries (`.local/share`) |
| `fish` | Fish shell configuration |
| `hypr` | Hyprland, Hypridle, and Hyprlock configs |
| `kitty` | Kitty terminal emulator configuration |
| `nvim` | Neovim configuration (LazyVim) |
| `services` | Systemd user service units |
| `wallpapers` | Desktop wallpapers |
| `yazi` | Yazi file manager configuration |

## Installation

```bash
git clone https://github.com/nikolisan/dots.git
cd dots
./install.sh
```

This will install required packages, set fish as the default shell, stow the dotfiles, and enable the necessary systemd services.
