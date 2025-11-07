import requests
from json_to_mysql import parse_and_store_json, parse_and_store_json_ar


def api_call(i, location):
    payload = {
        "express": {
            "rateCardCode": [
                location
            ]
        },
        "pageNum": i,
        "pageSize": 2,
        "orderBy": "createTime desc"
    }

    headers = {"Token": "j5Axr4US1Gcs8SWIPaRo3z5idTQkq2uPZ44okcd6pVZ+x49PoLJCsm7CHHUBZ9WFdgogUaGkPXHCg4HpiPfU+1XZDFaKx9sZgCM3oXuRXAhtTykfHM1hzjH7hLagmXBui+VJ/yDql0euqgkp24vZX3VCF7scoiptbFOGQfErCbc="}
    
    try:
        response = requests.post(
            'https://ship.horizonlogisticshub.com/services/ams/supplieraccountitem/querylist',
            headers=headers,
            json=payload
        )
        print(f"接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            parse_and_store_json_ar(result)
            print(f"响应内容: {result}")
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")

def generate_sample_data():
    """
    生成您指定格式的样本数据
    """
    sample_data = {
        "resultCode": "1",
        "resultContent": "",
        "resultData": {
            "serviceData": [
                {
                    "entityId": 17740462,
                    "status": 1,
                    "creatorCode": "管理员",
                    "createTime": "2025-11-06 22:34:58",
                    "modifierCode": "管理员",
                    "modifiedTime": "2025-11-06 22:34:58",
                    "clientCode": "EBAO",
                    "clientName": "易豹网络科技有限公司",
                    "rateCardCode": "SJO-PRICE-H-DELIVERY",
                    "itemCode": 295984936728088576,
                    "accountCode": "21099-84326-001",
                    "businessType": "EXP_PKG",
                    "chargeType": "DELIVERY",
                    "businessModelCode": "PEE397827",
                    "businessCode": "BG-25100488VPACP64G",
                    "logisticsCode": "HZCR55674680222",
                    "referenceCode": 293417940636270592,
                    "pl": "D",
                    "plName": "核销",
                    "volume": None,
                    "weight": 3441,
                    "categoryLevel1Code": "631",
                    "categoryLevel1Name": "DeliveryCharge",
                    "categoryLevel2Code": "631001",
                    "categoryLevel2Name": "Delivery Charge",
                    "categoryCode": "631001001",
                    "categoryName": "Delivery Charge",
                    "settlementObjectCode": "HORIZON",
                    "settlementObjectName": "HORIZON LOGISTICS",
                    "settleType": "1",
                    "accountBrief": "冲红",
                    "count": 3441.0,
                    "unitPrice": 0.0,
                    "tradeUnit": "G",
                    "amount": -348,
                    "currency": "USD",
                    "billedAmount": -348,
                    "billedCurrency": "USD",
                    "settlementAmount": -348,
                    "settlementCurrency": "USD",
                    "accountCurrency": None,
                    "billNo": None,
                    "exchangeRate": None,
                    "myExchangeRate": None,
                    "note": "[Return] 包裹 HZCR55674680222 末端运费, 运单重量3.441, 体积重量0.000, 重量等级3441G 末端分区Zonenull,业务编码 PEE397827",
                    "attachment": None,
                    "itemStatus": 12,
                    "orderTime": "2025-10-09 02:33:36",
                    "tradeTime": "2025-10-09 02:33:36",
                    "accountingTime": "2025-11-06 22:34:58",
                    "auditor": None,
                    "auditTime": None,
                    "extData1": "21013",
                    "extData2": "Alajuela",
                    "extData3": "Address1, Address2",
                    "extData4": "SJO",
                    "extData5": None,
                    "extNumber1": 0,
                    "extNumber2": 0,
                    "extNumber3": None,
                    "extNumber4": None,
                    "extNumber5": None,
                    "extDecimal1": 3441.0,
                    "extDecimal2": 0.0,
                    "extDecimal3": 0.0,
                    "extDecimal4": 0.0,
                    "extDecimal5": 0.0,
                    "orderAttribute": None,
                    "billCode": None
                }
            ],
            "currentPage": 1,
            "pageSize": 1,
            "totalPage": 1,
            "totalCount": 1
        },
        "success": True
    }
    return sample_data

if __name__ == '__main__':
    # 生成并处理样本数据
    sample_data = generate_sample_data()
    parse_and_store_json_ar(sample_data)
    
    # 如果需要调用API，请取消注释下面的代码
    # for i in range(100, 124):
    #     api_call(i, "SJO-COST-H-CUST")