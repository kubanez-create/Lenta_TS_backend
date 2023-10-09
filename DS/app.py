import asyncio
import json
import os
import pickle

import aiohttp
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

with open("/app/data/df_test.pkl", "rb") as df:
    df_test = pickle.load(df)
with open(
    '/app/data/features_test.pkl', 'rb') as f:
    features_test = pickle.load(f)
with open('/app/data/target_test.pkl', 'rb') as t:
    target_test = pickle.load(t)
with open(
    '/app/data/catboost_model_40.0.pkl', 'rb') as m:
    model = pickle.load(m)

predictions = model.predict(features_test)

df_to_endpoint = pd.DataFrame()
df_to_endpoint[['st_id', 'date', 'pr_sku_id']] = df_test[['st_id', 'date', 'pr_sku_id']]
df_to_endpoint['sales_units'] = predictions

# День прогноза
today='2023-07-05'

# Создания словаря result_main
def result_gen(row, today):

    result = []
    store = row['st_id']
    product = row['pr_sku_id']
    forecast_date = pd.to_datetime(row['date']).date().isoformat()  # .strftime('%m/%d/%Y')
    prediction_sales = row['sales_units']

    result.append({'store': store,
                   'forecast_date': today,
                   'forecast': {
                        'sku': product,
                        'sales_units': {forecast_date: prediction_sales}
                        }
                    }
                )

    return result

result_main = df_to_endpoint.apply(result_gen, today=today, axis = 1)

async def get_token():
    url = "http://host.docker.internal:8000/api/v1/auth/token/login/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD")
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_response = await response.json()
            return json_response['auth_token']

async def send_post_request(token, pred_list):
    url = "http://host.docker.internal:8000/api/v1/forecast/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token}"
    }
    for value in pred_list:
        data = {"data": value}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                pass

async def main():
    token = await get_token()
    await send_post_request(token, result_main)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
