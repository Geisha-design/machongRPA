# 数据库配置文件
# import mysql.connector
# from mysql.connector import Error
import pymysql.cursors
def create_connection():
    """
    创建数据库连接
    """
    connection = None
    try:
        connection = pymysql.Connect(
            host='localhost',
            database='aeropost_data',  # 修改为你的数据库名
            user='root',               # 修改为你的用户名
            password='qyzh12260315'        # 修改为你的密码
        )
        if connection.connect():
            print("成功连接到MySQL数据库")
    except Exception as e:
        print(f"连接MySQL时出错: {e}")
    
    return connection

def create_table(connection):
    """
    创建存储JSON数据的表
    """
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS service_data (
        entityId BIGINT PRIMARY KEY,
        status INT,
        creatorCode VARCHAR(255),
        createTime DATETIME,
        modifierCode VARCHAR(255),
        modifiedTime DATETIME,
        clientCode VARCHAR(255),
        rateCardCode VARCHAR(255),
        itemCode BIGINT,
        accountCode VARCHAR(255),
        businessType VARCHAR(50),
        chargeType VARCHAR(50),
        businessCode VARCHAR(255),
        referenceCode VARCHAR(255),
        logisticsCode VARCHAR(255),
        pl VARCHAR(10),
        categoryLevel1Code VARCHAR(50),
        categoryLevel1Name VARCHAR(255),
        categoryLevel2Code VARCHAR(50),
        categoryLevel2Name VARCHAR(255),
        categoryCode VARCHAR(50),
        categoryName VARCHAR(255),
        settlementObjectCode VARCHAR(255),
        settlementObjectName VARCHAR(255),
        settleType VARCHAR(10),
        accountBrief VARCHAR(255),
        count DECIMAL(15,2),
        unitPrice DECIMAL(15,2),
        tradeUnit VARCHAR(50),
        amount DECIMAL(15,2),
        currency VARCHAR(10),
        billedAmount DECIMAL(15,2),
        billedCurrency VARCHAR(10),
        settlementAmount DECIMAL(15,2),
        settlementCurrency VARCHAR(10),
        accountCurrency VARCHAR(10),
        billNo VARCHAR(255),
        exchangeRate DECIMAL(10,6),
        myExchangeRate DECIMAL(10,6),
        note TEXT,
        attachment TEXT,
        itemStatus INT,
        tradeTime DATETIME,
        auditor VARCHAR(255),
        auditTime DATETIME,
        auditStatus INT,
        extData1 VARCHAR(255),
        extData2 VARCHAR(255),
        extData3 VARCHAR(255),
        extData4 VARCHAR(255),
        extData5 VARCHAR(255),
        extNumber1 INT,
        extNumber2 INT,
        extNumber3 INT,
        extNumber4 INT,
        extNumber5 INT,
        extDecimal1 DECIMAL(15,2),
        extDecimal2 DECIMAL(15,2),
        extDecimal3 DECIMAL(15,2),
        extDecimal4 DECIMAL(15,2),
        extDecimal5 DECIMAL(15,2),
        orderAttribute VARCHAR(255)
    )
    '''
    
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("数据表创建成功")
    except BaseException as e:
        print(f"创建数据表时出错: {e}")
    finally:
        cursor.close()


def create_connection_ar():
    """
    创建数据库连接
    """
    connection = None
    try:
        connection = pymysql.Connect(
            host='localhost',
            database='aeropost_data',  # 修改为你的数据库名
            user='root',  # 修改为你的用户名
            password='qyzh12260315'  # 修改为你的密码
        )
        if connection.connect():
            print("成功连接到MySQL数据库")
    except Exception as e:
        print(f"连接MySQL时出错: {e}")

    return connection


def create_table_ar(connection):
    """
    创建存储JSON数据的表
    """
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS ar (
        entityId BIGINT PRIMARY KEY,
        status INT,
        creatorCode VARCHAR(255),
        createTime DATETIME,
        modifierCode VARCHAR(255),
        modifiedTime DATETIME,
        clientCode VARCHAR(255),
        
        clientName VARCHAR(255),
        
        
        rateCardCode VARCHAR(255),
        itemCode BIGINT,
        accountCode VARCHAR(255),
        businessType VARCHAR(50),
        chargeType VARCHAR(50),
        
        businessModelCode VARCHAR(255),
        
        
        businessCode VARCHAR(255),
        referenceCode VARCHAR(255),
        logisticsCode VARCHAR(255),
        
        
     
        
        
        
        pl VARCHAR(10),
        
        
        plName VARCHAR(255),
        volume VARCHAR(255),
        weight VARCHAR(255),
        
        
        categoryLevel1Code VARCHAR(50),
        categoryLevel1Name VARCHAR(255),
        categoryLevel2Code VARCHAR(50),
        categoryLevel2Name VARCHAR(255),
        categoryCode VARCHAR(50),
        categoryName VARCHAR(255),
        settlementObjectCode VARCHAR(255),
        settlementObjectName VARCHAR(255),
        settleType VARCHAR(10),
        accountBrief VARCHAR(255),
        count DECIMAL(15,2),
        unitPrice DECIMAL(15,2),
        tradeUnit VARCHAR(50),
        amount DECIMAL(15,2),
        currency VARCHAR(10),
        billedAmount DECIMAL(15,2),
        billedCurrency VARCHAR(10),
        settlementAmount DECIMAL(15,2),
        settlementCurrency VARCHAR(10),
        accountCurrency VARCHAR(10),
        billNo VARCHAR(255),
        exchangeRate DECIMAL(10,6),
        myExchangeRate DECIMAL(10,6),
        note TEXT,
        attachment TEXT,
        itemStatus INT,
        
        orderTime DATETIME,
        
        tradeTime DATETIME,
        
        accountingTime DATETIME,
        
        auditor VARCHAR(255),
        auditTime DATETIME,
        
        extData1 VARCHAR(255),
        extData2 VARCHAR(255),
        extData3 VARCHAR(255),
        extData4 VARCHAR(255),
        extData5 VARCHAR(255),
        extNumber1 INT,
        extNumber2 INT,
        extNumber3 INT,
        extNumber4 INT,
        extNumber5 INT,
        extDecimal1 DECIMAL(15,2),
        extDecimal2 DECIMAL(15,2),
        extDecimal3 DECIMAL(15,2),
        extDecimal4 DECIMAL(15,2),
        extDecimal5 DECIMAL(15,2),
        orderAttribute VARCHAR(255),
        
        billCode VARCHAR(255)
    )
    '''

    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("数据表创建成功")
    except BaseException as e:
        print(f"创建数据表时出错: {e}")
    finally:
        cursor.close()