# ąęćóżź
setxkbmap pl -option caps:super

# composer
picom --config $HOME/.config/picom/picom.conf &

# xrandr monitor configs
xrandr --output DP-1 --mode 2560x1440 --rate 120
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --left-of DP-1

# best tiling wm
qtile start
