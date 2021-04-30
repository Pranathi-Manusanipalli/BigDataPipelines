import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from google.cloud import vision
from google.cloud import storage
from google.cloud.vision_v1 import types
#from google.oauth2 import service_account
import io
import pandas as pd
import re
from io import StringIO
import requests
import json
#import streamlit.components.v1 as components
import hashlib
import pandas_gbq


#credentials = service_account.Credentials.from_service_account_file('/Users/prathyusha/Desktop/pranathi/project_new/bigdata-311523-d08f734796f8.json')

st.set_option('deprecation.showfileUploaderEncoding', False)
CURRENT_THEME = "IS_DARK_THEME"
IS_DARK_THEME = True


# Security
#passlib,hashlib,bcrypt,scrypt
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.title("Invoice Categorization")
		htp7='https://storage.googleapis.com/invoices_image/invoice_receipt_animation.gif'
		st.image(htp7, width=800)

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Bulk Load", "Image Upload","Reports","Invoice Data"])
				if task == "Bulk Load":
					st.title("Bulk Invoice Categorization")
					htp7='https://storage.googleapis.com/invoices_image/invoice_image.png'
					st.image(htp7, caption= 'Invoice Categorization', width=800)
					csv_file_buffer = st.file_uploader("Upload Invoice File", type=["csv"])
					if csv_file_buffer:
						df=pd.read_csv(csv_file_buffer,index_col=0)
						df_print=df.head(5)
						st.dataframe(df_print)
						destination_blob_name = 'new_transactions.csv'
						storage_client = storage.Client()
						bucket = storage_client.bucket('new_transactions')
						blob = bucket.blob(destination_blob_name)
						blob.upload_from_string(df.to_csv(),'text/csv')
						print("File uploaded to {}.".format(destination_blob_name))
						st.write("Batch processing for new transactions is initiated")
						
						#st.subheader("Add Your Post")

				elif task == "Image Upload":
					# Upload an image and set some options for demo purposes
				    st.header("Invoice Categorization")
				    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
				    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
				    #box_color = st.sidebar.beta_color_picker(label="Box Color", value='#0000FF')
				    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
				    aspect_dict = {"1:1": (1,1),
				                    "16:9": (16,9),
				                    "4:3": (4,3),
				                    "2:3": (2,3),
				                    "Free": None}
				    aspect_ratio = aspect_dict[aspect_choice]

				    if img_file:
				        img = Image.open(img_file)
				        if not realtime_update:
				            st.write("Double click to save crop")
				        # Get a cropped image from the frontend
				        cropped_img = st_cropper(img, realtime_update=realtime_update,# box_color=box_color,
				                                    aspect_ratio=aspect_ratio)

				        im1 = cropped_img.save("/tmp/crop_img.jpg")
				        # Manipulate cropped image at will
				        st.write("Preview")
				        _ = cropped_img.thumbnail((150,150))
				        st.image(cropped_img)

				        if st.button('Submit'):
				            st.spinner(text="Image Processing")
				            client = vision.ImageAnnotatorClient()

				            with io.open('/tmp/crop_img.jpg', 'rb') as image_file:
				                content = image_file.read()

				                image = types.Image(content=content)

				                response = client.text_detection(image=image)
				                texts = response.text_annotations
				                data=texts[0].description
				                result = ''.join(re.findall("[a-zA-Z\n'-'' '']+",data))
				                result = StringIO(result)
				                df = pd.read_csv(result, sep ="\n",header=None)
				                df.columns=['Description']
				                df['Description']=df['Description'].replace('$','')
				                desc= list(df['Description'])
				                str=''
				                for i in desc:
				                    str=str+'data={}&'.format(i)
				                str = str.rstrip(str[-1])
				                r = requests.post("https://fastapi-invoice-categorization-ii5x4gm7ra-uc.a.run.app/predict?{}".format(str),timeout=None)
				                a = json.loads(r.text)
				                df['Category']=a['predicted']
				                st.dataframe(df)
				                st.balloons()
				                pandas_gbq.to_gbq(df, 'Invoice_transactions.receipts_data', if_exists='append',project_id='bigdata-311523')


				elif task == "Reports":
					st.markdown("""
    <iframe width="1000" height="850" src="https://datastudio.google.com/embed/reporting/d5320412-115f-415f-959c-c5d87bdcff19/page/1M" frameborder="0" style="border:0" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

				elif task=="Invoice Data":
					st.markdown("""<iframe width="850" height="850" src="https://datastudio.google.com/embed/reporting/d5320412-115f-415f-959c-c5d87bdcff19/page/vSAGC" frameborder="0" style="border:0" allowfullscreen></iframe>""", unsafe_allow_html=True)
			else:
				st.warning("Incorrect Username/Password")



	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
