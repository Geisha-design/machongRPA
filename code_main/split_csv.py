import csv
import os
import sys

def split_csv(input_file, max_rows=10000):
    """
    将CSV文件拆分为多个文件，每个文件最多max_rows行
    
    Args:
        input_file (str): 输入的CSV文件路径
        max_rows (int): 每个拆分文件的最大行数，默认为10000
    """
    try:
        # 获取文件名（不含扩展名）
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        file_dir = os.path.dirname(input_file)
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            # 读取标题行（如果存在）
            try:
                header = next(reader)
                has_header = True
            except StopIteration:
                header = None
                has_header = False
            
            file_count = 1
            row_count = 0
            
            # 创建第一个输出文件
            output_file = os.path.join(file_dir, f"{file_name}_part{file_count}.csv")
            outfile = open(output_file, 'w', encoding='utf-8', newline='')
            writer = csv.writer(outfile)
            
            # 如果原文件有标题，则每个拆分文件都写入标题
            if has_header:
                writer.writerow(header)
                row_count = 1
            
            for row in reader:
                # 如果当前文件已达到最大行数，则创建新文件
                if row_count >= max_rows:
                    outfile.close()
                    file_count += 1
                    row_count = 0
                    
                    output_file = os.path.join(file_dir, f"{file_name}_part{file_count}.csv")
                    outfile = open(output_file, 'w', encoding='utf-8', newline='')
                    writer = csv.writer(outfile)
                    
                    # 如果原文件有标题，则每个拆分文件都写入标题
                    if has_header:
                        writer.writerow(header)
                        row_count = 1
                
                # 写入当前行
                writer.writerow(row)
                row_count += 1
            
            outfile.close()
            print(f"文件已成功拆分为 {file_count} 个部分")
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{input_file}'")
    except Exception as e:
        print(f"处理文件时出错: {e}")

def main():
    """
    主函数，处理命令行参数
    """
    if len(sys.argv) < 2:
        print("用法: python split_csv.py <csv文件路径> [每文件最大行数]")
        print("示例: python split_csv.py data.csv 10000")
        return
    
    input_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        return
    
    # 检查是否为CSV文件
    if not input_file.lower().endswith('.csv'):
        print("警告: 文件可能不是CSV格式")
    
    # 获取每文件最大行数参数，默认为10000
    max_rows = 10000
    if len(sys.argv) > 2:
        try:
            max_rows = int(sys.argv[2])
        except ValueError:
            print("警告: 行数参数无效，使用默认值10000")
    
    print(f"开始拆分文件 '{input_file}'，每文件最多 {max_rows} 行...")
    split_csv(input_file, max_rows)

if __name__ == "__main__":
    main()