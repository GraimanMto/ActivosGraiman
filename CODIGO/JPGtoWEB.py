from PIL import Image
import os

input_folder = 'imagenes_originales'
output_folder = 'imagenes_convertidas'

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, base_name + '.webp')

        img.save(output_path, 'webp')
        print(f'Convertido: {filename} -> {base_name}.webp')
