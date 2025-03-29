#!/bin/bash

# Более агрессивная проверка реального соединения
if ip -o link show | grep -E 'enp|eth|eno' | grep -q 'state UP'; then
    if CONNECTION=$(nmcli -t -f NAME,DEVICE connection show --active | grep -E 'enp|eth|eno' | cut -d: -f1 | head -n1); then
        echo "󰈁 $CONNECTION"
    fi
fi