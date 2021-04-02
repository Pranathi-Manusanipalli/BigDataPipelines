import snowflake.connector as snow
import pandas as pd

def snowflake_connect():
    conn = snow.connect(user="prudhvics",
                        password="Prudhvi_43",
                        account="tx62478.us-central1.gcp",
                        database="NASA_CMAPS",
                        schema="DEV",
                        warehouse="CMAPS")

    return conn
