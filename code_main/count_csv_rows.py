import csv
import sys
import os

def count_csv_rows(file_path):
    """
    统计CSV文件的行数
    
    Args:
        file_path (str): CSV文件的路径
    
    Returns:
        int: 文件的行数（包括标题行）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用csv.reader来正确处理CSV格式
            reader = csv.reader(file)
            row_count = sum(1 for row in reader)
        return row_count
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def count_csv_rows_without_header(file_path):
    """
    统计CSV文件的数据行数（不包括标题行）
    
    Args:
        file_path (str): CSV文件的路径
    
    Returns:
        int: 数据行数（不包括标题行）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过标题行
            next(reader, None)
            row_count = sum(1 for row in reader)
        return row_count
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def main():
    """
    主函数，处理命令行参数并显示结果
    """
    if len(sys.argv) < 2:
        print("用法: python count_csv_rows.py <csv文件路径> [--no-header]")
        print("选项:")
        print("  --no-header  不包括标题行")
        return
    
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        return
    
    # 检查是否为CSV文件
    if not file_path.lower().endswith('.csv'):
        print("警告: 文件可能不是CSV格式")
    
    # 检查是否包含--no-header参数
    exclude_header = '--no-header' in sys.argv
    
    if exclude_header:
        row_count = count_csv_rows_without_header(file_path)
        if row_count is not None:
            print(f"文件 '{file_path}' 数据行数: {row_count}")
    else:
        row_count = count_csv_rows(file_path)
        if row_count is not None:
            print(f"文件 '{file_path}' 总行数: {row_count}")

if __name__ == "__main__":
    main()