# Invoice Categorization

**Team 4**<br>
Prudhvi Chandra Sekharamahanti<br>
Harika Reddy Gurram<br>
Pranathi Manusanipalli<br>

**Problem Statement:**<br><br>
Organization xyz is spending millions of dollars on various resources/products required for the company to run smoothly but has no definitive analytics and categorization tool that helps them with all their spends. The input can be CSV or batch files.Our goal is to predict the category of the invoice based on invoice description.We build end to end pipelines that handle extraction,preprocessing, perform model training and model serving functionalities with ease.

**User:**<br>

FINANCIAL ANALYST<br><br>

**Functions:**<br>

Upload new invoice transaction files for categorization(Batch)<br>
Uploads an invoice image and gets the associated predictions( category ) from the Model Inference API<br><br>

**Technology Stack:**<br>

- Cloud Storage
- Cloud Run
- Cloud Functions
- Cloud Composer
- Big Query
- Google Datastudio
- Streamlit
- FastAPI
- Docker
- Apache Airflow
- Pytest

## Setup & Depployments

**Create a GCP account and activate your account to get 300$ free credit**<br>
Steps:
1. Go to https://cloud.google.com/ and click on ‘TRY IT FREE‘.<br>
2. Now, it will ask you to login to your Gmail account and choose your country and accept the terms & conditions<br>
3. In the third step, you have to fill your details, like account type, Name, Address, credit card details, tax information, etc. If you have old Gmail account and all the information is already there it would take it and you might not have to fill all the details.<br>
4. After filling all the details click on “Start my free trial“.<br>
5. Now Google will setup your cloud account and in few seconds your Google Cloud Platform account will be ready.<br><br>

**Creation of project**<br>
- In the dropdown beside search bar click on it and then click new project and create one<br><br>

For detailed account creation with screenshots visit: https://www.storagetutorials.com/create-free-trial-google-cloud-platform/<br>

**Enabling API's**
- In the search bar on the Search for API's and Services --> then click on Library --> Search for Cloud Functions, Cloud Run, Cloud Storage, Cloud Build, Cloud Composer, Bigquery and enable them<br><br>

**Deploying Airflow Pipelines on Cloud Composer**<br>

- Search for composer in the search panel<br>
- Click on create<br>
- Give the following options:<br>
  -  name: <name of composer environment><br>
  -  Location: us-central1<br>
  -  nodes:3<br>
  -  Zone: us-central1-c<br>
  -  Machine type: n1-standard-2<br>
  -  Image Version: composer-1.16.2-airflow-1.10.15<br>
  -  Pyhton version: 3<br>
 Just change only the above mentioned options and click on Create<br>
- Once Environment is created, click on it got to PYPI packages and add below packages and click update:<br>
   - scikit-learn<br>
   - sqlalchemy==1.3.18<br>
   - pandas_gbq<br>
   - fsspec<br>
   - gcsfs<br>
- Now environment is ready to upload airflow dags and trigger them.<br><br>

Adding Dags to Environment Bucket:<br>
- In the Composer Home Page under DAGs folder for the created environment click on the hyperlink and it will take you to the dags folder where the dags needs to be uploaded.
- Here in this case it is: https://console.cloud.google.com/storage/browser/us-central1-airflow-e35eb1a6-bucket/dags;tab=objects?project=bigdata-311523&prefix=&forceOnObjectsSortingFiltering=false<br><br>

Running Airflow Dags:<br>
- Here we have 4 designed for the project purpose<br>
  - ETL_TRAIN: DAG to do the ETL on initial training data<br>
  - ML_MODEL_TRAIN: DAG to fetch the training data, train the classification model and save the model in Cloud storage<br>
  - ETL_INFERENCE: DAG to do ETL on newly coming transactions aand stage them into tables<br>
  - MODEL_INFERENCE: DAG that takes the new transactions from stage and predects the categories for invoices by inferencing dockerized FastAPI model<br>
- Inorder to successfully run the pipelines following steps to be implemented:<br>
   Training:<br>
  - First upload the training_data.csv file in invoice_images/train_data data<br>
  - In composer homepage on GCP we have url to access Airflow, here it is: https://jf9eec1d3b656d340p-tp.appspot.com/admin/.<br>
  - click on TRAINING_ETL_DAG whhich does the ETL and automatically triggers ML_MODEL_TRAIN_DAG which trains and loads the model<br>
  - Thus we accomplished the initial task of traning<br>
  Inference:<br>
  - We no need to trigger any DAG's manually for inference/prediction on new transactions automatically which will be clearly discussed in used case section below<br><br>

**Deploying Dockerized FastAPI for serving the model**<br><br>
- cd into FastAPI folder<br> 
Setting up docker and linking them with google Containerized Repositories:<br>

- Dockerizing Application

    `docker build -t <imagename> .`
  
    `docker run -d -p 5000:5000 imagename`

***Deploying the app on Google Cloud Run:***<br>

- Install Google Cloud SDK 
- Authenticate the SDK using<br>
  `google auth login`<br>
- Authenicate docker to push images to Google Cloud Container Repositories<br>
  `google auth configure-docker`<br>
- Create a tag for your image<br>
  `docker tag imagename us.gcr.io/project-id/imagename` <br>
- Push the docker image<br>
  `docker push us.gcr.io/project-id/imagename` <br>
- Now to go to Cloud run and create a service with following parameters: <br>
  - select the image from the container repository which we pushed<br>
  - Memory: min 4GB<br>
  - Create<br>
- Once Cloud Run service is created we will get the service url and our API is up and running<br>
- To access the API use `SERVICE URL/predict`<br>




  



