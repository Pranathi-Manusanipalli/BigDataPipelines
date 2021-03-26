## Training Pipeline
Pipeline to fetch the data from s3 containing the labelled dataset from annotation pipeline and train/fine tune a BERT model using Transfer learning to train on our data and save the model to s3 bucket

## Github Pipeline

Part2_TrainingPipeline/
├── .DS_Store
├── airflow-webserver.err
├── airflow-webserver.log
├── airflow-webserver.out
├── airflow.cfg
├── airflow.db
├── dags/
│   ├── __pycache__/
│   │   └── train.cpython-37.pyc
│   ├── config.yaml
│   ├── train.py
│   └── utils/
│       ├── __pycache__/
│       │   └── utils.cpython-37.pyc
│       └── utils.py
├── logs/
│   ├── dag_processor_manager/
│   │   └── dag_processor_manager.log
│   ├── Model-Training-Pipeline/
│   │   ├── GetData/
│   │   │   ├── 2021-03-23T00:00:00+00:00/
│   │   │   │   ├── 1.log
│   │   │   │   └── 2.log
│   │   │   ├── 2021-03-23T20:24:25.927270+00:00/
│   │   │   │   ├── 1.log
│   │   │   │   └── 2.log
│   │   │   ├── 2021-03-23T20:26:37.123112+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T21:27:22.576507+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T21:38:30.791293+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:13:47.455672+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:19:57.871297+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:33:22.325963+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:39:53.035917+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:49:52.735071+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T22:53:32.603997+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T23:21:15.630127+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T23:28:27.221663+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-23T23:34:21.898848+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T00:14:51.403879+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T00:25:38.944447+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T01:09:58.669939+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T01:15:49.366449+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T04:04:13.645541+00:00/
│   │   │   │   └── 1.log
│   │   │   └── 2021-03-24T04:06:09.175220+00:00/
│   │   │       └── 1.log
│   │   ├── SaveModel/
│   │   │   ├── 2021-03-23T22:53:32.603997+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T00:25:38.944447+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T01:09:58.669939+00:00/
│   │   │   │   └── 1.log
│   │   │   ├── 2021-03-24T01:15:49.366449+00:00/
│   │   │   │   └── 1.log
│   │   │   └── 2021-03-24T04:06:09.175220+00:00/
│   │   │       └── 1.log
│   │   └── TrainBertModel/
│   │       ├── 2021-03-23T21:38:30.791293+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-23T22:53:32.603997+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-23T23:28:27.221663+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-23T23:34:21.898848+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-24T00:14:51.403879+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-24T00:25:38.944447+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-24T01:09:58.669939+00:00/
│   │       │   └── 1.log
│   │       ├── 2021-03-24T01:15:49.366449+00:00/
│   │       │   └── 1.log
│   │       └── 2021-03-24T04:06:09.175220+00:00/
│   │           └── 1.log
│   └── scheduler/
│       ├── 2021-03-23/
│       │   ├── native_dags/
│       │   │   └── example_dags/
│       │   │       ├── example_bash_operator.py.log
│       │   │       ├── example_branch_operator.py.log
│       │   │       ├── example_branch_python_dop_operator_3.py.log
│       │   │       ├── example_complex.py.log
│       │   │       ├── example_dag_decorator.py.log
│       │   │       ├── example_external_task_marker_dag.py.log
│       │   │       ├── example_kubernetes_executor.py.log
│       │   │       ├── example_kubernetes_executor_config.py.log
│       │   │       ├── example_latest_only.py.log
│       │   │       ├── example_latest_only_with_trigger.py.log
│       │   │       ├── example_nested_branch_dag.py.log
│       │   │       ├── example_passing_params_via_test_command.py.log
│       │   │       ├── example_python_operator.py.log
│       │   │       ├── example_short_circuit_operator.py.log
│       │   │       ├── example_skip_dag.py.log
│       │   │       ├── example_subdag_operator.py.log
│       │   │       ├── example_task_group.py.log
│       │   │       ├── example_trigger_controller_dag.py.log
│       │   │       ├── example_trigger_target_dag.py.log
│       │   │       ├── example_xcom.py.log
│       │   │       ├── example_xcomargs.py.log
│       │   │       ├── subdags/
│       │   │       │   └── subdag.py.log
│       │   │       ├── test_utils.py.log
│       │   │       ├── tutorial.py.log
│       │   │       ├── tutorial_etl_dag.py.log
│       │   │       └── tutorial_taskflow_api_etl.py.log
│       │   └── train.py.log
│       ├── 2021-03-24/
│       │   ├── native_dags/
│       │   │   └── example_dags/
│       │   │       ├── example_bash_operator.py.log
│       │   │       ├── example_branch_operator.py.log
│       │   │       ├── example_branch_python_dop_operator_3.py.log
│       │   │       ├── example_complex.py.log
│       │   │       ├── example_dag_decorator.py.log
│       │   │       ├── example_external_task_marker_dag.py.log
│       │   │       ├── example_kubernetes_executor.py.log
│       │   │       ├── example_kubernetes_executor_config.py.log
│       │   │       ├── example_latest_only.py.log
│       │   │       ├── example_latest_only_with_trigger.py.log
│       │   │       ├── example_nested_branch_dag.py.log
│       │   │       ├── example_passing_params_via_test_command.py.log
│       │   │       ├── example_python_operator.py.log
│       │   │       ├── example_short_circuit_operator.py.log
│       │   │       ├── example_skip_dag.py.log
│       │   │       ├── example_subdag_operator.py.log
│       │   │       ├── example_task_group.py.log
│       │   │       ├── example_trigger_controller_dag.py.log
│       │   │       ├── example_trigger_target_dag.py.log
│       │   │       ├── example_xcom.py.log
│       │   │       ├── example_xcomargs.py.log
│       │   │       ├── subdags/
│       │   │       │   └── subdag.py.log
│       │   │       ├── test_utils.py.log
│       │   │       ├── tutorial.py.log
│       │   │       ├── tutorial_etl_dag.py.log
│       │   │       └── tutorial_taskflow_api_etl.py.log
│       │   └── train.py.log
│       └── latest
├── README.md
├── requirements.txt
├── unittests.cfg
└── webserver_config.py

### Requirements - 
Install the dependencies as outlines in the requirements.txt by running 
`pip install -r requirements.txt`

### Configurations
Update the `dasgs/config.yaml` with dynamic parameters for execution of the pipeline as described below
- `bucket` -> your s3 bucket
- `aws_secret_access_key, aws_access_key_id `-> AWS root credentials
- `local_downloaddir` -> local directory where your intial source file needs to be downloaded
from s3
- `s3_sourcefilename` - The source file name in s3 used for training the model
- `s3_target` -> s3 target directory name where you want your model saved
- `saved_model_path`: The directory name where you want the model to be saved in your local

#### Airflow Configuration 
- Use your present working directory as the airflow home
`export AIRFLOW_HOME=~(pwd)`

- export Python Path to allow use of custom modules by Airflow
`export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"`
- initialize the database
`airflow db init`

`airflow users create \
    --username admin \
    --firstname <YourName> \
    --lastname <YourLastName> \
    --role Admin \
    --email example@example.com
`

### Instructions to run
**Run airflow by following these commands**
- Start the airflow server in daemon on port 8081 `airflow webserver -D -p 8081`
- Start the scheduler 
` airflow scheduler`
Once both are running , you can access the UI by visting http://127.0.0.1:8080/home on your browser.
- To kill the web server
    - `lsof -i tcp:8081`
    It shows a list of processes with PIDs
    - `kill <PID>` to kill the process
- Once you login to Airflow on the browser, run the DAG 'Model-Training-Pipeline'
- Once the pipeline is run successfully, the model is saved in the specified path in the s3 bucket.

#### CLAT document - 
Refer to https://codelabs-preview.appspot.com/?file_id=1jCLBg9N-M6sL1eEP3I5kE4cvZVNoPEeiTT1aiGq8qdY#0 for detailed report on the sentiment model
