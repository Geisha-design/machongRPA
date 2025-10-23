import os
import time
import googletool
from DrissionPage import WebPage, ChromiumOptions, SessionOptions


def visit_and_scrape_links(links):
    """访问链接列表并抓取数据"""
    co = ChromiumOptions()
    co.existing_only(False)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)

    scraped_data = []

    for i, link in enumerate(links):
        try:
            print(f"正在访问第 {i + 1} 个链接: {link}")
            page.get(link)
            googletool.randomSleep()

            # 在这里添加你需要抓取的数据逻辑
            # 示例：抓取页面标题
            title = page.title
            print(f"页面标题: {title}")

            # 示例：抓取特定元素内容
            # 你可以根据实际需要修改这里的选择器和抓取逻辑
            try:
                # 添加你的数据抓取逻辑
                data = {
                    "url": link,
                    "title": title,
                    # "content": page.ele('xpath://*[@id="some-content"]').text
                }
                scraped_data.append(data)
            except Exception as e:
                print(f"抓取数据时出错: {e}")
                scraped_data.append({"url": link, "error": str(e)})

        except Exception as e:
            print(f"访问链接 {link} 时出错: {e}")
            scraped_data.append({"url": link, "error": str(e)})

    page.quit()
    return scraped_data





# 在您的主函数中使用
def enhanced_google_download():
    """增强的Google Drive下载功能"""
    # 设置下载路径
    download_folder = "/Users/qiyuzheng/Desktop/temu_files"

    # 获取链接的代码保持不变
    co = ChromiumOptions()
    co.existing_only(False)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get(
        'https://drive.google.com/drive/folders/10vTzaFJ4vCn1XJWMfD7W8xaRfURsZl3w?q=after:2025-10-15%20parent:10vTzaFJ4vCn1XJWMfD7W8xaRfURsZl3w')
    bodyele = page.ele('xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody')
    countflag = googletool.trNum(bodyele)

    # 存储所有链接和下载元素
    links = []
    download_xpaths = []

    for i in range(1, countflag + 1):
        print(f"获取第 {i} 个元素")
        element = page.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]')
        url = element.attr("data-id")
        print(url)
        newlink = 'https://drive.google.com/drive/folders/' + url
        links.append(newlink)

        # 假设下载按钮在同一行，可以根据实际页面结构调整
        # download_xpath = f'//*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]/td[5]/div/button'
        # download_xpaths.append(download_xpath)

    page.quit()

    # 执行下载
    if links:
        print(f"共找到 {len(links)} 个下载项，开始下载...")
        # 这里需要改为links的for循环
        downloaded_path = auto_download_with_drissionpage(
            'https://drive.google.com/drive/folders/1Y_4rx0vRedaJX0TFTYk8CgOCjYoBpOrG',
            download_folder
        )
        print(f"所有文件已下载到: {downloaded_path}")
    else:
        print("未找到任何下载项")


def auto_download_with_drissionpage(url, download_path):
    """使用DrissionPage自动下载文件"""
    # 创建下载目录
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # 配置浏览器
    co = setup_browser_for_download(download_path)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)

    try:
        # 访问页面
        page.get(url)
        time.sleep(3)  # 等待页面加载 //*[@id=":hg"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[2]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[3]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        tab = page.latest_tab

        # 设置下载路径（双重确认）
        tab.set.download_path(download_path)

        # 获取所有下载元素

        bodyele = page.ele('xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody')
        countflag = googletool.trNum(bodyele)
        print(f"内层文件tr元素数量: {countflag}")

        downloaded_files = []
        time.sleep(4)
        for i in range(1, countflag + 1):
            print(f"处理第 {i} 个文件")
            tab.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]/td[1]/div/div/div[2]/div/div[1]').click()
            # 点击下载按钮 //*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[2]/td[1]/div
            # tab.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}/td[5]/div/div/div[1]/drive-collection/div/div[2]').click
            download_btn = tab.ele(
                f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div')
            if download_btn:
                download_btn.click()


                ppflag = tab.ele('无法对文件进行病毒扫描')
                if ppflag:
                    print("存在pp")
                    tab.ele('仍然下载').click()
                    time.sleep(10)
                else:
                    print('执行常规的下载检测即可')
                    time.sleep(2)
                # 等待下载开始
            #     try:
            #         tab.wait.download_begin(timeout=30)
            #         mission = tab.wait.download_begin()
            #         while not mission.is_done:
            #             print(f'\r{mission.rate}%', end='')
            #
            #         # 获取下载文件信息
            #         download_item = tab.download_item()
            #         if download_item:
            #             file_name = download_item.name
            #             file_path = os.path.join(download_path, file_name)
            #
            #             # 等待下载完成
            #             tab.wait.downloads_done(timeout=60)
            #
            #             # 验证文件是否存在
            #             if os.path.exists(file_path):
            #                 downloaded_files.append(file_path)
            #                 print(f"成功下载: {file_name}")
            #             else:
            #                 print(f"下载失败: {file_name} 未找到")
            #         else:
            #             print("未检测到下载项")
            #
            #     except Exception as e:
            #         print(f"等待下载时出错: {e}")
            # else:
            #     print(f"第 {i} 个下载按钮未找到")

        # return downloaded_files

    finally:
        print(1)
        # page.quit()

        # 遍历并点击所有下载元素
        #
        # 每个 URL 链接都有三个指定的任务存在
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[2]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # //*[@id=":51"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[3]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div


        # //*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div
        # tab = page.latest_tab
        # tab.set.download_path('/Users/qiyuzheng/Desktop/temu_files')
        # tab.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div').click()  # 点击下载按钮
        # tab.wait.download_begin()  # 等待下载开始
        # tab.wait.downloads_done()
        # for i in range(1, countflag + 1):
        #     print(f"获取第 {i} 个元素")
        #     tab = page.latest_tab
        #     tab.set.download_path('/Users/qiyuzheng/Desktop/temu_files')
        #     tab.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[1]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div').click()



            # tab = page.latest_tab
            # tab.set.download_path('/Users/qiyuzheng/Desktop/temu_files')
            # tab.ele(f'xpath://*[@id=":a"]/div/c-wiz/div/div/c-wiz[2]/div/div/div[1]/table/tbody/tr[{i}]/td[5]/div/div/div[1]/drive-collection/div/div[2]/span/button/div').click()  # 点击下载按钮
            # tab.wait.download_begin()  # 等待下载开始
            # tab.wait.downloads_done()  # 等待所有任务结束


        # for i, xpath in enumerate(download_elements_xpath):
        #     print(f"正在处理第 {i + 1} 个下载任务")
        #     if click_element_to_download(page, xpath):
        #         # 等待下载完成
        #         wait_for_download_complete(download_path)
        #         print(f"第 {i + 1} 个文件下载完成")
        #     else:
        #         print(f"第 {i + 1} 个下载任务失败")

    # finally:
    #     print("下载任务完成")
    #     # page.quit()
    #
    # return download_path


def setup_browser_for_download(download_path):
    """配置浏览器下载设置"""
    co = ChromiumOptions()
    co.existing_only(False)
    # 设置下载路径和相关参数
    co.set_pref('download.default_directory', download_path)
    co.set_pref('download.prompt_for_download', False)  # 禁用下载前询问
    co.set_pref('download.directory_upgrade', True)
    co.set_pref('safebrowsing.enabled', True)
    return co





if __name__ == '__main__':
    # 定义下载文件夹路径
    # download_folder = "/Users/qiyuzheng/Desktop/temu_files"
    enhanced_google_download()
    # # 获取需要点击的坐标列表
    # coordinates_list = get_file_download_coordinates()
    #
    # # 执行自动下载
    # downloaded_path = auto_download_from_google_drive(coordinates_list, download_folder)
    # print(f"所有文件已下载到: {downloaded_path}")


    # google()


# 哥斯达黎加流程 需要按照顺序来执行
