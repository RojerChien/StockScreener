import os
import glob

# 获取当前工作目录
dir_path = os.getcwd()

# 查找所有.jpg及.png文件
# pg_files = glob.glob(os.path.join(dir_path, "*.jpg"))
# image_files = glob.glob(os.path.join(dir_path, "*.[jp][pn]g"))
# image_files = glob.glob(os.path.join(dir_path, "*.html"))
remove_file_list = glob.glob(os.path.join(dir_path, "*.[jp][pn]g")) + glob.glob(os.path.join(dir_path, "*.html"))


# 删除所有.jpg文件
for image_file in remove_file_list:
    os.remove(image_file)

print("All image and html files have been deleted.")
