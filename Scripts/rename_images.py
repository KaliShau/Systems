import os
from pathlib import Path

def rename_images(directory):
    # Получаем список всех файлов в директории
    files = os.listdir(directory)
    
    # Фильтруем только изображения
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    # Сортируем изображения по имени 
    images.sort()
    
    # Переименовываем изображения
    for i, image in enumerate(images, start=1):
        old_path = os.path.join(directory, image)
        extension = os.path.splitext(image)[1]
        new_name = f"bg-image-{i}{extension}"
        new_path = os.path.join(directory, new_name)
        
        # Переименовываем файл
        os.rename(old_path, new_path)
        print(f"Переименован: {old_path} -> {new_path}")

if __name__ == "__main__":
    # Укажите путь к директории с изображениями
    directory = "/home/Shau/.background"
    
    # Вызываем функцию для переименования
    rename_images(directory)