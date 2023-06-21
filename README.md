# thai_text_summarization
Thai text summarization (test)

# directories
~~~
./
　├ venv/
　├ data/
　├ model/
　├ text_summarization.ipynb
　├ TextSum_train.ipynb
　├ requirements.txt
　├ run.sh
　└ main.py
~~~

- `venv`: Python 3.9.13 virtual environment (not exist in GitHub). Please install libraries according to requirements.txt.
- `data`: abbrev.csv is used for preprocessing text. (Source - https://github.com/PyThaiNLP/lexicon-thai/tree/master/thai-abbreviation)
- `model`: pytorch_model does not exist in Github, since the file is too large (1.2 GB). Please download the model from this [link](https://drive.google.com/file/d/1-4CTXn1ly_CVRRDka30uqcyCX5ALAZf7/view?usp=share_link), and put it in folder `model`
- `TextSum_train.ipynb` : code for preprocessing and fine-tuning model
- `main.py` : main program for API

# how to run API
~~~
$ source run.sh
INFO:     Started server process [91802]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8789 (Press CTRL+C to quit)
