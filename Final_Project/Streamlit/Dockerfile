FROM python:3.8-slim-buster
COPY . /streamlit
WORKDIR /streamlit
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT [ "streamlit","run" ]
CMD [  "streamtest.py" ]