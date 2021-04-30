import json

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Import Custom Modules
import pandas as pd
import numpy as np
# import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import re
import sys
import pandas_gbq
from google.cloud import storage
from google.oauth2 import service_account
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# import yaml


default_args = {
    'owner': 'airflow',
    'provide_context': True,
}
with DAG(
        'ML_MODEL_TRAIN',
        default_args=default_args,
        description='ETL_train',
        schedule_interval=None,
        start_date=days_ago(2),
        tags=['example'],
) as dag:
    def EXTRACTION(**kwargs):
        ti = kwargs['ti']

        sql = "SELECT * FROM `bigdata-311523.Invoice_transactions.invoicedata`"
        df = pandas_gbq.read_gbq(sql, project_id="bigdata-311523")
        df.to_csv('gs://invoices_image/composer_stage/MODEL_TRAIN.csv', index=False)


    def FEATURE_EXTRACTION(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='EXTRACTION', key='data')
        # df = pd.DataFrame(df)
        df = pd.read_csv('gs://invoices_image/composer_stage/MODEL_TRAIN.csv')
        print(df.shape)
        # Extracting columns we needed for the model
        df = df[['Invoice_Description', 'Expense_Category']]
        # print(df.shape)
        # out = df.to_dict('records')
        # ti.xcom_push('feature_extraction', out)
        df.to_csv('gs://invoices_image/composer_stage/MODEL_TRAIN.csv', index=False)


    def SPLITTING(**kwargs):
        # ti = kwargs['ti']
        # df = ti.xcom_pull(task_ids='FEATURE_EXTRACTION', key='feature_extraction')
        # df = pd.DataFrame(df)
        df = pd.read_csv('gs://invoices_image/composer_stage/MODEL_TRAIN.csv')
        sentences = df['Invoice_Description'].values
        y = df['Expense_Category'].values

        sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.25,
                                                                            random_state=1000)
        out1 = {'sentences_train': sentences_train.tolist(),
                'y_train': y_train.tolist()

               }
        out2={'sentences_test': sentences_test.tolist(), 'y_test': y_test.tolist()}
        df1=pd.DataFrame(out1)
        df2 = pd.DataFrame(out2)
        df1.to_csv('gs://invoices_image/composer_stage/TRAIN.csv', index=False)
        df2.to_csv('gs://invoices_image/composer_stage/TEST.csv', index=False)

    def TRAINING(**kwargs):
        # ti = kwargs['ti']
        # out = ti.xcom_pull(task_ids='SPLITTING', key='splitting')
        df1 = pd.read_csv('gs://invoices_image/composer_stage/TRAIN.csv')
        df2 = pd.read_csv('gs://invoices_image/composer_stage/TEST.csv')

        sentences_train = np.array(list(df1['sentences_train']))
        sentences_test = np.array(list(df2['sentences_test']))

        vectorizer = CountVectorizer()
        vectorizer.fit(sentences_train)

        X_train = vectorizer.transform(sentences_train)
        X_test = vectorizer.transform(sentences_test)
        y_train = df1['y_train']
        y_test = df2['y_test']
        print(X_train.shape)

        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)

        print("Accuracy:", score)
        import pickle
        os.system("mkdir -p model")
        workdir = "./model/"
        pickle.dump(classifier, open(workdir + 'classifier.sav', "wb"))
        pickle.dump(vectorizer, open(workdir + 'vectorizer.sav', "wb"))
        print('model saved successfully')


    def GCP_LOAD(**kwargs):
        for i in ['classifier', 'vectorizer']:
            source_file_name = 'model/{}.sav'.format(i)
            destination_blob_name = 'model/{}.sav'.format(i)
            storage_client = storage.Client()
            bucket = storage_client.bucket('invoices_image')
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)

            print(
                "File uploaded to {}.".format(
                    destination_blob_name
                )
            )


    EXTRACTION = PythonOperator(
        task_id='EXTRACTION',
        python_callable=EXTRACTION,
    )
    FEATURE_EXTRACTION = PythonOperator(
        task_id='FEATURE_EXTRACTION',
        python_callable=FEATURE_EXTRACTION,
    )
    SPLITTING = PythonOperator(
        task_id='SPLITTING',
        python_callable=SPLITTING,
    )
    TRAINING = PythonOperator(
        task_id='TRAINING',
        python_callable=TRAINING,
    )
    GCP_LOAD = PythonOperator(
        task_id='GCP_LOAD',
        python_callable=GCP_LOAD,
    )

    EXTRACTION >> FEATURE_EXTRACTION >> SPLITTING >> TRAINING >> GCP_LOAD