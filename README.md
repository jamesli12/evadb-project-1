# Layoff Prediction App

The directory of the project is in the `evadb-venv` folder.

## Setup
After installing the prerequisite libraries using pipenv, run `python -m run_evadb` to test out the program. There is a `requirements.txt` file for you to use, it contains the libraries **on top** of EvaDB that you will need.

## How to use/Input
The program will ask you for an OpenAI key, after which, it will ask you for the name of the company. It will then prompt you for a series of search queries, the more queries you provide, the more accurate the program will be when determining layoffs. There is bias based on your input, so make sure to choose accordingly. Inputting `end` will terminate your input and start the program. The default searches are "COMPANY_NAME layoffs", "COMPANY_NAME financials and funding", and "COMPANY_NAME hiring".

## Notes
The program uses Google to scrape, so you may get timed out occasionally.
The program now uses DataFetcher as an integrated EvaDB function, and the `CREATE FUNCTION IF NOT EXISTS DataFetcher IMPL './evadb-venv/DataFetcher.py` line in `run_evadb.py` references the `DataFetcher.py` file. Since I run the program in the root directory, there isn't a problem. However, if you're running the project from a different directory, you may have to change this line for it to reference the function properly.

## Sample Flow
![image](https://github.com/jamesli12/layoff_prediction_app/assets/19893822/299f91ca-7ae3-4ed7-9438-f00b4303214f)

