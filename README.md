# robo-advisor

(description based on rock-paper-scissors-exercise from Corbin Beckerman)

This is a python based code for a robo stock advisor. Follow the instructions for instillation and use.

## Set-up

First, you need to create and activate a specific Anaconda environment. Do so through the following method in the command line:

```sh
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```

Once the environment is set up, you will then need to install certain packages. Do so by executing the following code, also in the command line:

```sh
pip install -r requirements.txt
```

At this point, you will need to create an environment variable. Create a new variable, call it .env, and place the following into it, replacing "abc123" with your own, specific API key.

```sh
ALPHAVANTAGE_API_KEY="abc123"
```

## Usage

Start the program by putting the following command into the command line:

```py
python app/robo_advisor.py
```

Once that command is entered, follow the instructions accordingly- there is an initial instruction that has more details.
Your csv files will show up in your external editor and on your computer. Happy investing!