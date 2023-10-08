import evadb
from DataFetcher import DataFetcher
import csv
import pandas as pd
import os

class LayoffPredictor:

    def __init__(self):

        os.environ["OPENAI_KEY"] = input("Enter your OpenAI API key: ")
        COMPANY_NAME = input("Enter the name of the company you would like to analyze: ")

        fetcher = DataFetcher()
        data = fetcher.get_data(COMPANY_NAME, "Financial")
        for d in fetcher.get_data(COMPANY_NAME, "Layoff"): data.append(d)
        for d in fetcher.get_data(COMPANY_NAME, "Economy"): data.append(d)

        with open('./headers.csv', 'w', newline='') as file:
            fieldname = ['header']
            writer = csv.DictWriter(file, fieldnames=fieldname)
            writer.writeheader()
            for data in data:
                writer.writerow({ 'header': data })


        cursor = evadb.connect().cursor()
        cursor.drop_table("Headers", if_exists=True).execute()
        cursor.query(
            """CREATE TABLE IF NOT EXISTS Headers (header TEXT(100));"""
        ).execute()
        cursor.load('./headers.csv', "Headers", 'csv').execute()

        data_frame = cursor.table("Headers").select("ChatGPT('Determine if the following text is positive or negative towards a company, respond only with yes or no. If you are unsure or are unable to determine the sentiment, just say no.', header)").df()

        counter = [0, 0, 0]
        for response in data_frame['chatgpt.response']:
            if 'yes' in response.lower():
                counter[0] += 1
            elif 'no' in response.lower():
                counter[1] += 1
            else:
                counter[2] += 1

        print(f"Sentiment Analysis Results: {counter[0]} positive, {counter[1]} negative, {counter[2]} neutral/unsure")
        print(f"This company is {round(counter[0] / (counter[0] + counter[1] + counter[2]) * 100, 2)}% likely to layoff employees in the near future.")


LayoffPredictor()