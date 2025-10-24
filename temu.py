import json
import time
import anyconfig
import pika
from loguru import logger
from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import random
import requests
import json


def exist(element):
    if element.is_exists:
        print("元素存在")
        url = element.attr("href")
    else:
        print("元素不存在")

def trNum(ele):
    tbody_element = ele
    tr_count = len(tbody_element.eles('tag:tr'))  # 使用标签选择器
    print(f"tr元素数量: {tr_count}")
    return tr_count

def randomSleep():
    # Set random sleep time, range from min_seconds to max_seconds, integer seconds
    min_seconds = 3
    max_seconds = 5
    # Generate a random integer representing sleep time (seconds)
    sleep_time = random.randint(min_seconds, max_seconds)
    print(f"Randomly selected sleep time: {sleep_time} seconds")
    # Let the program sleep for this random time
    time.sleep(sleep_time)

def temu():
    # result = json.loads(msg)
    # invoiceNo = result["invoiceNo"]
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    # https: // logistics.temu.com / settlement / bill - preview / collect - taxes  https://logistics.temu.com/settlement/bill-preview/collect-taxes
    # page.get('https://logistics.temu.com/settlement/bill-preview/collect-taxes')
    page.get('https://logistics.temu.com/settlement/bill-preview/tail-bill')
    tab = page.latest_tab
    ele = tab('xpath://*[@id="bgb-overseas-logistics-settlement"]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div[2]/button')
    ele.click.to_upload('CR运费0.01更正.xlsx')



    # randomSleep() https://logistics.temu.com/settlement/bill-preview/collect-taxes
    # page.run_js('document.readyState === "complete"')

    # 后面自动化检测登陆状态
    # page.ele('xpath://*[@id="email"]/div/div/div/div/div/div/div/div[2]/input').input('qiyz@smartebao.com')
    # page.ele('xpath://*[@id="password"]/div/div/div/div/div/div/div/div[2]/input').input('yb123456.')
    # page.ele('xpath://*[@id="root"]/div/div/div/div[1]/div[2]/div[2]/form/div/div/div[4]/button').click()
    # 等待页面 readyState 为 complete
    randomSleep()
    return page


def check_task_status(cookies, task_id):
    """
    检查任务状态
    """
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }
    
    # 准备请求参数
    params = {
        "regionId": 49,
        "all": 1,
        "limit": 10,
        "pageNum": 1
    }
    
    try:
        response = requests.post(
            'https://logistics.temu.com/tms/thrall/package/bill/task/pageList',
            headers=headers,
            json=params
        )
        print(f"检查任务状态接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")
            # 解析回执的保文
            return parse_task_status(result)
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")
    
    return None


def parse_task_status(response_data):
    """
    解析任务状态
    """
    if not response_data.get("success"):
        print("接口调用失败")
        return None
    
    result = response_data.get("result", {})
    task_infos = result.get("taskInfos", [])
    
    if task_infos:
        # 获取第一个任务的状态
        task = task_infos[0]
        status_name = task.get("statusName")
        print(f"当前任务状态: {status_name}")
        return status_name
    
    return None


def CostaRicaFirst(file_name):
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get('https://logistics.temu.com/settlement/bill-preview/collect-taxes')
    page.ele('xpath://*[@id="__collect_taxes__"]/div[2]/div[1]/div[1]/div/div/div[2]').click()
    tab = page.latest_tab
    ele = tab('xpath://*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[4]/button')
    # ele.click.to_upload('EB-TEMU-CR-TAX202508-025 Tax Bill.xlsx')


    # 先检测是否已经上传好啦
    # 等待任务完成后再返回
    cookies = page.cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    while True:
        status = check_task_status(cookies, None)  # 这里可以传入具体的task_id
        if status and status == "完成":  # 当状态不再是"分析中"时，跳出循环
            print(f"任务状态已变为: {status}，继续执行下一步")
            break
        else:
            print("文件任务仍在上传中，等待5秒后重新检查...")
            time.sleep(15)  # 等待30秒后再次检查


    ele.click.to_upload(file_name)
    time.sleep(4)
    # 使用 requests 发送请求到 https://logistics.temu.com/tms/thrall/package/bill/task/pageList

    cookies = page.cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }
    
    # 准备请求参数
    params = {
        "regionId": 49,
        "all": 1,
        "limit": 10,
        "pageNum": 1
    }
    
    try:
        response = requests.post(
            'https://logistics.temu.com/tms/thrall/package/bill/task/pageList',
            headers=headers,
            json=params
        )
        print(f"接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")
            # 解析回执的保文
            parse_task_response(result)
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")
    
    # 等待任务完成后再返回
    while True:
        status = check_task_status(cookies, None)  # 这里可以传入具体的task_id
        if status and status == "完成":  # 当状态不再是"分析中"时，跳出循环
            print(f"任务状态已变为: {status}，继续执行下一步")
            break
        else:
            print("任务仍在分析中，等待8秒后重新检查...")
            time.sleep(8)  # 等待30秒后再次检查
    
    return page


def parse_task_response(response_data):
    """
    解析任务回执响应数据
    """
    if not response_data.get("success"):
        print("接口调用失败")
        return
    
    result = response_data.get("result", {})
    task_infos = result.get("taskInfos", [])
    
    print(f"\n=== 任务回执解析结果 ===")
    print(f"总任务数: {len(task_infos)}")
    
    for i, task in enumerate(task_infos):
        task_id = task.get("taskId")
        status_name = task.get("statusName")
        is_success = task.get("isSuccess")
        file_name = task.get("fileName")
        import_time = task.get("importTime")
        total_count = task.get("totalCount")
        success_lines = task.get("successLines")
        error_lines = task.get("errorLines")
        result_summary = task.get("resultSummary")
        
        print(f"\n--- 任务 {i+1} ---")
        print(f"任务ID: {task_id}")
        print(f"状态: {status_name}")
        print(f"是否成功: {'是' if is_success else '否'}")
        print(f"文件名: {file_name}")
        print(f"导入时间: {import_time}")
        print(f"总行数: {total_count}")
        print(f"成功行数: {success_lines}")
        print(f"错误行数: {error_lines}")
        print(f"结果摘要: {result_summary}")
        
        # 解析结果摘要中的详细错误信息
        try:
            summary_dict = json.loads(result_summary)
            print("详细错误信息:")
            for error_type, count in summary_dict.items():
                print(f"  {error_type}: {count} 条")
        except:
            print("无法解析详细错误信息")


def CostaRicaTwo(file_path):
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get('https://logistics.temu.com/settlement/bill-preview/collect-taxes')
    page.ele('xpath://*[@id="__collect_taxes__"]/div[2]/div[1]/div[1]/div/div/div[2]').click()
    tab = page.latest_tab
    ele = tab('xpath://*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/button')
    # ele.click.to_upload('145-90586963-提单Excel.xlsx')

    # 先检测是否已经上传好啦
    # 等待任务完成后再返回
    cookies = page.cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    while True:
        status = check_task_status(cookies, None)  # 这里可以传入具体的task_id
        if status and status == "完成":  # 当状态不再是"分析中"时，跳出循环
            print(f"任务状态已变为: {status}，继续执行下一步")
            break
        else:
            print("文件任务仍在上传中，等待5秒后重新检查...")
            time.sleep(5)  # 等待30秒后再次检查






    ele.click.to_upload(file_path)
    time.sleep(4)
    cookies = page.cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }

    # 准备请求参数
    params = {
        "regionId": 49,
        "all": 1,
        "limit": 10,
        "pageNum": 1
    }

    try:
        response = requests.post(
            'https://logistics.temu.com/tms/thrall/package/bill/task/pageList',
            headers=headers,
            json=params
        )
        print(f"接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")
            # 解析回执的保文
            parse_task_response(result)
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")

    # 等待任务完成后再返回
    while True:
        status = check_task_status(cookies, None)  # 这里可以传入具体的task_id
        if status and status == "完成":  # 当状态不再是"分析中"时，跳出循环
            print(f"任务状态已变为: {status}，继续执行下一步")
            break
        else:
            print("任务仍在分析中，等待30秒后重新检查...")
            time.sleep(15)  # 等待30秒后再次检查
    return page

# 税单凭证
def CostaRicaThree(file_path):
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get('https://logistics.temu.com/settlement/bill-preview/collect-taxes')
    page.ele('xpath://*[@id="__collect_taxes__"]/div[2]/div[1]/div[1]/div/div/div[2]').click()
    tab = page.latest_tab
    elev = tab('xpath://*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[6]/button')

    vvflag = page.ele('xpath://html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/button[2]/span',timeout=5)
    # //*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[6]/button/svg/use  判断是否存在 不存在就往下执行
    # //*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[6]/button/svg
    print('开始检测是否在加载中')
    print(vvflag.text)
    # time.sleep(400)
    elev.click.to_upload(file_path)
    time.sleep(4)
    while True:
        if vvflag:
            print("文件任务检测存在仍在上传中，等待30秒后重新检查...")
            time.sleep(30)
            vvflag = page.ele(
            'xpath://*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[6]/button/svg',timeout=5)
        else:
            print('加载元素不存在')
            # ele.click.to_upload(file_path)
            break

    # time.sleep(8)
    return page


# ele = tab.ele('****')#__collect_taxes__ > div.outerWrapper-1-2-1.outerWrapper-d5-1-2-7 > div.outerWrapper-1-2-1.outerWrapper-d12-1-2-14 > div > div.index-module__twfContainer___2j5P8.pc-easy-twf > div.index-module__operateArea___2Cpr8 > div > div > div > div:nth-child(8) > button > svg > use
#
# # 判断是否找到元素//*[@id="__collect_taxes__"]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[6]/button/svg/use
# if ele:
#     print('找到了。')
#
# if not ele:
#     print('没有找到。')


def fileStatus(page):
    # 使用 requests 发送请求到 https://logistics.temu.com/tms/thrall/package/bill/task/pageList

    cookies = page.cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }

    # 准备请求参数
    params = {
        "regionId": 49,
        "all": 1,
        "limit": 10,
        "pageNum": 1
    }

    try:
        response = requests.post(
            'https://logistics.temu.com/tms/thrall/package/bill/task/pageList',
            headers=headers,
            json=params
        )
        print(f"接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")
            # 解析回执的保文
            parse_task_response(result)
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")

import os
def get_files_from_directory(directory_path):
    """
    获取指定目录下所有文件的路径

    Args:
        directory_path (str): 目录路径

    Returns:
        list: 文件路径列表
    """
    file_paths = []

    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"目录 {directory_path} 不存在")
        return file_paths

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # 获取完整文件路径
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths

if __name__ == '__main__':
    # temu()
    # 获取所有文件
    # all_files = get_files_from_directory('/Users/qiyuzheng/Desktop/想送项目/ddtemu/qqq')
    # for file_path in all_files:
    #     print(file_path)
    #     CostaRicaFirst(file_path)
    #     time.sleep(15)

    # all_files = get_files_from_directory('/Users/qiyuzheng/Desktop/想送项目/ddtemu/td')
    # for file_path in all_files:
    #     print(file_path)
    #     CostaRicaTwo(file_path)
    #     time.sleep(10)
    #
    #
    all_files = get_files_from_directory('/Users/qiyuzheng/Desktop/想送项目/ddtemu/saika3')
    for file_path in all_files:
        print(file_path)
        CostaRicaThree(file_path)
        time.sleep(10)
    # # 只获取Excel文件
    # excel_files = get_files_from_directory_with_extension('/path/to/your/directory', '.xlsx')
    # for file_path in excel_files:
    #     print(file_path)


    # CostaRicaFirst(file_name='145-90586963-提单Excel.xlsx')
    # 现在CostaRicaFirst会自动等待任务完成后再继续
    # CostaRicaTwo()
    # 现在CostaRicaTwo会自动等待任务完成后再继续
    # CostaRicaThree()

# 哥斯达黎加流程 需要按照顺序来执行
