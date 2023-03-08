import os
import glob

# 获取当前工作目录
dir_path = os.getcwd()

# 查找所有.jpg文件
jpg_files = glob.glob(os.path.join(dir_path, "*.jpg"))

# 删除所有.jpg文件
for jpg_file in jpg_files:
    os.remove(jpg_file)

print("All .jpg files have been deleted.")