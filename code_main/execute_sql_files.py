#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在指定服务器上依次执行SQL文件的脚本
"""

import sys
import os
import pymysql
from database_config import create_connection


def execute_sql_file(connection, file_path):
    """
    执行单个SQL文件
    
    Args:
        connection: 数据库连接对象
        file_path (str): SQL文件路径
        
    Returns:
        bool: 执行是否成功
    """
    if not os.path.exists(file_path):
        print(f"错误: SQL文件 '{file_path}' 不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句（按分号分割）
        sql_statements = sql_content.split(';')
        
        cursor = connection.cursor()
        executed_count = 0
        
        for statement in sql_statements:
            # 清理语句（去除首尾空白字符）
            statement = statement.strip()
            
            # 跳过空语句
            if not statement:
                continue
                
            try:
                cursor.execute(statement)
                executed_count += 1
            except Exception as e:
                print(f"执行SQL语句时出错: {e}")
                print(f"错误的SQL语句: {statement[:100]}...")
                connection.rollback()
                return False
        
        connection.commit()
        print(f"成功执行 '{file_path}' 中的 {executed_count} 条SQL语句")
        cursor.close()
        return True
        
    except Exception as e:
        print(f"读取或执行SQL文件 '{file_path}' 时出错: {e}")
        return False


def execute_sql_files(server_config, sql_files):
    """
    在指定服务器上依次执行SQL文件
    
    Args:
        server_config (dict): 服务器配置信息
        sql_files (list): SQL文件路径列表
        
    Returns:
        bool: 所有文件是否执行成功
    """
    # 创建数据库连接
    connection = create_connection()
    
    if connection is None:
        print("无法建立数据库连接")
        return False
    
    print(f"成功连接到数据库服务器")
    
    # 依次执行SQL文件
    success_count = 0
    for sql_file in sql_files:
        print(f"\n正在执行: {sql_file}")
        if execute_sql_file(connection, sql_file):
            success_count += 1
        else:
            print(f"执行 '{sql_file}' 失败")
    
    # 关闭数据库连接
    try:
        connection.close()
        print("\n数据库连接已关闭")
    except:
        pass
    
    total_files = len(sql_files)
    print(f"\n执行结果: {success_count}/{total_files} 个文件执行成功")
    
    return success_count == total_files


def main():
    """
    主函数，处理命令行参数
    """
    if len(sys.argv) < 2:
        print("用法: python execute_sql_files.py <SQL文件1> [SQL文件2] [SQL文件3] ...")
        print("示例: python execute_sql_files.py ./saika/table1.sql ./saika/table2.sql")
        return
    
    # 获取SQL文件列表
    sql_files = sys.argv[1:]
    
    # 检查文件是否存在
    existing_files = []
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            existing_files.append(sql_file)
        else:
            print(f"警告: 文件 '{sql_file}' 不存在，将被跳过")
    
    if not existing_files:
        print("没有找到有效的SQL文件")
        return
    
    # 使用database_config.py中的配置执行SQL文件
    print("开始执行SQL文件...")
    success = execute_sql_files({}, existing_files)
    
    if success:
        print("\n所有SQL文件执行成功!")
    else:
        print("\n部分或全部SQL文件执行失败!")


if __name__ == "__main__":
    main()