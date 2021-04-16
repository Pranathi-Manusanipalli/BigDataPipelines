
import requests
import streamlit as st
import pandas as pd
import io
import boto3
import json
import altair as alt
from boto3.dynamodb.conditions import Key


st.set_option("deprecation.showfileUploaderEncoding", False)
# s3://prudhvics/sec-edgar/call_transcripts/AGEN
#s3://prudhvics/api3_masked/727520526624-PII-33d84d43ff4a2e0ac042122f3f6e182d/output/anonymized.txt.out



choice = st.sidebar.selectbox("Choose a page", ["File Analysis", "Sentiment Analysis","Get PII Entities"])

if choice == "File Analysis":
    bgcolor="#010000"
    fontcolor = "#fff"
    st.title("File Analysis")
    user_input = st.text_input("S3 url")
    token = st.text_input("Authentication token")
    if st.button("Submit"):
        head = {'Authorization': 'Bearer ' + token}
        r = requests.get("https://w1q69ke9j0.execute-api.us-east-1.amazonaws.com/DEV/v1/api2?url={}".format(user_input),headers=head)
        a = json.loads(r.text)
        df=pd.DataFrame(a['Entities'])
        st.dataframe(df)
        s = df['Type'].value_counts() ## Counts the occurrence of unqiue elements and stores in a variable called "s" which is series type
        new = pd.DataFrame({'Type':s.index, 'Count':s.values})
        basic_chart=alt.Chart(new).mark_line().encode(x='Type',y="Count").properties(title='Entities Counts',width=800,height=500)
        st.altair_chart(basic_chart)

if choice == "Get PII Entities":
    #users = pass_data['Customer_ID'].unique().tolist()
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type = 'password')
    # path= 's3://AKIAJV5PIUOIYOJJ3VEQ:LfR3OY+MWpXjZ91yTUK8I0MCmsCTOHzoHgAdGaoQ@prudhvics/usersdata/users.csv'
    # pass_data = pd.read_csv(smart_open(path),sep=',', encoding="utf8",header=0)
    s3c = boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ',
        aws_secret_access_key='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'
    )

    obj = s3c.get_object(Bucket='prudhvics', Key='usersdata/users.csv')
    pass_data = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
    x=pass_data[pass_data['user_ID']==username]
    lbtn=st.sidebar.button("Login")
    if lbtn:
        if x.empty:
            st.warning("Invalid User Name/Password")

        elif(username==""):
            st.warning("User Name cannot be empty")
        elif(password==""):
            st.warning("Password cannot be empty")
        elif((x.iloc[0].user_ID==username) & (x.iloc[0].Password==password)):
            st.success("Logged in as {}".format(username))
            st.subheader("Hash Keys Data:")
            dynamodb = boto3.resource('dynamodb',region_name='us-east-1',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
            #obj = pd.DataFrame(dynamo_json.loads(data))
            table = dynamodb.Table('anonymize_table')
            print(table.item_count)
            resp = table.scan(ProjectionExpression="messagekey,#sources,#Texts,#types",ExpressionAttributeNames = {"#sources": "source","#Texts" : "Text","#types" : "type"})
            print(resp)
            print(resp['Items'])
            item=resp['Items']
            final_df=pd.DataFrame(item)
            st.dataframe(final_df)
        elif((x.iloc[0].user_ID!=username) | (x.iloc[0].Password!=password)):
            st.warning("Invalid User Name/Password")


elif choice =="Sentiment Analysis":
    # defines an h1 header
    st.title("Sentiment Analysis")
    user_input = st.text_input("S3 url")
    if st.button("Submit"):
        r = requests.get("http://localhost:8000/get_prediction?s3_url={}".format(user_input),timeout=None)
        a = json.loads(r.text)
        final_df=pd.DataFrame(a)
        st.dataframe(final_df)
        #st.dataframe(final_df)

