# EvaDB Project 1

The directory of the project is in the `evadb-venv` folder.

## Setup
After installing the prerequisite libraries using pipenv, run `python -m run_evadb` to test out the program.

## How to use/Input
The program will ask you for an OpenAI key, after which, it will ask you for the name of the company. It will also ask you to input a sequence of categories. These categories are simply the type of news you'd like to reference, for example, `Layoff` would include news articles about layoffs from the company. There is bias based on your input, so make sure to choose accordingly. Inputting `end` will terminate your input and start the program. The default tags are `Layoff`, `Economy`, and `Financial`.

## Notes
The program uses Google to scrape, so you may get timed out occasionally.