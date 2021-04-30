from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
# Import Custom Modules
import os
import pandas as pd
import numpy as np
import json
import re
import sys
import pandas_gbq
from google.oauth2 import service_account


default_args = {
    'owner': 'airflow',
    'provide_context': True,
}

with DAG(
    'TRAINING_ETL_DAG',
    default_args=default_args,
    description='ETL_train',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    def EXTRACTION(**kwargs):
        ti = kwargs['ti']
        df=pd.read_csv('gs://invoices_image/train_data/training_data.csv')
        df.to_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv',index=False)
        #out = df.to_dict('records')
        #ti.xcom_push('data', out)

    def DROPCOLUMNS(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='EXTRACTION', key='data')
        # df = pd.DataFrame(df)
        # Dropping columns we do not need
        df=pd.read_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv')
        df.drop(['Category', 'Zip', 'Contract Number', 'PO Number', 'PO Line'], axis=1, inplace=True)
        df.drop(['Invoice Distribution Line'], axis=1, inplace=True)
        df.to_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv', index=False)

    def CLEANING(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='DROPCOLUMNS', key='dropdata')
        # df = pd.DataFrame(df)
        df = pd.read_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv')
        def clean_str(row):
            """
            String cleaning .
            """
            string = row['Invoice Description']
            string2 = row['Expense Category']
            #     print(string)
            string = re.sub(r"[^A-Za-z0-9]", " ",
                            string)  # remove unused charactor other than english letter and number, use space to replace
            #     print(string)
            string2 = re.sub(r"[^A-Za-z0-9]", " ", string2)
            return pd.Series([string.strip(), string2.strip()])

        # Removing special characters
        df[['cleaned_invoice_description', 'cleaned_expense_category']] = df.apply(lambda row: clean_str(row), axis=1)
        df['Expense Category'] = df['cleaned_expense_category']
        df['Invoice Description'] = df['cleaned_invoice_description']
        df = df.drop(columns=['cleaned_invoice_description', 'cleaned_expense_category'])

        # Replacing " " in column names with '_'
        df.columns = [c.replace(' ', '_') for c in df.columns]
        df.to_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv', index=False)
        # out = df.to_dict('records')
        # ti.xcom_push('cleandata', out)

    def TRANSFORM(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='CLEANING', key='cleandata')
        # df = pd.DataFrame(df)
        df = pd.read_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv')
        # Replacing the missing invoice dates based on Fiscal Year Period
        df['Invoice_Date'].fillna(df['Fiscal_Year_Period'].map(str) + '/01/' + df['Fiscal_Year'].map(str), inplace=True)
        # Replacing " " in column names with '_'
        df.columns = [c.replace(' ', '_') for c in df.columns]
        # change the invoice_date format - String to Timestamp format
        # df['Invoice_Date'] = pd.to_datetime(df.Invoice_Date, format='%m/%d/%Y')
        # change description - UPPER case to LOWER case
        df['Invoice_Description'] = df.Invoice_Description.str.lower()
        df.to_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv', index=False)
        # out = df.to_dict('records')
        # ti.xcom_push('transformdata', out)


    def LOAD(**kwargs):
        #
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='TRANSFORM', key='transformdata')
        # df = pd.DataFrame(df)
        df = pd.read_csv('gs://invoices_image/composer_stage/ETL_TRAIN.csv')
        pandas_gbq.to_gbq(df, 'Invoice_transactions.invoicedata', if_exists='append', project_id='bigdata-311523')
        print("Data loaded to Big query")


    def MODEL_TRAINING_DAG_TRIGGER(**kwargs):
        os.system('airflow dags trigger ML_MODEL_TRAIN')


    EXTRACTION = PythonOperator(
        task_id='EXTRACTION',
        python_callable=EXTRACTION,
    )
    DROPCOLUMNS = PythonOperator(
        task_id='DROPCOLUMNS',
        python_callable=DROPCOLUMNS,
    )
    CLEANING = PythonOperator(
        task_id='CLEANING',
        python_callable=CLEANING,
    )
    TRANSFORM = PythonOperator(
        task_id='TRANSFORM',
        python_callable=TRANSFORM,
    )
    LOAD = PythonOperator(
        task_id='LOAD',
        python_callable=LOAD,
    )
    MODEL_TRAINING_DAG_TRIGGER = PythonOperator(
        task_id='MODEL_TRAINING_DAG_TRIGGER',
        python_callable=MODEL_TRAINING_DAG_TRIGGER,
    )


    EXTRACTION >> DROPCOLUMNS >> CLEANING >> TRANSFORM >> LOAD >> MODEL_TRAINING_DAG_TRIGGER