from fastapi import FastAPI
from v1.routers import router
from mangum import Mangum

app = FastAPI(title='Sentiment Analysis',
              description='Sentiment Analysis')
app.include_router(router, prefix="/v1")


@app.get("/")
def read_root():
    return {"Welcome to FastAPI"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
