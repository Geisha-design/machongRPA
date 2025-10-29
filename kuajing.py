import json
import time
import anyconfig
import pika
from loguru import logger
from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import random

# {"invoiceNo": "17772"}

# 到时候专门存一个配置文件 地址
def baseConfig(divide,key):
    yaml_config = anyconfig.load('./element_kuajing.yaml', ac_parser="yaml", encodings='gbk')
    return yaml_config.get(divide).get(key)

# company_name = baseConfig('config','company_name')
ebao_mq_ip = baseConfig('config','mq_ip')
ebao_mq_vhost = baseConfig('config','mq_vhost')
ebao_mq_port = baseConfig('config','mq_port')
mq_queue_name = baseConfig('config','queue_name')
ebao_mq_user = baseConfig('config','mq_user')
ebao_mq_password = baseConfig('config','mq_password')
theheadless = baseConfig('config','headless')

def get_release_messages(channel):
    mq_queue_name =  baseConfig('config', 'queue_name')
    msg = ''
    msg_count = 0
    method_frame, header_frame, body = channel.basic_get(mq_queue_name)
    if method_frame:
        # logger.info(method_frame+header_frame+body)
        # 本次请求编号
        delivery_tag = method_frame.delivery_tag
        # 本次获取完毕剩余的个数(不包含本条)
        msg_count = method_frame.message_count
        logger.info('剩余未执行指令数量：',msg_count)
        # 获得的数据
        msg = body.decode()
        logger.info('获取的指令：' + msg)
        # 提交本次响应结果
        channel.basic_ack(delivery_tag)
    else:
        # logger.info('暂无未执行的指令')
        msg_count = -1
    return msg,msg_count



def establish_connection():
    ebao_mq_ip = baseConfig('config', 'mq_ip')
    ebao_mq_vhost = baseConfig('config', 'mq_vhost')
    ebao_mq_port = baseConfig('config', 'mq_port')
    ebao_mq_user = baseConfig('config', 'mq_user')
    ebao_mq_password = baseConfig('config', 'mq_password')

    # ########################## consumer ##########################
    credentials = pika.PlainCredentials(ebao_mq_user, ebao_mq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(ebao_mq_ip, ebao_mq_port, ebao_mq_vhost, credentials))
    channel = connection.channel()

    msg,msg_count = get_release_messages(channel)
    if(msg == '' or msg_count == -1 or msg_count is None):
        #logger.info("没有消息")
        return channel, msg
    # 在此处开始编写您的应用
    if (msg != '' and msg_count != -1 and msg_count is not None):
        # 只有有数据的时候才做浏览器数据的初始化
        try:
            print(msg)
            CR(channel,msg)
        except Exception as e:
            print(e)
            # 构建最终返回的JSON结构

            jsonreturn = {
                "invoiceNo": invoiceNo,
                "invoiceResult": "ERROR"
            }
            # 消息队列回推消息 json.dumps(main_card_msg, ensure_ascii=False)
            # logger.info("输出异常事件回传消息")
            logger.info(jsonreturn)
            channel.queue_declare(queue='taxes.result.queue', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key="taxes.result.queue",
                body=json.dumps(jsonreturn, ensure_ascii=False),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 使消息持久化
                ))
            # send_alarm_msg("出现了规划之外的异常，请人工检测"+str(e))
            # 这里增加一个邮件提示模块
    return channel, msg


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

def CR(channel,msg):
    result = json.loads(msg)
    invoiceNo = result["invoiceNo"]
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get('https://portaltica.hacienda.go.cr/TicaExterno/hcitelelog.aspx')
    # https: // portaltica.hacienda.go.cr / TicaExterno / hcitelelog.aspx
    randomSleep()
    # page.run_js('document.readyState === "complete"')
    page.ele('xpath://*[@id="vAGENTE"]').input('310111982920')
    page.ele('xpath://*[@id="vNUME_ORDEN"]').input(invoiceNo)
    page.ele('xpath://*[@id="TABLE3"]/tbody/tr/td[1]/input').click()
    # 等待页面 readyState 为 complete
    randomSleep()
    # page.run_js('document.readyState === "complete"')
    urllist = []
    # 然后获取元素
    bodyele = page.ele('xpath://*[@id="Subfile1ContainerTbl"]/tbody', timeout=10)
    countflag = trNum(bodyele)
    for i in range(1, countflag+1):
        # 格式化数字为4位数，前面补0
        formatted_i = f"{i:04d}"
        element = page.ele(f'xpath://*[@id="span_TELNUME_CORRE_{formatted_i}"]/a')
        url = element.attr("href")
        print(url)
        # // *[ @ id = "span_TELNUME_CORRE_0264"] / a //*[@id="Subfile1ContainerRow_0014"]  //*[@id="Subfile1ContainerRow_0001"]
        elementname = page.ele(f'xpath://*[@id="span_TELNUME_CORRE_{formatted_i}"]/a').text
        print(elementname)

        if elementname != '':
            urllist.append(url)
    print(urllist)
    if len(urllist) >= 1:
        print("存在数据")
        thesingle = urllist[0]
        page.get(thesingle)
        fetch_bill_of_lading_data(page,channel,invoiceNo)
    else:
        print("不存在数据")

        # 构建最终返回的JSON结构
        jsonreturn = {
            "invoiceNo": invoiceNo,
            "invoiceResult": None
        }
        print("最终数据:", jsonreturn)

        # 消息队列回推消息 json.dumps(main_card_msg, ensure_ascii=False)
        # logger.info("输出异常事件回传消息")
        logger.info(jsonreturn)
        channel.queue_declare(queue='taxes.result.queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key="taxes.result.queue",
            body=json.dumps(jsonreturn, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 使消息持久化
            ))





    return page




def fetch_bill_of_lading_data(page,channel,invoiceNo):
    print("进行数据抓取")
    randomSleep()
    page.ele('xpath://*[@id="TABLE3"]/tbody/tr[2]/td[4]/input').click()
    randomSleep()
    tax_data = {
        "arancelarios": "",
        "sobre": "",
        "selectivo": "",
        "procomer": "",
        "archivo": "",
        "asociacion": "",
        "contadores": "",
        "Ley6946": ""

    }

    finalbodyelement = page.ele('xpath://*[@id="Sftributos1ContainerTbl"]/tbody')

    # 获取所有的 tr 元素
    tr_elements = finalbodyelement.eles('tag:tr')

    # 定义税种映射关系
    tax_mapping = {
        'DERECHOS ARANCELARIOS A LA IMPORTACIÓN (DAI)': 'arancelarios',
        'IMPUESTO SOBRE EL VALOR AGREGADO. LEY 9635': 'sobre',
        'IMPUESTO SELECTIVO DE CONSUMO (S.C.)': 'selectivo',
        '$ 3 PROCOMER': 'procomer',
        'TIMBRE ARCHIVO NACIONAL': 'archivo',
        'TIMBRE ASOCIACION AGENTES DE ADUANA LEY 7017': 'asociacion',
        'TIMBRE CONTADORES PRIVADOS DE COSTA RICA': 'contadores',
        'LEY 6946': 'Ley6946'
    }


    # 遍历每一行数据
    for index, tr_element in enumerate(tr_elements):
        # 获取该行的所有 td 元素文本
        td_elements = tr_element.eles('tag:td')
        td_texts = [td.text for td in td_elements]

        if len(td_texts) >= 6:
            # 获取税种名称（倒数第二个元素）和金额（最后一个元素）
            tax_name = td_texts[-2]
            tax_amount = td_texts[-1]

            print(f"税种: {tax_name}, 金额: {tax_amount}")

            # 根据税种名称映射到对应的字段
            if tax_name in tax_mapping:
                field_name = tax_mapping[tax_name]
                tax_data[field_name] = tax_amount



    # 构建最终返回的JSON结构
    jsonreturn = {
        "invoiceNo": invoiceNo,
        "invoiceResult": tax_data
    }
    print("最终数据:", jsonreturn)



    # 消息队列回推消息 json.dumps(main_card_msg, ensure_ascii=False)
    # logger.info("输出异常事件回传消息")
    logger.info(jsonreturn)
    channel.queue_declare(queue='taxes.result.queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key="taxes.result.queue",
        body=json.dumps(jsonreturn, ensure_ascii=False),
        properties=pika.BasicProperties(
            delivery_mode=2,  # 使消息持久化
        ))








    return jsonreturn

# {
#   "invoiceNo": "172745"
# }



if __name__ == '__main__':
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    logger.add("跨境-logs/" + f'{today}.log', rotation="1000 MB")
    logger.info("开始执行跨境税单RPA机器人")
    invoiceNo =  ""
    channel, msg = establish_connection()
    while True:
        try:
            channel,msg =establish_connection()
            logger.complete()
        except Exception as e:
            logger.error(e)
            logger.complete()
            pass
        time.sleep(4)



    # page = CR()



