from fastapi import FastAPI
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import Security, Depends, FastAPI, HTTPException
from snowflake_connect import snowflake_connect
from query import snowflake_query
import json
from typing import Optional
import os
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import secrets

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# API_KEY = "a"
API_KEY_NAME = "access_token"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

app = FastAPI()
conn=snowflake_connect()
def get_api_key(
    api_key_query: str = Security(api_key_query)):
    if api_key_query == os.getenv('API_KEY'):
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
auto_error=False

fake_users_db = {
    "tom": {
        "username": "Tom",
        "full_name": "Tom",
        "email": "tom@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    },
    "sam": {
        "username": "sam",
        "full_name": "Sam Anders",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user



async def get_current_user(token: str = Depends(oauth2_scheme)):

    user = fake_decode_token(token)

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid authentication credentials",

            headers={"WWW-Authenticate": "Bearer"},

        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):

    if current_user.disabled:

        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

@app.get("/")
def root():
    return{"message":"Welcome to NASA Turbofan Jet Engine Data"}


@app.post("/generatetoken")
async def generatetoken(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    os.environ['API_KEY']=secrets.token_urlsafe()
    return os.getenv('API_KEY')
    # return {"access_token": user.username, "token_type": "bearer"}

@app.post("/pipeline/config")
def start_server(api_key: APIKey = Depends(get_api_key)):
    os.system('airflow webserver -D')
    os.system('airflow scheduler -D')
    # Return the issue & confidence
    return {"Airflow Webserver & Scheduler Started"}

@app.post("/pipeline/start")
def start_pipeline(api_key: APIKey = Depends(get_api_key)):
    run_details = os.system('airflow dags trigger CMAPS_SNOWFLAKE_INGESTION')
    # Return the issue & confidence
    return {"status": "Airflow Pipeline Started", "details": run_details}

@app.get("/cycles")
def getcycles(unit_number:str, fault:str,api_key: APIKey = Depends(get_api_key)):
    sql= "SELECT dataset_type, MAX(time_in_cycles) as count from TRAIN_TEST where unit_number='{}' AND fault='{}' GROUP BY dataset_type order by dataset_type desc".format(unit_number,fault)
    df = snowflake_query(sql)
    result = {'train_cycles':int(df['COUNT'][0]),'test_cycles':int(df['COUNT'][1])}
    # return json.dumps(json.loads(df.to_json(orient="records")))
    return json.loads(json.dumps(result))

@app.get("/rul")
def fetchrul(unit_number:str,fault:Optional[str] = None,api_key: APIKey = Depends(get_api_key)):
    if fault:
        sql= "SELECT unit_number,fault,RUL FROM RUL where unit_number='{}' and fault='{}'".format(unit_number,fault)
        df_fault = snowflake_query(sql)
        return json.loads(df_fault.to_json(orient='records'))
    else:
        sql="SELECT unit_number,RUL,fault FROM RUL where unit_number='{}'".format(unit_number)
        df=snowflake_query(sql)
        return json.loads(df.to_json(orient='records'))
    
@app.get("/engine/operational_data")
def fetchoperationaldata(unit_number:str,dataset_type:str,fault:Optional[str] = None,api_key: APIKey = Depends(get_api_key)):
    if fault:
        sql= "SELECT fault,unit_number,time_in_cycles,operational_setting_1, operational_setting_2, operational_setting_3 FROM TRAIN_TEST where unit_number='{}' and fault='{}' and dataset_type='{}'".format(unit_number,fault,dataset_type)
        df_fault = snowflake_query(sql)
        return json.loads(df_fault.to_json(orient='records'))
    else:
        sql="SELECT fault,unit_number,time_in_cycles,operational_setting_1, operational_setting_2, operational_setting_3 FROM TRAIN_TEST where unit_number='{}' and dataset_type='{}'".format(unit_number,dataset_type)
        df=snowflake_query(sql)
        return json.loads(df.to_json(orient='records'))
        
@app.get("/engine/sensordata")
def fetchsensordata(unit_number:str,dataset_type:str,fault:Optional[str] = None,api_key: APIKey = Depends(get_api_key)):
    if fault:
        sql= "SELECT fault,unit_number,time_in_cycles,sensor_measurement_1, sensor_measurement_2, sensor_measurement_3,sensor_measurement_4,sensor_measurement_5,sensor_measurement_6,sensor_measurement_7,sensor_measurement_8,sensor_measurement_9,sensor_measurement_10,sensor_measurement_11,sensor_measurement_12,sensor_measurement_13,sensor_measurement_14,sensor_measurement_15,sensor_measurement_16,sensor_measurement_17,sensor_measurement_18,sensor_measurement_19,sensor_measurement_20,sensor_measurement_21 FROM TRAIN_TEST where unit_number='{}' and fault='{}' and dataset_type='{}'".format(unit_number,fault,dataset_type)
        df_fault = snowflake_query(sql)
        return json.loads(df_fault.to_json(orient='records'))
    else:
        sql="SELECT fault,unit_number,time_in_cycles,sensor_measurement_1, sensor_measurement_2, sensor_measurement_3,sensor_measurement_4,sensor_measurement_5,sensor_measurement_6,sensor_measurement_7,sensor_measurement_8,sensor_measurement_9,sensor_measurement_10,sensor_measurement_11,sensor_measurement_12,sensor_measurement_13,sensor_measurement_14,sensor_measurement_15,sensor_measurement_16,sensor_measurement_17,sensor_measurement_18,sensor_measurement_19,sensor_measurement_20,sensor_measurement_21 FROM TRAIN_TEST where unit_number='{}' and dataset_type='{}'".format(unit_number,dataset_type)
        df=snowflake_query(sql)
        return json.loads(df.to_json(orient='records'))



