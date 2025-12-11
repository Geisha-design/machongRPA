import random
import os
import time

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

def setup_download_directory(download_path):
    """设置下载目录"""
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path


def click_element_to_download(page, element_xpath):
    """点击元素触发下载"""
    try:
        # 定位下载元素
        download_element = page.ele(f'xpath://{element_xpath}')
        if download_element:
            # 点击触发下载
            download_element.click()
            print(f"已点击元素: {element_xpath}")
            return True
        else:
            print(f"未找到元素: {element_xpath}")
            return False
    except Exception as e:
        print(f"点击元素时出错: {e}")
        return False

def wait_for_download_complete(download_path, timeout=60):
    """等待下载完成"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        # 检查是否有Chrome下载临时文件
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload')]
        if not downloading_files:
            # 检查是否有Firefox下载临时文件
            part_files = [f for f in os.listdir(download_path) if f.endswith('.part')]
            if not part_files:
                break
        time.sleep(1)
    print("下载完成或超时")
# def google():
#     co = ChromiumOptions()
#     co.existing_only(False)
#     # co = ChromiumOptions().headless()
#     so = SessionOptions()
#     page = WebPage(chromium_options=co, session_or_options=so)
#     page.get('https://drive.google.com/drive/folders/10vTzaFJ4vCn1XJWMfD7W8xaRfURsZl3w?q=after:2025-10-15%20parent:10vTzaFJ4vCn1XJWMfD7W8xaRfURsZl3w')
#     bodyele = page.ele('xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody')
#     countflag = trNum(bodyele)
#     # 核心获取data-id 这个主要元素
#     # 存储所有链接的列表
#     links = []
#     for i in range(1, countflag+1):
#         # 格式化数字为4位数，前面补0
#         # formatted_i = f"{i:04d}"
#         print("获取第 {i} 个元素"+str(i))
#         # print(i)
#         element = page.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]')
#         url = element.attr("data-id")
#         print(url)
#         print(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]')
#         newlink = 'https://drive.google.com/drive/folders/' + url
#
#         # 存储链接
#         links.append(newlink)
#     page.quit()
#
#
#     # 依次访问所有链接并抓取数据
#     if links:
#         print(f"共找到 {len(links)} 个链接，开始依次访问...")
#         scraped_data = visit_and_scrape_links(links)
#
#         # 输出抓取结果
#         print("抓取结果:")
#         for data in scraped_data:
#             print(data)
#
#         return scraped_data
#     else:
#         print("未找到任何链接")
#         return []
#
#     return page
