#!/usr/bin/env bash

##############################################
############### Launch polybar ###############
##############################################

# copy this config in ~/.config/polybar
# cp -r ~/.config/bspwm/polybar ~/.config

# kill already running bar instances
killall -q polybar

# launch bar1 and bar2
echo "---" | tee -a /tmp/polybar1.log /tmp/polybar2.log

# polybar example  >>/tmp/polybar1.log 2>&1 &
polybar top -r >>/tmp/polybar1.log 2>&1 & disown

echo "Bars launched..."