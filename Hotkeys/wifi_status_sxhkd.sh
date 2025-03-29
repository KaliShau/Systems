#!/bin/bash

# Проверяем, включен ли Wi-Fi
wifi_status=$(nmcli radio wifi)

if [[ "$wifi_status" == "enabled" ]]; then
    # Получаем имя активной сети
    connected_ssid=$(nmcli -t -f active,ssid dev wifi | grep -E '^yes:' | cut -d: -f2)
    
    if [[ -n "$connected_ssid" ]]; then
        echo "  $connected_ssid"  # Иконка + имя сети
    else
        echo "No connection"   # Wi-Fi включен, но нет подключения
    fi
else
    echo "  off"          # Wi-Fi выключен
fi