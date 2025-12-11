from DrissionPage import WebPage, ChromiumOptions, SessionOptions
from AOSCCOCR import *
import AOSCCOCR
import json
import time
import requests
from loguru import logger
from rpacapture import *




if theheadless == 'false' or theheadless == 'False':
    co = ChromiumOptions()
else:
    co = ChromiumOptions().headless()
so = SessionOptions()
page = WebPage(chromium_options=co, session_or_options=so)
if theheadless == 'false' or theheadless == 'False':
    logger.info("进入目标网址(有头模式)" + "https://xb-node.amazon.cn/")
else:
    logger.info("进入目标网址(无头模式)" + "https://xb-node.amazon.cn/")
page.get('https://xb-node.amazon.cn/')
logger.info('第一次cookie状态检测')
# cookiea = page.cookies(as_dict=True)
cookiea = page.cookies()