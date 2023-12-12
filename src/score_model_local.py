import os
import glob
import pandas as pd
import numpy as np
import json
import joblib
from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


def init():
    global model
    model_path = "trained_models/model.pkl"
    model = joblib.load(model_path)

input_sample = pd.DataFrame(data=[{
    "Per_capita_income": 57123,
    "Percent_unemployed": 5.2,
    "Percent_without_diploma": 4.5,
    "Percent_households_below_poverty": 7.5,
    "Ward": 47,
    "ZIP": 60618,
    "Police_District": 19,
    "Unit_ID": 502,
    "Violation_ID": 26,
    "Issued_year": 2010,
    "Time_of_day": "Evening",
    "License_plate_origin": "Out-of-state",
    "Vehicle_type": "PAS",
    "Community_Name": "North Center",
    "Sector": "Other N/NW Side",
    "Side": "North Side",
    "Neighborhood": "NC2"
}])

output_sample = np.array([0])

@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    pred = model.predict(data)
    return pred.tolist()
