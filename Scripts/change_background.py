#!/usr/bin/env python3

import os
import random
import subprocess

background_dir = os.path.expanduser('~/.background')

images = [f for f in os.listdir(background_dir) if os.path.isfile(os.path.join(background_dir, f))]

if images:
    selected_image = random.choice(images)
    image_path = os.path.join(background_dir, selected_image)

    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri-dark', f'file://{image_path}'])

    print(f'Сменили фон на: {selected_image}')
else:
    print('Нет изображений в директории.')
