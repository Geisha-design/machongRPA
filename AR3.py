import requests
from json_to_mysql import parse_and_store_json, parse_and_store_json_ar


def api_call(i, location):
    payload =  {
        "express": {
            "clientCode": [
                "EBAO"
            ]
        },
        "pageNum": i,
        "pageSize": 20000,
        "orderBy": "accountingTime desc"
    }
    #     {
    #     "express": {
    #         "rateCardCode": [
    #             location
    #         ]
    #     },
    #     "pageNum": i,
    # "pageSize": 2,
    #     "orderBy": "createTime desc"
    # }



    headers = {"Token": "THQDISGHFZsmleYRkqV6ccGJ70SHPACFkuIpsSnDWmjAXtV+y5A2zf09piQTbFaDBUvimXsTN585UQ971AKwC3Dgu/LNtV6/C1qoGe2hoOIASFq7S56CbsknB1tFl0YSLj37fTv693d+FTpGYcyaHPYhh4UfoZ8mjcVlVQkbUDc="}
    # THQDISGHFZsmleYRkqV6ccGJ70SHPACFkuIpsSnDWmjAXtV + y5A2zf09piQTbFaDBUvimXsTN585UQ971AKwC3Dgu / LNtV6 / C1qoGe2hoOIASFq7S56CbsknB1tFl0YSLj37fTv693d + FTpGYcyaHPYhh4UfoZ8mjcVlVQkbUDc =

    try:
        response = requests.post(
            'https://ship.horizonlogisticshub.com/services/ams/billitem/querylist',
            headers=headers,
            json=payload
        )
        print(f"接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            parse_and_store_json_ar(result)
            print(f"响应内容: {result}")
            return True
        else:
            print(f"错误响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"调用接口时出错: {e}")
        return False

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
    # sample_data = generate_sample_data()
    # parse_and_store_json_ar(sample_data)
    # 22 开始 作为执行项标准来看
    # 如果需要调用API，请取消注释下面的代码

    # 创建一个列表来存储失败的页码
    failed_pages = []

    for i in range(371, 430):
        try:
            success = api_call(i, "SJO-COST-H-CUST")
            if success:
                print(f"第{i}页数据处理完成")
            else:
                print(f"第{i}页数据处理失败")
                failed_pages.append(i)
                # 实时记录失败的页码到本地txt文件
                with open("failed_pages.txt", "a", encoding="utf-8") as f:
                    f.write(f"{i}\n")
        except Exception as e:
            print(f"第{i}页数据处理失败: {e}")
            failed_pages.append(i)
            # 实时记录失败的页码到本地txt文件
            with open("failed_pages.txt", "a", encoding="utf-8") as f:
                f.write(f"{i}\n")
        # api_call(i, "SJO-COST-H-CUST")

    # 将失败的页码写入本地txt文件
    if failed_pages:
        print(f"共有 {len(failed_pages)} 个页面处理失败，页码已实时保存到 failed_pages.txt 文件中")
    else:
        print("所有页面都处理成功")

# 31 32 33
# if __name__ == '__main__':
#     # 生成并处理样本数据
#     # sample_data = generate_sample_data()
#     # parse_and_store_json_ar(sample_data)
#     # 22 开始 作为执行项标准来看
#     # 如果需要调用API，请取消注释下面的代码
#     for i in range(295, 2000):
#         try:
#             api_call(i, "SJO-COST-H-CUST")
#             print(f"第{i}页数据处理完成")
#         except Exception as e:
#             print(f"第{i}页数据处理失败: {e}")
#         # api_call(i, "SJO-COST-H-CUST")