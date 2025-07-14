import tkinter as tk

from tkinter import *
from tkinter import scrolledtext ,ttk

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

submit_button = tk.Button(input_frame, text = "Send")
submit_button.pack(side = LEFT)

notebook = ttk.Notebook(root)
notebook.pack(expand = True, fill = "both")

# Start Tkinter Main Loop
root.mainloop()