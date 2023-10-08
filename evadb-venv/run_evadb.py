import evadb
from DataFetcher import DataFetcher
import csv
import pandas as pd
import os

class LayoffPredictor:

    def __init__(self):

        os.environ["OPENAI_KEY"] = input("Enter your OpenAI API key: ")
        COMPANY_NAME = input("Enter the name of the company you would like to analyze: ")

        #grab this from input
        data_types = []
        curr_type = ""
        while True:
            curr_type = input("Enter the category of data you'd like to analyze (Layoff, Economy, Financial), type 'end' to stop: ")
            if curr_type == "end" or len(curr_type) == 0:
                break
            data_types.append(curr_type)

        if len(data_types) == 0:
            data_types = ["Layoff", "Economy", "Financial"]

        fetcher = DataFetcher()
        data = []
        for data_type in data_types:
            for d in fetcher.get_data(COMPANY_NAME, str(data_type)):
                data.append(d)

        with open('./headers.csv', 'w', newline='') as file:
            fieldname = ['header']
            writer = csv.DictWriter(file, fieldnames=fieldname)
            writer.writeheader()
            for d in data:
                writer.writerow({ 'header': d })

        cursor = evadb.connect().cursor()
        cursor.drop_table("Headers", if_exists=True).execute()
        cursor.query(
            """CREATE TABLE IF NOT EXISTS Headers (header TEXT(100));"""
        ).execute()
        cursor.load('./headers.csv', "Headers", 'csv').execute()

        data_frame = cursor.table("Headers").select("ChatGPT('Is the following header positive or negative? Respond only with positive or negative. Here are examples: company lays off: negative, company hires 100 new employees: positive. If you are unsure or are unable to determine the sentiment, just say unsure.', header)").df()
        counter = [0, 0, 0]
        for response in data_frame['chatgpt.response']:
            if 'positive' in response.lower():
                counter[0] += 1
            elif 'negative' in response.lower():
                counter[1] += 1
            else:
                counter[2] += 1

        print(f"Sentiment Analysis Results: {counter[0]} positive, {counter[1]} negative, {counter[2]} neutral/unsure")
        print(f"This company is {round(counter[1] / (counter[0] + counter[1] + counter[2]) * 100, 2)}% likely to layoff employees in the near future.")


LayoffPredictor()