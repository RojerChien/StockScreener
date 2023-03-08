from PIL import Image
import glob
import os

# 設置每行顯示6張圖片，計算列數
images_per_row = 6
width_resolution = 1080
height_resolution = int(width_resolution * 0.56)

# 找到所有*date.jpg文件
date = "2023-03-09"
image_list = glob.glob(f"*{date}.jpg")

# 將圖像列表分成多個列表
num_images_per_list = 636  # 每個列表中包含100個圖像
image_lists = [image_list[i:i+num_images_per_list] for i in range(0, len(image_list), num_images_per_list)]

# 遍歷每個圖像列表
for i, image_list in enumerate(image_lists):
    # 計算輸出圖像大小和行數
    num_rows = len(image_list) // images_per_row + (1 if len(image_list) % images_per_row else 0)
    output_width = images_per_row * width_resolution
    output_height = num_rows * height_resolution
    # 創建一個空白的輸出圖像
    output_image = Image.new('RGB', (output_width, output_height))
    # 將所有圖像合併到輸出圖像中
    for j, image_path in enumerate(image_list):
        # 打開圖像
        image = Image.open(image_path)
        # 計算該圖像的位置
        row = j // images_per_row
        col = j % images_per_row
        x = col * width_resolution
        y = row * height_resolution
        # 將圖像貼到輸出圖像中
        output_image.paste(image, (x, y))
    # 將輸出圖像保存為文件
    output_image.save(f"merged_{i}_{date}.png")






"""
from PIL import Image
import glob

# 設置每行顯示6張圖片，計算列數
images_per_row = 6
width_resolution = 1080
height_resolution = int(width_resolution * 0.56)

# 找到所有*date.jpg文件
date = "2023-03-08"
image_list = glob.glob(f"*{date}.jpg")

num_rows = len(image_list) // images_per_row + (1 if len(image_list) % images_per_row else 0)

# 設置輸出圖像大小
output_width = images_per_row * width_resolution  # 6張圖片，每張圖片寬度為200像素
output_height = num_rows * height_resolution

# 創建一個空白的輸出圖像
output_image = Image.new('RGB', (output_width, output_height))

# 將所有圖像合併到輸出圖像中
for i, image_path in enumerate(image_list):
    # 打開圖像
    image = Image.open(image_path)
    # 計算該圖像的位置
    row = i // images_per_row
    col = i % images_per_row
    x = col * width_resolution
    y = row * height_resolution
    # 將圖像貼到輸出圖像中
    output_image.paste(image, (x, y))

# 將輸出圖像保存為文件
output_image.save("output.png")"""




"""from PIL import Image

# 這裡是您想要合併的PNG圖像的檔名清單
image_files = ['83.jpg', '313.jpg', '722.jpg', '723.jpg', '838.jpg', '1050.jpg', '1216.jpg', '1607.jpg', '1741.jpg', '2059.jpg']

# 打開第一張圖像，並獲取其寬度和高度
with Image.open(image_files[0]) as im:
    width, height = im.size

# 建立一個新的空白圖像，其大小足以容納所有圖像
new_image = Image.new('RGBA', (width * 4, height * 3))

# 逐一貼上所有圖像
for i in range(len(image_files)):
    with Image.open(image_files[i]) as im:
        x = i % 4  # 計算此圖像應該放在第幾行第幾列
        y = i // 4
        new_image.paste(im, (x * width, y * height))

# 儲存新的合併圖像
new_image.save('merged_image.png')
"""

