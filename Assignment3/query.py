from snowflake_connect import snowflake_connect
import json
def snowflake_query(sql):
    conn=snowflake_connect()
    cur = conn.cursor()
    # Execute a statement that will generate a result set.
    df=cur.execute(sql)
    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    df = cur.fetch_pandas_all()
    
    return df

# def test():
#     sql= "SELECT dataset_type, MAX(time_in_cycles) as count from TRAIN_TEST where unit_number=1 AND fault='FD001' GROUP BY dataset_type order by dataset_type desc"
#     df = snowflake_query(sql)
#     # print(df['COUNT'][0])
#     # return {'train':df['COUNT'][0],'test':df['COUNT'][1]}
#     # print(df.to_dict('list'))
#     result = {'train':str(df['COUNT'][0]),'test':str(df['COUNT'][1])}
#     print(json.loads(json.dumps(result)))

# test()