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

    print("开始执行4")
    for i in range(3, 50):
        api_call(i,"SJO-COST-H-DELIVERY")

    # api_call()



# JM-COST-AEROPOST-MAWB  牙买加Aeropost干线成本 ok
# TGU-COST-CUST  洪都拉斯税费成本 ok
# TGU-COST-DELIVERY  洪都拉斯运费成本 ok
# TGU-COST-CIF-MAWB  洪都拉斯CIF成本 ok
# TGU-COST-CIF-MAWB 危地马拉运费成本 ok
# UIO-COST-SER-DELIVERY SER-厄瓜多尔运费成本。 running
# UIO-COST-ECPOST-CUST ECPOST-厄瓜多尔清关成本。running
# KIN-COST-H-DELIVERY 牙买加运费。ok
# CIF-MAWB-COST-POS  CIF-TT Master Transfer Cost。ok


# SJO-COST-H-DELIVERY 哥斯达黎加商清运费成本 running
# SJO-COST-C-DELIVERY 哥斯达黎加邮清运费成本 ？？
# SJO-COST-C-CUST 哥斯达黎加邮清税费成本。？？
# SJO-COST-H-CUST     哥斯达黎加商清税费成本  ？？


# TT-COST-DUTY-H 特立尼达多巴哥成本税费 ok
# MVD-COST-U-CUST 乌拉圭税费成本 ok
# MVD-COST-U-DELIVERY 乌拉圭运费成本 running
# POS-COST-A-L1  HORIZON-AEROPOST的南美账套？ok


# {
#   "express": {
#     "rateCardCode": [
#       "POS-COST-A-L1"
#     ]
#   },
#   "pageNum": 1,
#   "pageSize": 20,
#   "orderBy": "createTime desc"
# }







# {
#   "express": {
#     "rateCardCode": [
#       "MVD-COST-U-DELIVERY"
#     ]
#   },
#   "pageNum": 1,
#   "pageSize": 20,
#   "orderBy": "createTime desc"
# }
# {
#   "express": {
#     "rateCardCode": [
#       "MVD-COST-U-CUST"
#     ]
#   },
#   "pageNum": 1,
#   "pageSize": 20,
#   "orderBy": "createTime desc"
# }




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