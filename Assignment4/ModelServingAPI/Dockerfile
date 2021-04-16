FROM python:3.7-slim



COPY . /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD [  "main.py" ]