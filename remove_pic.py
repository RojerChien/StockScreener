import os
import glob

# 获取当前工作目录
dir_path = os.getcwd()

# 查找所有.jpg文件
#pg_files = glob.glob(os.path.join(dir_path, "*.jpg"))
image_files = glob.glob(os.path.join(dir_path, "*.[jp][pn]g"))
# 删除所有.jpg文件
for image_file in image_files:
    os.remove(image_file)

print("All image files have been deleted.")