#!/bin/bash
theme=$1

if [[ $# -ge 2 ]]; then
    main_monitor=$2
else
    main_monitor="DP-2"
fi
if [[ $# -ge 3 ]]; then
    second_monitor=$3
else
    second_monitor="HDMI-A-3"
fi

dir_with_configs=/home/air_berlin/Theme/$theme-theme-dir

main_monitor_movie="$(cat $dir_with_configs/$theme-right-wallpaper)"
second_monitor_movie="$(cat $dir_with_configs/$theme-left-wallpaper)"

font="$(cat $dir_with_configs/$theme-font)"
emacs_theme="$(cat $dir_with_configs/$theme-emacs-theme)"

light="$(cat $dir_with_configs/$theme-light)"
dark="$(cat $dir_with_configs/$theme-dark)"

waybar_style=$theme-waybar-style.css
zathura_config=$theme-zathurarc
kitty_config=$theme-kitty
ncspot_config=$theme-ncspot

zathura_reload=$theme-zathura-reload

# discord
cp $dir_with_configs/$theme-discord /home/air_berlin/.config/BetterDiscord/themes/DiscordPlus.theme.css

# emacs
emacsclient -e "(apply-theme '$emacs_theme \"$font\")"

echo $theme > $dir_with_configs/../current_theme

# zathura
cp $dir_with_configs/$zathura_config /home/air_berlin/.config/zathura/zathurarc
/home/air_berlin/OtherPrograms/zathura-scripts/send_zathura_commands_from_file.py $dir_with_configs/$zathura_reload &

# waybar
cp $dir_with_configs/$waybar_style /home/air_berlin/.config/waybar/style.css

# mpvpaper
mpv_pids="$(pidof mpvpaper)"
nohup /usr/local/bin/mpvpaper -f -o "no-audio --loop" $main_monitor "$main_monitor_movie"
nohup /usr/local/bin/mpvpaper -f -o "no-audio --loop" $second_monitor "$second_monitor_movie"
kill $mpv_pids


# hyprland borders
hyprctl keyword general:col.active_border $light $dark

# kitty
cp $dir_with_configs/$kitty_config /home/air_berlin/.config/kitty/kitty.conf
length=$(hyprctl -j clients | jq '. | length')
for ((i=0; i<length; i++)); do
    if [[ $(hyprctl -j clients | jq -r ".[$i].class") = "kitty" ]]; then
        hyprctl dispatch sendshortcut Control+Shift,F5,address:$(hyprctl -j clients | jq -r ".[$i].address")
    fi
done

# ncspot
cp $dir_with_configs/$ncspot_config /home/air_berlin/.config/ncspot/config.toml
hyprctl dispatch sendshortcut Control,j,title:Spotify
