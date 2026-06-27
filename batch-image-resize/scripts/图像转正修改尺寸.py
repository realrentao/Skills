# %%
from PIL import Image

import os


def adjust_image_orientation(image_path):
    """
    根据EXIF信息中的Orientation标签调整图片方向
    """
    img = Image.open(image_path)
    try:
        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(274)  # 使用 get() 方法以避免 KeyError
            # 根据 Orientation 值调整图片
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 4:
                img = img.rotate(180, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
 
        # 保存调整后的图片覆盖原文件
        img.save(image_path)
    except (AttributeError, KeyError, IndexError, IOError) as e:
        print(f"Error processing {image_path}: {e}")

def batch_adjust_images(folder_path):
    """
    批量调整指定文件夹内所有图片的方向
    """
    for filename in os.listdir(folder_path):
        # 检查文件扩展名
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            adjust_image_orientation(image_path)
            print(f"Adjusted {image_path}")

def resize_images(target_folder, target_width):
    """
    调整文件夹中所有图片的宽度
    """
    for filename in os.listdir(target_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # 检查文件扩展名
            img_path = os.path.join(target_folder, filename)
            with Image.open(img_path) as img:
                # 计算新的尺寸
                w_percent = (target_width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))

                # 等比例缩放图片
                img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)

                # 保存图片，覆盖原图
                img.save(img_path)
                print(f'Resized {filename} to {target_width}x{h_size}')

# 使用示例
folder_path = 'D:\\BaiduNetdiskDownload'  # 修改为你的图片文件夹路径
batch_adjust_images(folder_path)

# 指定目标宽度并调整图片尺寸
target_width = 1080  # 你希望图片缩放后的新宽度
resize_images(folder_path, target_width)

print('All images have been resized.')