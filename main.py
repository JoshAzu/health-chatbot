import tkinter as tk
import os
import json

from tkinter import *
from tkinter import scrolledtext ,ttk
from google import genai
from google.genai import types
from pydantic import BaseModel

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
    print(foods_parsed)

    # Append response to chat log
    chat.insert(tk.END, "Coach: " + response_parsed + "\n\n")
    chat.config(state = "disabled")

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

# Bind return key to send command
root.bind("<Return>", send)

# Start Tkinter Main Loop
root.mainloop()