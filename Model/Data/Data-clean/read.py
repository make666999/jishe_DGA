import os

def count_lines_in_directory(directory):
    total_lines = 0
    for filename in os.listdir(directory):
        # 拼接完整的文件路径
        path = os.path.join(directory, filename)
        # 确保这是一个文件而不是目录
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                total_lines += len(lines)
                print(f"{filename}: {len(lines)} 行")
    return total_lines

# 获取当前目录
current_directory = os.getcwd()
# 调用函数
total_lines = count_lines_in_directory(current_directory)
print(f"当前文件夹总行数：{total_lines}")
