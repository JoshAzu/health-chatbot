import tkinter as tk
import os
import json
import datetime

from tkinter import *
from tkinter import scrolledtext ,ttk
from google import genai
from google.genai import types
from pydantic import BaseModel
from pathlib import Path

# Import environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Set up Pydantic Data Types for response schema
class FoodType(BaseModel):
    name: str
    calories: int

class ChatResponse(BaseModel):
    response: str
    foods: list[FoodType]

# Define a function to check tracker.json file
def check_tracker_json():
    
    # Change working directory to script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Check tracker.json file
    file_path = "tracker.json"
    json_file = Path(file_path)

    if json_file.is_file():
        return True
    else:
        return False

# Define a function to update tracker.json
def update_tracker_json(foods_parsed, date_today):
    file_path = "tracker.json"

    # If tracker.json file exists, load the json file
    if check_tracker_json():
        with open(file_path, mode = "r+") as read_file:
            tracker_json = json.load(read_file)

            # If today has not been recorded in the json file, create new entry
            if str(date_today) not in tracker_json:
                foods_list = []
                for row in foods_parsed:
                    foods_list.append(row)
                tracker_json[date_today] = foods_list
                read_file.seek(0)
                json.dump(tracker_json, read_file, indent = 2)

            # If today has already been recorded in the json file, append the entry
            else:
                for row in foods_parsed:
                    tracker_json[date_today].append(row)
                read_file.seek(0)
                json.dump(tracker_json, read_file, indent = 2)

    # If tracker.json file does not exists, create new json file
    else:
        foods_list = []
        for row in foods_parsed:
            foods_list.append(row)
        tracker_json = {
            date_today:foods_list
        }

        # Write data into new json file
        with open(file_path, mode = "w") as out_file:
            json.dump(tracker_json, out_file, indent = 2)

# Define a function to clear table tabs
def clear_notebook_tabs(notebook):
    for tab_name in notebook.tabs():
        notebook.forget(tab_name)

# Define a function to update gui table
def update_table():

    # Clear table tabs in notebook object
    clear_notebook_tabs(notebook)

    file_path = "tracker.json"

    # Read tracker.json file and print foods into table
    with open(file_path, mode = "r+") as read_file:
        tracker_json = json.load(read_file)
        for x in tracker_json:

            # Create tabs for each entry in tracker.json
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text = str(x))
            table = ttk.Treeview(tab_frame, columns = ("name", "calories"), show = "headings")
            table.heading("name", text = "Food Name")
            table.heading("calories", text = "Estimated Calories")
            table.pack(expand = True, fill = "both")

            # Insert data from tacker.json entry into table tabs
            for row in tracker_json[x]:
                table.insert(parent = "", index = 0, values = (row["name"], row["calories"]))

    # Select tab for current day
    tab_index = int(len(notebook.tabs())) - 1
    notebook.select(tab_index)

# Define a function to update calorie counter
def update_calorie_counter(date_today):
    file_path = "tracker.json"

    # Read tracker.json file and sum up calories for the day
    with open(file_path, mode = "r+") as read_file:
        tracker_json = json.load(read_file)

        # Check if today has been recorded
        if str(date_today) in tracker_json:
            calorie_sum = 0
            for row in tracker_json[date_today]:
                calories = int(row['calories'])
                calorie_sum += calories
            text_var.set("Daily Calories: " + str(calorie_sum))

# Define a function to send Gemini requests and return responses
def send(event = None):

    # Retrieve input field message and append to chat log
    msg = chat_input.get()
    chat_input.delete(0, tk.END)
    chat.config(state = "normal")
    chat.insert(tk.END, "You: " + msg + "\n\n")

    # Create Gemini request with inputted message
    response = client.models.generate_content(
        model=model_name,
        contents=msg,
        config=types.GenerateContentConfig(
            response_mime_type = "application/json",
            response_schema = ChatResponse,
            system_instruction="You are Rock, an AI Health Coach. Be friendly, encouraging, and informative. When the user mentions a food they have eaten, your primary task is to identify it, estimate its calories, and include this data in your response. Reply in a valid JSON format that can easily be parsed in python. When you respond, acknowledge the food and seamlessly integrate your health advice. If the user's message does not contain any food, make the 'food' field in your JSON response null."
        )
    )

    # Get parsed response from json response
    response_json = json.loads(response.text)
    response_parsed = response_json["response"]
    foods_parsed = response_json["foods"]

    # Get current date
    date = datetime.datetime.now()
    date_today = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

    # Check if last message included food
    if foods_parsed:
        update_tracker_json(foods_parsed, date_today)
        update_table()
        update_calorie_counter(date_today)

    # Append response to chat log
    chat.insert(tk.END, "Coach: " + response_parsed + "\n\n")
    chat.config(state = "disabled")

# Define a function to update calorie counter when selecting recorded days
def select_tab(event):
    selected_tab = notebook.select()
    selected_tab_text = notebook.tab(selected_tab, "text")
    update_calorie_counter(selected_tab_text)

# Configure Gemini AI Client
model_name = "gemini-2.5-pro"
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Configure GUI
root = tk.Tk()
root.title("AI Health Coach")
root.geometry("800x800")

text_var = tk.StringVar()
text_var.set("Daily Calories: ")
calorie_count = tk.Label(root, textvariable=text_var)
calorie_count.pack()

chat = scrolledtext.ScrolledText(root, width = 100, height = 30, state="disabled")
chat.pack()

input_frame = tk.Frame(root)
input_frame.pack()

chat_input = tk.Entry(input_frame, width = 50)
chat_input.pack(side = LEFT)

submit_button = tk.Button(input_frame, text = "Send", command = send)
submit_button.pack(side = LEFT)

notebook = ttk.Notebook(root)
notebook.pack(expand = True, fill = "both")
notebook.bind("<<NotebookTabChanged>>", select_tab)

# Get current date
date = datetime.datetime.now()
date_today = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

# Check if tracker.json is present before updating gui elements
if check_tracker_json():
    update_table()
    update_calorie_counter(date_today)

# Bind return key to send command
root.bind("<Return>", send)

# Start Tkinter Main Loop
root.mainloop()