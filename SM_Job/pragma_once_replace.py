import os
import re

if __name__ == "__main__":
    old_path = r"E:\\RD\\GraphicsComponent_QtExample_1118"
    ends_str = ".h"
    old_str = "#pragma once"


    is_replace = False

    for root, dirs, files in os.walk(old_path):

        for file_name in files:
            file_path = f'{root}/{file_name}'

            fn = file_name.split('.')[0].upper()
            new_str = f"#ifndef {fn}_H_\n#define {fn}_H_\n"
            end_str = f"\n#endif //{fn}_H_\n"

            if file_path.endswith(ends_str):
                print(f"正在处理 {file_name}")

                f = open(file_path, 'r', encoding='UTF-8')
                all_lines = f.readlines()
                f.close()

                temp_list = list(filter(lambda x: old_str in x, all_lines))
                if len(temp_list) > 0:
                    all_lines.append(end_str)

                f = open(file_path, 'w+', encoding='UTF-8')
                for each_line in all_lines:
                    a = re.sub(old_str, new_str, each_line)
                    f.writelines(a)
                f.close()
    print('完毕')
