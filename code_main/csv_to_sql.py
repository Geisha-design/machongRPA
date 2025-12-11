import csv
import os
import sys
import re

def get_csv_reader(file_path):
    """
    尝试用不同编码方式打开CSV文件并返回reader对象
    
    Args:
        file_path (str): CSV文件路径
        
    Returns:
        tuple: (file_object, csv_reader, encoding_used)
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            csvfile = open(file_path, 'r', encoding=encoding)
            reader = csv.reader(csvfile)
            # 测试读取第一行
            next(reader)
            # 重新打开文件以确保从头开始读取
            csvfile.close()
            csvfile = open(file_path, 'r', encoding=encoding)
            reader = csv.reader(csvfile)
            return csvfile, reader, encoding
        except UnicodeDecodeError:
            continue
        except StopIteration:
            # 文件为空，重新打开
            csvfile.close()
            csvfile = open(file_path, 'r', encoding=encoding)
            reader = csv.reader(csvfile)
            return csvfile, reader, encoding
    
    raise Exception(f"无法使用常见编码格式读取文件: {file_path}")

def sanitize_table_name(filename):
    """
    将文件名转换为合法的表名
    
    Args:
        filename (str): 原始文件名
        
    Returns:
        str: 合法的表名
    """
    # 移除文件扩展名
    table_name = os.path.splitext(filename)[0]
    # 将非字母数字字符替换为下划线
    table_name = re.sub(r'[^a-zA-Z0-9_]', '_', table_name)
    # 如果表名以数字开头，添加前缀
    if table_name[0].isdigit():
        table_name = 'table_' + table_name
    # 转换为小写
    table_name = table_name.lower()
    return table_name

def csv_to_sql(input_file, output_file):
    """
    将CSV文件转换为SQL文件
    
    Args:
        input_file (str): 输入的CSV文件路径
        output_file (str): 输出的SQL文件路径
    """
    csvfile = None
    try:
        # 获取表名
        table_name = sanitize_table_name(os.path.basename(input_file))
        
        # 尝试多种编码方式打开文件
        csvfile, reader, encoding_used = get_csv_reader(input_file)
        print(f"使用 {encoding_used} 编码读取文件 '{input_file}'")
        
        # 读取标题行作为列名
        try:
            headers = next(reader)
        except StopIteration:
            print(f"警告: 文件 '{input_file}' 为空")
            return
            
        # 清理列名，确保它们是合法的SQL列名
        cleaned_headers = []
        for header in headers:
            # 移除非字母数字字符，只保留字母、数字和下划线
            cleaned_header = re.sub(r'[^a-zA-Z0-9_]', '_', header)
            # 如果列名以数字开头，添加前缀
            if cleaned_header and cleaned_header[0].isdigit():
                cleaned_header = 'col_' + cleaned_header
            # 如果列名为空，使用默认名称
            if not cleaned_header:
                cleaned_header = 'col'
            cleaned_headers.append(cleaned_header)
            
        # 写入SQL文件
        with open(output_file, 'w', encoding='utf-8') as sqlfile:
            # 写入创建表语句
            sqlfile.write(f"-- 创建表 {table_name}\n")
            sqlfile.write(f"CREATE TABLE {table_name} (\n")
                
            # 为每个列添加定义（这里假设所有列都是VARCHAR类型）
            columns_def = []
            for header in cleaned_headers:
                columns_def.append(f"  {header} VARCHAR(255)")
                
            sqlfile.write(",\n".join(columns_def))
            sqlfile.write("\n);\n\n")
                
            # 写入插入数据语句
            for row in reader:
                # 确保行数据与列数匹配
                if len(row) < len(cleaned_headers):
                    # 如果行数据列数不足，补充空值
                    row.extend([''] * (len(cleaned_headers) - len(row)))
                elif len(row) > len(cleaned_headers):
                    # 如果行数据列数过多，截断
                    row = row[:len(cleaned_headers)]
                    
                # 处理特殊字符，如单引号
                escaped_values = []
                for value in row:
                    # 转义单引号
                    escaped_value = value.replace("'", "''")
                    escaped_values.append(f"'{escaped_value}'")
                    
                values_str = ", ".join(escaped_values)
                sqlfile.write(f"INSERT INTO {table_name} ({', '.join(cleaned_headers)}) VALUES ({values_str});\n")
        
        print(f"已成功将 '{input_file}' 转换为 '{output_file}'")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{input_file}'")
    except Exception as e:
        print(f"处理文件 '{input_file}' 时出错: {e}")
    finally:
        if csvfile and not csvfile.closed:
            csvfile.close()

def convert_csv_files_in_directory(input_directory, output_directory):
    """
    将指定目录下的所有CSV文件转换为SQL文件
    
    Args:
        input_directory (str): 包含CSV文件的输入目录
        output_directory (str): 存储SQL文件的输出目录
    """
    # 检查输入目录是否存在
    if not os.path.exists(input_directory):
        print(f"错误: 输入目录 '{input_directory}' 不存在")
        return
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)
    
    # 遍历输入目录中的所有文件
    file_count = 0
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename[:-4] + '.sql')
            try:
                csv_to_sql(input_file, output_file)
                file_count += 1
            except Exception as e:
                print(f"跳过文件 '{input_file}': {e}")
    
    if file_count > 0:
        print(f"成功转换 {file_count} 个CSV文件")
    else:
        print(f"在目录 '{input_directory}' 中未找到CSV文件")

def main():
    """
    主函数，处理命令行参数
    """
    if len(sys.argv) < 2:
        print("用法: python csv_to_sql.py <CSV文件目录> [输出目录]")
        print("示例: python csv_to_sql.py ./csv_files ./saika")
        print("      python csv_to_sql.py ./csv_files  # 默认输出到saika文件夹")
        return
    
    input_directory = sys.argv[1]
    
    # 如果提供了输出目录参数，则使用它，否则默认为saika
    if len(sys.argv) > 2:
        output_directory = sys.argv[2]
    else:
        output_directory = 'saika'
    
    print(f"开始转换 '{input_directory}' 目录下的CSV文件...")
    print(f"SQL文件将保存到 '{output_directory}' 目录")
    convert_csv_files_in_directory(input_directory, output_directory)

if __name__ == "__main__":
    main()