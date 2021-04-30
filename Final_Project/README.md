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

Create a GCP account and activate your account to get 300$ free credit<br>
Steps:
1. Go to https://cloud.google.com/ and click on ‘TRY IT FREE‘.<br>
2. Now, it will ask you to login to your Gmail account and choose your country and accept the terms & conditions<br>
3. In the third step, you have to fill your details, like account type, Name, Address, credit card details, tax information, etc. If you have old Gmail account and all the information is already there it would take it and you might not have to fill all the details.<br>
4. After filling all the details click on “Start my free trial“.<br>
5. Now Google will setup your cloud account and in few seconds your Google Cloud Platform account will be ready.<br>

For detailed account creation with screenshots visit: https://www.storagetutorials.com/create-free-trial-google-cloud-platform/<br>

Enabling API's
- In the search bar on the Search for API's and Services --> then click on Library --> Search for Cloud Functions, Cloud Run, Cloud Storage, Cloud Build, Cloud Composer and enable them

