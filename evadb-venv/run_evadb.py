import evadb
from DataFetcher import DataFetcher
import csv
import pandas as pd
import os
import openai
from collections import defaultdict

class LayoffPredictor:

    def __init__(self):

        os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key: ")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        COMPANY_NAME = input("Enter the name of the company you would like to analyze: ")

        #grab this from input
        data_types = []
        curr_type = ""
        while True:
            curr_type = input(f"Enter a search prompt (eg. {COMPANY_NAME} layoffs, {COMPANY_NAME} financials and funding, etc.), type 'end' to stop: ")
            if curr_type == "end" or len(curr_type) == 0:
                break
            data_types.append(curr_type)

        if len(data_types) == 0:
            data_types = [f"{COMPANY_NAME} layoffs", f"{COMPANY_NAME} financials and funding", f"{COMPANY_NAME} hiring"]

        fetcher = DataFetcher()
        data = []
        for data_type in data_types:
            for d in fetcher.get_data(COMPANY_NAME, str(data_type)):
                data.append(d)

        if (len(data) == 0):
            print("There was an error fetching data, please try again (time out).")
            return

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
        for index, row in data_frame.iterrows():
            response = row['response']
            if 'positive' in response.lower():
                counter[0] += 1
            elif 'negative' in response.lower():
                counter[1] += 1
            else:
                counter[2] += 1

        print(f"Sentiment Analysis Results: {counter[0]} positive, {counter[1]} negative, {counter[2]} neutral/unsure")
        print(f"This company is {round(counter[1] / (counter[0] + counter[1] + counter[2]) * 100, 2)}% likely to layoff employees in the near future.")
        if round(counter[1] / (counter[0] + counter[1] + counter[2]) * 100, 2) > 0:
            data_frame = cursor.table("Headers").select("ChatGPT('Assuming that this company will conduct layoffs in the future, based on this headline, how many employees will they fire and what department will be affected? Format your responses as: Engineering 15. Do not respond with anything else, if you are not sure, make your best guess.', header)").df()
            dept_map = defaultdict(int)
            for index, row in data_frame.iterrows():
                response = row['response']
                if len(response.lower().split(' ')) == 2 and response.lower().split(' ')[1].strip().isdigit():
                    dept_map[response.lower().split(' ')[0].strip()] += int(response.lower().split(' ')[1].strip())
            if len(dept_map) > 0:
                print(f"Most likely department to be affected: {max(dept_map, key=dept_map.get)}")
                print(f"Estimated number of layoffs: {dept_map[max(dept_map, key=dept_map.get)]}")
            else:
                print("Insufficient data to determine department and number of layoffs. Please try again.")

LayoffPredictor()