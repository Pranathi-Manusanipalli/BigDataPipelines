import json

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests

# Import Custom Modules
import pandas as pd
import numpy as np
# import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import re
import sys
import pandas_gbq
from google.oauth2 import service_account

# import yaml

default_args = {
    'owner': 'airflow',
    'provide_context': True
}
with DAG(
    'model_inference_pipeline',
    default_args=default_args,
    description='Model_Inference',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    def extraction(**kwargs):

        sql = "SELECT * FROM `bigdata-311523.Invoice_transactions.stage_new_modified_transactions`"
        df = pandas_gbq.read_gbq(sql, project_id="bigdata-311523")
        df.to_csv("gs://invoices_image/composer_stage/model_inference_pipeline.csv",index=False)

    def prediction(**kwargs):

        df = pd.read_csv("gs://invoices_image/composer_stage/model_inference_pipeline.csv")
        desc = list(df['Invoice_Description'])

        final_df = df[0:0]
        preds = []

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        for i in chunks(desc, 20):
            str = ''
            for j in i:
                str = str + 'data={}&'.format(j)
            str = str.rstrip(str[-1])

            r = requests.post("https://fastapi-invoice-categorization-ii5x4gm7ra-uc.a.run.app/predict?{}".format(str), timeout=None)
            a = json.loads(r.text)
            preds.append(a['predicted'])

        print(preds)
        preds = [item for sublist in preds for item in sublist]
        print('after', preds)
        df['Expense_Category'] = preds
        df.to_csv("gs://invoices_image/composer_stage/model_inference_pipeline.csv",index=False)


    def load(**kwargs):
        df=pd.read_csv("gs://invoices_image/composer_stage/model_inference_pipeline.csv")
        pandas_gbq.to_gbq(df, 'Invoice_transactions.categorized_new_transaction_data', if_exists='replace',
                          project_id='bigdata-311523')

        sql1 = "SELECT * FROM `bigdata-311523.Invoice_transactions.invoicedata` WHERE FALSE"
        df1 = pandas_gbq.read_gbq(sql1, project_id="bigdata-311523")
        df1 = pd.concat([df1, df])
        pandas_gbq.to_gbq(df1, 'Invoice_transactions.invoicedata', if_exists='append',
                          project_id='bigdata-311523')
        print("Data loaded to Big query")
        return {'success': 'success'}

    extract = PythonOperator(
        task_id='extract',
        python_callable=extraction,
    )
    predict = PythonOperator(
        task_id='predict',
        python_callable=prediction,
    )
    load = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    extract >> predict >> load