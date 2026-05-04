source ~/.config/fish/themes/colors.fish
source /usr/share/cachyos-fish-config/cachyos-config.fish
source $__fish_config_dir/environment.fish

abbr -a sedit sudoedit
abbr -a fish-reload 'source ~/.config/fish/config.fish'
abbr -a lgit lazygit
abbr -a vim nvim

# alias paste = "curl --data-binary @- https://paste.rs/" # online term paste bin 

function y
    set tmp (mktemp -t "yazi-cwd.XXXXXX")
    command yazi $argv --cwd-file="$tmp"
    if read -z cwd <"$tmp"; and [ "$cwd" != "$PWD" ]; and test -d "$cwd"
        builtin cd -- "$cwd"
    end
    rm -f -- "$tmp"
end

# Dialog to start hyprland using uwsm
# if uwsm check may-start && uwsm select
#     exec uwsm start default
# end

# Starts direcly the uwsm hyprland.desktop without prompt
# if uwsm check may-start
#     exec uwsm start hyprland.desktop
# end

# overwrite greeting
# potentially disabling fastfetch
#function fish_greeting
#    # smth smth
#end
