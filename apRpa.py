import requests

from json_to_mysql import parse_and_store_json


def api_call(i,location):
    payload = {
  "express": {
    "rateCardCode": [
      location
    ]
  },
  "pageNum": i,
  "pageSize": 20000,
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

            parse_and_store_json(result)
            print(f"响应内容: {result}")
            # 解析回执的保文

        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")



if __name__ == '__main__':
    for i in range(1, 61):
        api_call(i,"SJO-COST-H-CUST")
# 31之后开始


# JM-COST-AEROPOST-MAWB  牙买加Aeropost干线成本
# TGU-COST-CUST  洪都拉斯税费成本
# TGU-COST-DELIVERY  洪都拉斯运费成本
# TGU-COST-CIF-MAWB  洪都拉斯CIF成本
# TGU-COST-CIF-MAWB 危地马拉运费成本
# UIO-COST-SER-DELIVERY SER-厄瓜多尔运费成本
# UIO-COST-ECPOST-CUST ECPOST-厄瓜多尔清关成本



# {
#   "express": {
#     "rateCardCode": [
#       ""
#     ]
#   },
#   "pageNum": 1,
#   "pageSize": 20,
#   "orderBy": "createTime desc"
# }


# {
#   "express": {
#     "rateCardCode": [
#       "TGU-COST-DELIVERY"
#     ]
#   },
#   "pageNum": 1,
#   "pageSize": 20,
#   "orderBy": "createTime desc"
# }