# 解析JSON数据并存储到MySQL数据库
import json
from datetime import datetime
from database_config import create_connection, create_table

def parse_and_store_json(json_data):
    """
    解析JSON数据并存储到MySQL数据库
    """
    # 创建数据库连接
    connection = create_connection()
    if connection is None:
        print("无法建立数据库连接")
        return
    
    # 创建数据表
    create_table(connection)
    
    # 解析JSON数据
    try:
        data = json_data if isinstance(json_data, dict) else json.loads(json_data)
        
        if data.get('success') and 'resultData' in data and 'serviceData' in data['resultData']:
            service_data_list = data['resultData']['serviceData']
            
            # 插入数据到数据库
            insert_service_data(connection, service_data_list)
        else:
            print("JSON数据格式不正确或请求不成功")
            
    except json.JSONDecodeError as e:
        print(f"解析JSON数据时出错: {e}")
    except Exception as e:
        print(f"处理数据时出错: {e}")
    # finally:
    #     if connection.connected():
    #         connection.close()
    #         print("MySQL连接已关闭")

def convert_datetime_format(date_str):
    """
    转换日期时间格式
    """
    if date_str is None:
        return None
    try:
        # 将 "YYYY-MM-DD HH:MM:SS" 格式转换为datetime对象
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def insert_service_data(connection, service_data_list):
    """
    将服务数据插入到数据库中
    """
    cursor = connection.cursor()
    
    # 准备INSERT语句
    insert_query = '''
    INSERT INTO service_data (
        entityId, status, creatorCode, createTime, modifierCode, modifiedTime,
        clientCode, rateCardCode, itemCode, accountCode, businessType, chargeType,
        businessCode, referenceCode, logisticsCode, pl, categoryLevel1Code, 
        categoryLevel1Name, categoryLevel2Code, categoryLevel2Name, categoryCode,
        categoryName, settlementObjectCode, settlementObjectName, settleType,
        accountBrief, count, unitPrice, tradeUnit, amount, currency, billedAmount,
        billedCurrency, settlementAmount, settlementCurrency, accountCurrency,
        billNo, exchangeRate, myExchangeRate, note, attachment, itemStatus,
        tradeTime, auditor, auditTime, auditStatus, extData1, extData2, extData3,
        extData4, extData5, extNumber1, extNumber2, extNumber3, extNumber4,
        extNumber5, extDecimal1, extDecimal2, extDecimal3, extDecimal4, extDecimal5,
        orderAttribute
    ) VALUES (
        %(entityId)s, %(status)s, %(creatorCode)s, %(createTime)s, %(modifierCode)s, %(modifiedTime)s,
        %(clientCode)s, %(rateCardCode)s, %(itemCode)s, %(accountCode)s, %(businessType)s, %(chargeType)s,
        %(businessCode)s, %(referenceCode)s, %(logisticsCode)s, %(pl)s, %(categoryLevel1Code)s,
        %(categoryLevel1Name)s, %(categoryLevel2Code)s, %(categoryLevel2Name)s, %(categoryCode)s,
        %(categoryName)s, %(settlementObjectCode)s, %(settlementObjectName)s, %(settleType)s,
        %(accountBrief)s, %(count)s, %(unitPrice)s, %(tradeUnit)s, %(amount)s, %(currency)s, %(billedAmount)s,
        %(billedCurrency)s, %(settlementAmount)s, %(settlementCurrency)s, %(accountCurrency)s,
        %(billNo)s, %(exchangeRate)s, %(myExchangeRate)s, %(note)s, %(attachment)s, %(itemStatus)s,
        %(tradeTime)s, %(auditor)s, %(auditTime)s, %(auditStatus)s, %(extData1)s, %(extData2)s, %(extData3)s,
        %(extData4)s, %(extData5)s, %(extNumber1)s, %(extNumber2)s, %(extNumber3)s, %(extNumber4)s,
        %(extNumber5)s, %(extDecimal1)s, %(extDecimal2)s, %(extDecimal3)s, %(extDecimal4)s, %(extDecimal5)s,
        %(orderAttribute)s
    ) ON DUPLICATE KEY UPDATE
        status = VALUES(status),
        modifierCode = VALUES(modifierCode),
        modifiedTime = VALUES(modifiedTime),
        amount = VALUES(amount),
        settlementAmount = VALUES(settlementAmount)
    '''
    
    # 处理每条记录
    inserted_count = 0
    for item in service_data_list:
        try:
            # 处理日期时间字段
            processed_item = item.copy()
            processed_item['createTime'] = convert_datetime_format(item.get('createTime'))
            processed_item['modifiedTime'] = convert_datetime_format(item.get('modifiedTime'))
            processed_item['tradeTime'] = convert_datetime_format(item.get('tradeTime'))
            processed_item['auditTime'] = convert_datetime_format(item.get('auditTime'))
            
            # 执行插入操作
            cursor.execute(insert_query, processed_item)
            inserted_count += 1
            
        except Exception as e:
            print(f"插入数据时出错 (entityId: {item.get('entityId')}): {e}")
            connection.rollback()
    
    # 提交事务
    connection.commit()
    print(f"成功插入 {inserted_count} 条记录到数据库")
    cursor.close()

# 示例JSON数据
sample_json_data = {
    "resultCode": "1",
    "resultContent": "",
    "resultData": {
        "serviceData": [
            {
                "entityId": 33659382,
                "status": 1,
                "creatorCode": "管理员",
                "createTime": "2025-10-10 01:43:24",
                "modifierCode": "管理员",
                "modifiedTime": "2025-10-25 12:10:20",
                "clientCode": "AEROPOST",
                "rateCardCode": "TGU-COST-CUST",
                "itemCode": 293975860811798529,
                "accountCode": "77025-84326-001",
                "businessType": "EXP_PKG",
                "chargeType": "DUTY",
                "businessCode": "BG-2510098HKCRRH43V",
                "referenceCode": None,
                "logisticsCode": "HZHN55676938223",
                "pl": "C",
                "categoryLevel1Code": "500",
                "categoryLevel1Name": "Customs",
                "categoryLevel2Code": "500100",
                "categoryLevel2Name": "Customs Duty",
                "categoryCode": "500100011",
                "categoryName": "Honduras VAT",
                "settlementObjectCode": "HORIZON",
                "settlementObjectName": "HORIZON LOGISTICS",
                "settleType": "1",
                "accountBrief": None,
                "count": 231.0,
                "unitPrice": None,
                "tradeUnit": "G",
                "amount": 296,
                "currency": "USD",
                "billedAmount": 0,
                "billedCurrency": None,
                "settlementAmount": 296,
                "settlementCurrency": "USD",
                "accountCurrency": None,
                "billNo": None,
                "exchangeRate": None,
                "myExchangeRate": None,
                "note": None,
                "attachment": None,
                "itemStatus": 10,
                "tradeTime": "2025-10-10 01:43:24",
                "auditor": None,
                "auditTime": None,
                "auditStatus": 0,
                "extData1": "00000",
                "extData2": "Yoro",
                "extData3": "Address1, Address2",
                "extData4": "SAP",
                "extData5": None,
                "extNumber1": 0,
                "extNumber2": 2,
                "extNumber3": None,
                "extNumber4": None,
                "extNumber5": None,
                "extDecimal1": 231.0,
                "extDecimal2": 0.0,
                "extDecimal3": 0.0,
                "extDecimal4": 0.0,
                "extDecimal5": 0.0,
                "orderAttribute": None
            },
            {
                "entityId": 33659381,
                "status": 1,
                "creatorCode": "管理员",
                "createTime": "2025-10-10 01:43:24",
                "modifierCode": "管理员",
                "modifiedTime": "2025-10-25 12:10:20",
                "clientCode": "AEROPOST",
                "rateCardCode": "TGU-COST-CUST",
                "itemCode": 293975860810749955,
                "accountCode": "77025-84326-001",
                "businessType": "EXP_PKG",
                "chargeType": "DUTY",
                "businessCode": "BG-2510098HKCRRH43V",
                "referenceCode": None,
                "logisticsCode": "HZHN55676938223",
                "pl": "C",
                "categoryLevel1Code": "500",
                "categoryLevel1Name": "Customs",
                "categoryLevel2Code": "500100",
                "categoryLevel2Name": "Customs Duty",
                "categoryCode": "500100009",
                "categoryName": "Honduras Duty",
                "settlementObjectCode": "HORIZON",
                "settlementObjectName": "HORIZON LOGISTICS",
                "settleType": "1",
                "accountBrief": None,
                "count": 231.0,
                "unitPrice": None,
                "tradeUnit": "G",
                "amount": 142,
                "currency": "USD",
                "billedAmount": 0,
                "billedCurrency": None,
                "settlementAmount": 142,
                "settlementCurrency": "USD",
                "accountCurrency": None,
                "billNo": None,
                "exchangeRate": None,
                "myExchangeRate": None,
                "note": None,
                "attachment": None,
                "itemStatus": 10,
                "tradeTime": "2025-10-10 01:43:24",
                "auditor": None,
                "auditTime": None,
                "auditStatus": 0,
                "extData1": "00000",
                "extData2": "Yoro",
                "extData3": "Address1, Address2",
                "extData4": "SAP",
                "extData5": None,
                "extNumber1": 0,
                "extNumber2": 2,
                "extNumber3": None,
                "extNumber4": None,
                "extNumber5": None,
                "extDecimal1": 231.0,
                "extDecimal2": 0.0,
                "extDecimal3": 0.0,
                "extDecimal4": 0.0,
                "extDecimal5": 0.0,
                "orderAttribute": None
            },
            {
                "entityId": 33659339,
                "status": 1,
                "creatorCode": "管理员",
                "createTime": "2025-10-10 01:41:37",
                "modifierCode": "管理员",
                "modifiedTime": "2025-10-26 12:08:58",
                "clientCode": "AEROPOST",
                "rateCardCode": "TGU-COST-CUST",
                "itemCode": 293975862651074563,
                "accountCode": "77025-84326-001",
                "businessType": "EXP_PKG",
                "chargeType": "DUTY",
                "businessCode": "BG-2510098AV28M6SZ4",
                "referenceCode": None,
                "logisticsCode": "HZHN55676955210",
                "pl": "C",
                "categoryLevel1Code": "500",
                "categoryLevel1Name": "Customs",
                "categoryLevel2Code": "500100",
                "categoryLevel2Name": "Customs Duty",
                "categoryCode": "500100011",
                "categoryName": "Honduras VAT",
                "settlementObjectCode": "HORIZON",
                "settlementObjectName": "HORIZON LOGISTICS",
                "settleType": "1",
                "accountBrief": None,
                "count": 233.0,
                "unitPrice": None,
                "tradeUnit": "G",
                "amount": 247,
                "currency": "USD",
                "billedAmount": 0,
                "billedCurrency": None,
                "settlementAmount": 247,
                "settlementCurrency": "USD",
                "accountCurrency": None,
                "billNo": None,
                "exchangeRate": None,
                "myExchangeRate": None,
                "note": None,
                "attachment": None,
                "itemStatus": 10,
                "tradeTime": "2025-10-10 01:41:37",
                "auditor": None,
                "auditTime": None,
                "auditStatus": 0,
                "extData1": "00000",
                "extData2": "Cortés",
                "extData3": "Address1, Address2",
                "extData4": "SAP",
                "extData5": None,
                "extNumber1": 0,
                "extNumber2": 1,
                "extNumber3": None,
                "extNumber4": None,
                "extNumber5": None,
                "extDecimal1": 233.0,
                "extDecimal2": 0.0,
                "extDecimal3": 0.0,
                "extDecimal4": 0.0,
                "extDecimal5": 0.0,
                "orderAttribute": None
            },
            {
                "entityId": 33659338,
                "status": 1,
                "creatorCode": "管理员",
                "createTime": "2025-10-10 01:41:37",
                "modifierCode": "管理员",
                "modifiedTime": "2025-10-26 12:08:58",
                "clientCode": "AEROPOST",
                "rateCardCode": "TGU-COST-CUST",
                "itemCode": 293975862651074561,
                "accountCode": "77025-84326-001",
                "businessType": "EXP_PKG",
                "chargeType": "DUTY",
                "businessCode": "BG-2510098AV28M6SZ4",
                "referenceCode": None,
                "logisticsCode": "HZHN55676955210",
                "pl": "C",
                "categoryLevel1Code": "500",
                "categoryLevel1Name": "Customs",
                "categoryLevel2Code": "500100",
                "categoryLevel2Name": "Customs Duty",
                "categoryCode": "500100009",
                "categoryName": "Honduras Duty",
                "settlementObjectCode": "HORIZON",
                "settlementObjectName": "HORIZON LOGISTICS",
                "settleType": "1",
                "accountBrief": None,
                "count": 233.0,
                "unitPrice": None,
                "tradeUnit": "G",
                "amount": 215,
                "currency": "USD",
                "billedAmount": 0,
                "billedCurrency": None,
                "settlementAmount": 215,
                "settlementCurrency": "USD",
                "accountCurrency": None,
                "billNo": None,
                "exchangeRate": None,
                "myExchangeRate": None,
                "note": None,
                "attachment": None,
                "itemStatus": 10,
                "tradeTime": "2025-10-10 01:41:37",
                "auditor": None,
                "auditTime": None,
                "auditStatus": 0,
                "extData1": "00000",
                "extData2": "Cortés",
                "extData3": "Address1, Address2",
                "extData4": "SAP",
                "extData5": None,
                "extNumber1": 0,
                "extNumber2": 1,
                "extNumber3": None,
                "extNumber4": None,
                "extNumber5": None,
                "extDecimal1": 233.0,
                "extDecimal2": 0.0,
                "extDecimal3": 0.0,
                "extDecimal4": 0.0,
                "extDecimal5": 0.0,
                "orderAttribute": None
            }
        ],
        "currentPage": 2,
        "pageSize": 20,
        "totalPage": 24741,
        "totalCount": 494801
    },
    "success": True
}

if __name__ == "__main__":


    # for i in range(1, 24742):
    #     api_call()


    # 解析并存储示例JSON数据
    parse_and_store_json(sample_json_data)