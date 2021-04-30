from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import json
from google.oauth2 import service_account
import pandas_gbq
import re
import os

default_args = {
    'owner': 'airflow',
    'provide_context': True,
}
with DAG(
    'ETL_Inference',
    default_args=default_args,
    description='ETL_train',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    def extract(**kwargs):
        #ti = kwargs['ti']

        sql = "SELECT * FROM `bigdata-311523.Invoice_transactions.stage_invoices`"
        df = pandas_gbq.read_gbq(sql, project_id="bigdata-311523")
        #out = df.to_dict('records')
        #print(df.shape)
        df.to_csv("gs://invoices_image/composer_stage/ETL_Inference.csv",index=False)
        #ti.xcom_push('data', out)


    def dropcolumns(**kwargs):
        #ti = kwargs['ti']

        #df = ti.xcom_pull(task_ids='extract', key='data')
        #df=pd.DataFrame(df)
        df=pd.read_csv("gs://invoices_image/composer_stage/ETL_Inference.csv")
        print(df.columns)
        df1=df.drop(columns=['Category', 'Zip', 'Contract_Number', 'PO_Number', 'PO_Line'])
        df2=df1.drop(columns=['Invoice_Distribution_Line'])
        print(df2.columns)
        # out = df2.to_dict('records')
        # ti.xcom_push('data', out)
        df2.to_csv("gs://invoices_image/composer_stage/ETL_Inference.csv",index=False)



    def cleaning(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='dropcolumns', key='data')
        # df = pd.DataFrame(df)
        df=pd.read_csv("gs://invoices_image/composer_stage/ETL_Inference.csv")
        def clean_str(row):
            """
            String cleaning .
            """
            string = row['Invoice_Description']
            #     print(string)
            string = re.sub(r"[^A-Za-z0-9]", " ",
                            str(string))  # remove unused charactor other than english letter and number, use space to replace
            #     print(string)
            return pd.Series([string.strip()])

        # Removing special characters
        df[['cleaned_invoice_description']] = df.apply(lambda row: clean_str(row), axis=1)
        df['Invoice_Description'] = df['cleaned_invoice_description']
        df = df.drop(columns=['cleaned_invoice_description'])

        # Replacing " " in column names with '_'
        df.columns = [c.replace(' ', '_') for c in df.columns]
        df.to_csv("gs://invoices_image/composer_stage/ETL_Inference.csv",index=False)

        # out = df.to_dict('records')
        # ti.xcom_push('data', out)

    def transform(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='cleaning', key='data')
        # df = pd.DataFrame(df)
        df=pd.read_csv("gs://invoices_image/composer_stage/ETL_Inference.csv")
        # Replacing the missing invoice dates based on Fiscal Year Period
        df['Invoice_Date'].fillna(df['Fiscal_Year_Period'].map(str) + '/01/' + df['Fiscal_Year'].map(str),
                                  inplace=True)
        # Replacing " " in column names with '_'
        df.columns = [c.replace(' ', '_') for c in df.columns]
        # change the invoice_date format - String to Timestamp format
        # df['Invoice_Date'] = pd.to_datetime(df.Invoice_Date, format='%m/%d/%Y')
        # change description - UPPER case to LOWER case
        df['Invoice_Description'] = df.Invoice_Description.str.lower()
        df.to_csv("gs://invoices_image/composer_stage/ETL_Inference.csv",index=False)
        # out = df.to_dict('records')
        # ti.xcom_push('data', out)

    def load(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='transform', key='data')
        # df = pd.DataFrame(df)
        df=pd.read_csv("gs://invoices_image/composer_stage/ETL_Inference.csv")
        pandas_gbq.to_gbq(df, 'Invoice_transactions.stage_new_modified_transactions', if_exists='replace',
                          project_id='bigdata-311523')
        print("Data loaded to Big query")
        return {'success': 'success'}

    def Inference_Pipeline_Trigger(**kwargs):

        os.system("airflow dags trigger model_inference_pipeline")


    extract = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    dropcolumns = PythonOperator(
        task_id='dropcolumns',
        python_callable=dropcolumns,
    )
    cleaning = PythonOperator(
        task_id='cleaning',
        python_callable=cleaning,
    )
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    load = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    Inference_Pipeline_Trigger = PythonOperator(
        task_id='Inference_Pipeline_Trigger',
        python_callable=Inference_Pipeline_Trigger,
    )


    extract >> dropcolumns >> cleaning >> transform >> load >> Inference_Pipeline_Trigger