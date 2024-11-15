import os
import sys
from dotenv import load_dotenv
import certifi
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import pandas as pd
import pymongo

from fastapi.responses import Response

from starlette.responses import RedirectResponse

from network_security.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.util.main_utils.utils import load_object
from network_security.util.ml_utils.model.estimator import NetworkModel

ca = certifi.where()
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["Authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return Response("Training successful !!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(
    request: Request,
    file: UploadFile = File(...),
):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_models/preprocessor.pkl")
        model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor, model)
        y_pred = network_model.predict(df)
        df["prediction"] = y_pred

        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes="table table-striped")

        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table": table_html,
            },
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
