import os
from pathlib import Path
import uuid

def rename_images(directory, dry_run=False):
    if not os.path.exists(directory):
        print(f"Ошибка: директория {directory} не существует!")
        return
    
    try:
        files = os.listdir(directory)
    except PermissionError:
        print(f"Ошибка: нет доступа к директории {directory}!")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    if not images:
        print("Нет изображений для переименования.")
        return
    
    images.sort()
    
    print(f"Найдено {len(images)} изображений. {'(Dry run)' if dry_run else ''}")
    
    for i, image in enumerate(images, start=1):
        old_path = os.path.join(directory, image)
        extension = os.path.splitext(image)[1]
        base_name = f"bg-{uuid.uuid4()}"
        new_name = f"{base_name}{extension}"
        new_path = os.path.join(directory, new_name)
        
        counter = 1
        while os.path.exists(new_path):
            new_name = f"{base_name}-{counter}{extension}"
            new_path = os.path.join(directory, new_name)
            counter += 1
        
        if dry_run:
            print(f"[Dry Run] Будет переименован: {old_path} -> {new_path}")
            continue
        
        try:
            os.rename(old_path, new_path)
            print(f"Успешно: {old_path} -> {new_path}")
        except PermissionError:
            print(f"Ошибка: нет прав для переименования {old_path}!")
        except Exception as e:
            print(f"Ошибка при переименовании {old_path}: {e}")

if __name__ == "__main__":
    directory = input("Напиши путь к каталогу обоев: ")
    
    rename_images(directory, dry_run=False)