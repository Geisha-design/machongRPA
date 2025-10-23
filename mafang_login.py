import json
import time
import requests
from loguru import logger
from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import random
from datetime import datetime
import concurrent.futures
from threading import Lock
import html
import AOSCCOCR


def randomSleep():
    # Set random sleep time, range from min_seconds to max_seconds, integer seconds
    min_seconds = 1
    max_seconds = 3
    # Generate a random integer representing sleep time (seconds)
    sleep_time = random.randint(min_seconds, max_seconds)
    print(f"Randomly selected sleep time: {sleep_time} seconds")
    # Let the program sleep for this random time
    time.sleep(sleep_time)
def rpapageshadow():
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get('https://www.nbsinglewindow.cn/user/login.do')
    logger.info('第一次cookie状态检测')
    cookiea = page.cookies()
    dictionary = {cookie['name']: cookie['value'] for cookie in cookiea}
    cookiea = dictionary
    logger.info(cookiea)
    logger.info('Login status A')
    logger.info(cookiea.get('eporttoken'))
    if cookiea.get('eporttoken1') is None:
        page.ele('xpath://*[@id="userId"]').input('nbfar')
        randomSleep()
        page.ele('xpath://*[@id="userPassword"]').input('nbfar666')
        randomSleep()

        # Call AOSCC OCR recognition mode start
        page.ele('xpath://*[@id="certificationCodeImg"]').get_screenshot('thescreen.png')
        randomSleep()
        # OCR recognition module
        with open("thescreen.png", 'rb') as f:
            img_bytes = f.read()
        ocr = AOSCCOCR.AosccOcr()
        poses = ocr.classification(img_bytes)
        logger.info(poses)
        # Call AOSCC OCR recognition mode end

        page.ele('xpath://*[@id="certificationCode"]').input(poses)
        # This button tag is for stability and security considerations, will be replaced with point-control button later
        randomSleep()
        page.ele('xpath://html/body/div[2]/div[2]/a[1]').click()
        randomSleep()

    logger.info('Second cookie status detection')
    cookieb = page.cookies()
    dictionary = {cookie['name']: cookie['value'] for cookie in cookieb}
    cookieb = dictionary
    logger.info(cookieb)
    logger.info('Login status B')
    logger.info(cookieb.get('eporttoken'))


    page.get('https://www.nbsinglewindow.cn/user/login.do?redirectURL=http%3A%2F%2Fp.nbsinglewindow.cn%2Fmember%2Freleaseinfo%2Freleaseinfo%21allquery.do')
    return page




def fetch_bill_of_lading_data():
    pass




if __name__ == '__main__':
    page = rpapageshadow()