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
    # 72 之后开始
    for i in range(84, 101):
        api_call(i,"SJO-COST-H-CUST")
    # JM-COST-AEROPOST-MAWB  牙买加Aeropost干线成本 ok
    # TGU-COST-CUST  洪都拉斯税费成本 ok
    # TGU-COST-DELIVERY  洪都拉斯运费成本 ok
    # TGU-COST-CIF-MAWB  洪都拉斯CIF成本 ok
    # TGU-COST-CIF-MAWB 危地马拉运费成本 ok
    # UIO-COST-SER-DELIVERY SER-厄瓜多尔运费成本。 ok
    # UIO-COST-ECPOST-CUST ECPOST-厄瓜多尔清关成本。ok
    # KIN-COST-H-DELIVERY 牙买加运费。ok
    # CIF-MAWB-COST-POS  CIF-TT Master Transfer Cost。ok
    # SJO-COST-H-DELIVERY 哥斯达黎加商清运费成本 ok
    # SJO-COST-C-DELIVERY 哥斯达黎加邮清运费成本 ok
    # SJO-COST-C-CUST 哥斯达黎加邮清税费成本。ok
    # SJO-COST-H-CUST     哥斯达黎加商清税费成本  running
    # TT-COST-DUTY-H 特立尼达多巴哥成本税费 ok
    # MVD-COST-U-CUST 乌拉圭税费成本 ok
    # MVD-COST-U-DELIVERY 乌拉圭运费成本 ok
    # POS-COST-A-L1  HOR-特立尼达成本-A ok