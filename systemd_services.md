# List of required systemd sevices for the uwsm managed Hyprland

Enable theses services within systemd:

| Service | Command |
| ---------- | ------ |
| hyprpaper | systemctl --user enable --now hyprpaper.service |
| hypridle | systemctl --user enable --now hypridle.service |

These are required services for the system to function.

Usually they are setup in the hyprland.conf using `exec-once`, however in
`uwsm managed` system we should let `systemctl` do the hard work.
