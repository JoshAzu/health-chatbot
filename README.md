# AI Health Coach Chatbot

This is a simple AI chatbot capable of tracking daily calorie intake by estimating the calories of foods you mention in conversation. 

It is a simple python script that uses the Google Gemini API in order to make LLM requests and displays the responses on a Tkinter interface. This response is then parsed to store past foods mentioned into a json file that can be viewed whenever. 

Daily colorie total for the selected day is shown at the top, and foods previously mentioned in conversation, alongside their estimated calories are displayed at the bottom, organized by day.


## Installation

First, clone the repository. Once cloned, create a .env file, with your Google Gemini API key inside using the format:

```bash
  GEMINI_API_KEY = "YOUR API KEY"
```

Place your .env file in the project folder

Next, create a virtual python environment using Python 3.13.5

On your python terminal, cd into the project folder and install all the dependencies using:

```bash
  pip install -r requirements.txt
```

After installation, run the python script using:

```bash
  python main.py
```
