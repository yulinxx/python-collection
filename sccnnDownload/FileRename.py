import os
import shutil


def is_shortcut(file_path):
    # 判断文件是否是快捷方式
    return os.path.islink(file_path)


def is_small_file(file_path, size_limit_kb=2):
    # 判断文件大小是否小于指定大小限制，默认为2K
    return os.path.getsize(file_path) < size_limit_kb * 1024


def move_files(from_folder, to_folder, file_name):
    # 复制子文件夹的文件到目标路径
    for root, dirs, files in os.walk(from_folder):
        for file in files:
            source_path = os.path.join(root, file)

            # 构建目标文件路径为第一级子文件夹的上一级目录，并在文件名前添加第一级子文件夹的名称
            target_path = os.path.join(to_folder, f"{file_name}_{file}")

            # 判断文件是否是快捷方式或大小小于2K
            if is_shortcut(source_path) or is_small_file(source_path):
                try:
                    os.remove(source_path)  # 尝试删除文件
                    print(f"Deleted: {source_path}")
                except Exception as e:
                    print(f"Error deleting {source_path}: {e}")

                print(f"Deleted: {source_path}")
            else:
                try:
                    shutil.move(source_path, target_path)  # 使用shutil.move移动文件
                    print(f"Moved: {source_path} to {target_path}")
                except Exception as e:
                    print(f"Error moving {source_path} to {target_path}: {e}")

def move_and_rename_files(main_folder):
    # 获取主文件夹下的所有子文件夹
    sub_folders = [f.path for f in os.scandir(main_folder) if f.is_dir()]

    for sub_a_folder in sub_folders:  # 第一级目录

        # 获取用于命名的文件夹的名称，即第一级目录的文件夹名称
        folder_name = os.path.basename(sub_a_folder)

        # ***************************************

        # ***************************************
        # 构建目标路径为第一级子文件夹的上一级目录
        target_folder = os.path.dirname(sub_a_folder)

        move_files(sub_a_folder, target_folder, folder_name)

        # 获取子文件夹下的所有子文件夹
        sub_b_folders = [f.path for f in os.scandir(sub_a_folder) if f.is_dir()]

        for last_folder in sub_b_folders:  # 第二级目录
            # 获取最终子文件夹的名称
            final_folder_name = os.path.basename(last_folder)

            # 复制子文件夹的文件到目标路径
            move_files(last_folder, target_folder, folder_name)


# 删除空文件夹
def delete_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # 使用topdown=False确保我们从底层向上遍历，以便先处理子文件夹
        for folder in dirs:
            current_folder = os.path.join(root, folder)
            if not os.listdir(current_folder):
                try:
                    os.rmdir(current_folder)
                    print(f"Deleted empty folder: {current_folder}")
                except Exception as e:
                    print(f"Error deleting folder {current_folder}: {e}")


if __name__ == "__main__":
    main_folder = "D:/xx/Pictures/Matter/M"
    move_and_rename_files(main_folder)
    delete_empty_folders(main_folder)
