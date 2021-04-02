import pandas as pd
import os
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

def DataExtraction():
    # Train data
    faults=['FD001','FD002','FD003','FD004']
    dataset_type=['train','test']
    rul=['RUL']

    collist=['unit_number','time_in_cycles']+['operational_setting_'+str(i) for i in range(1,4)]+['sensor_measurement_'+str(i) for i in range(1,22)]
    collist=[x.upper() for x in collist]
    train_df=pd.DataFrame({})
    test_df=pd.DataFrame({})
    for k in dataset_type:
            j=1
            for i in faults:

                df1=pd.read_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/cmaps_data/{}_{}'.format(k,i)+'.txt',names=collist,sep='\s')
                if j==1:
                    df1['FAULT']=i
                    if k =='train':
                        train_df=df1.copy()
                    else:
                        test_df = df1.copy()
                else:
                    df1['FAULT']=i
                    if k=='train':
                        train_df=pd.concat([train_df,df1])
                    else:
                        test_df = pd.concat([test_df, df1])
                j=j+1
                # print(df1.shape)
            if k=='train':
                train_df['DATASET_TYPE']=k
                # print(train_df.shape)
            else:
                test_df['DATASET_TYPE'] = k
                # print(test_df.shape)
    # print(train_df['fault'].unique())
    # print(test_df['fault'].unique())
    # print(train_df['dataset_type'].unique())
    # print(test_df['dataset_type'].unique())

    final_df=pd.concat([train_df,test_df])

    #RUL data
    l=1
    rul_df=pd.DataFrame({})
    for a in faults:
        df1 = pd.read_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/cmaps_data/RUL_{}'.format(a) + '.txt', names=rul)
        if l == 1:
            df1['FAULT'] = a
            df1['UNIT_NUMBER']=[i for i in range(1,len(df1['RUL'])+1)]
            # print(df1.shape)
            rul_df=df1.copy()
        else:
            df1['FAULT'] = a
            df1['UNIT_NUMBER'] = [i for i in range(1, len(df1['RUL']) + 1)]
            # print(df1.shape)
            rul_df=pd.concat([rul_df,df1])
        l=l+1
    # print(rul_df.shape)
    # print(rul_df.tail())
    final_df.to_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/final_data/train_test.csv',index=False)
    rul_df.to_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/final_data/rul.csv', index=False)
    print('Files saved successfully')

def SnowflakeLoad():
    train_test_df=pd.read_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/final_data/train_test.csv')
    rul_df_final=pd.read_csv('/Users/harika/Desktop/CSYE_7245/Assignment3/FastAPI/airflow/final_data/rul.csv')

    conn = snow.connect(user="prudhvics",
                        password="Prudhvi_43",
                        account="tx62478.us-central1.gcp")

    cur = conn.cursor()

    sql = "USE ROLE SYSADMIN"
    cur.execute(sql)

    sql = """CREATE WAREHOUSE IF NOT EXISTS CMAPS 
             WITH WAREHOUSE_SIZE = XSMALL"""
    cur.execute(sql)

    sql = "USE WAREHOUSE CMAPS"
    cur.execute(sql)

    # See if the desired database exists.
    sql = "CREATE DATABASE IF NOT EXISTS NASA_CMAPS"
    cur.execute(sql)


    # And then use it.
    sql = "USE DATABASE NASA_CMAPS"
    cur.execute(sql)

    sql = "CREATE SCHEMA IF NOT EXISTS DEV"
    cur.execute(sql)

    # And then use it.
    sql = "USE SCHEMA DEV"
    cur.execute(sql)

    # And finally, the table.
    sql = """CREATE TABLE IF NOT EXISTS TRAIN_TEST
                (unit_number INT,
                time_in_cycles INT,
                operational_setting_1 NUMBER(18,4),
                operational_setting_2 NUMBER(18,4),
                operational_setting_3 NUMBER(18,4),
                sensor_measurement_1 NUMBER(18,4),
                 sensor_measurement_2 NUMBER(18,4),
                 sensor_measurement_3 NUMBER(18,4),
                 sensor_measurement_4 NUMBER(18,4),
                 sensor_measurement_5 NUMBER(18,4),
                 sensor_measurement_6 NUMBER(18,4),
                 sensor_measurement_7 NUMBER(18,4),
                 sensor_measurement_8 NUMBER(18,4),
                 sensor_measurement_9 NUMBER(18,4),
                 sensor_measurement_10 NUMBER(18,4),
                 sensor_measurement_11 NUMBER(18,4),
                 sensor_measurement_12 NUMBER(18,4),
                 sensor_measurement_13 NUMBER(18,4),
                 sensor_measurement_14 NUMBER(18,4),
                 sensor_measurement_15 NUMBER(18,4),
                 sensor_measurement_16 NUMBER(18,4),
                 sensor_measurement_17 NUMBER(18,4),
                 sensor_measurement_18 NUMBER(18,4),
                 sensor_measurement_19 NUMBER(18,4),
                 sensor_measurement_20 NUMBER(18,4),
                 sensor_measurement_21 NUMBER(18,4),
                 fault STRING,
                 dataset_type STRING)"""
    cur.execute(sql)

    sql= "CREATE TABLE IF NOT EXISTS RUL(rul INT,fault STRING,unit_number INT)"
    cur.execute(sql)
    print('Database objects created successfully')

    write_pandas(conn, train_test_df, "TRAIN_TEST")
    write_pandas(conn, rul_df_final, "RUL")

    cur.close()
    conn.close

    print('Database objects loaded successfully')

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('CMAPS_SNOWFLAKE_INGESTION',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_start = PythonOperator(task_id='DataExtraction',
                              python_callable=DataExtraction)
    t1_getdata = PythonOperator(task_id='DataLoadSnowflake',
                                python_callable=SnowflakeLoad)


t0_start >> t1_getdata










