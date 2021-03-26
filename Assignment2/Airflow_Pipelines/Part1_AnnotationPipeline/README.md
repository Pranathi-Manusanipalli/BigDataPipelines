Annotation Pipeline
This pipeline aims to predict sentiments for each sentence in a list of company earnings call transcripts

![Pipeline](/images/pipeline.png)

Requirements -
Install the dependencies as outlines in the requirements.txt by running pip install -r requirements.txt

Configurations
Update the dags/config.yaml with dynamic parameters for execution of the pipeline as described below

bucket -> your s3 bucket
filepath -> local directory where your intial source files are present and are uploaded to s3
downloadpath -> root directory path to download files
fetchpath -> local directory where your files are downloaded from s3 and stored
APIKey -> API key for accesing Microsoft Cognitive Service 

Airflow Configuration
Use your present working directory as the airflow home export AIRFLOW_HOME=~(pwd)

export Python Path to allow use of custom modules by Airflow export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"

initialize the database airflow db init

airflow users create \ --username admin \ --firstname <YourName> \ --lastname <YourLastName> \ --role Admin \ --email example@example.com

Instructions to run
Run airflow by following these commands

- Start the airflow server in daemon on port 8081 airflow webserver -D -p 8081 <br/>
- Start the scheduler airflow scheduler Once both are running , you can access the UI by visting http://127.0.0.1:8080/home on your browser. <br/>
- To kill the web server <br/>
lsof -i tcp:8081 It shows a list of processes with PIDs <br/>
kill PID to kill the process <br/>
Once you login to Airflow on the browser, run the DAG 'Model-Training-Pipeline' <br/>
Once the pipeline is run successfully, the model is saved in the specified path in the s3 bucket. <br/>
CLAT document - <br/>
Refer to https://codelabs-preview.appspot.com/?file_id=1jCLBg9N-M6sL1eEP3I5kE4cvZVNoPEeiTT1aiGq8qdY#0 for detailed report on the creating an annotation pipeline
