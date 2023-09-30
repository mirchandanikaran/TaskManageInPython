import tkinter as tk
from tkinter import messagebox
import pandas as pd
import datetime
import tkcalendar
from tkinter import simpledialog

# Create a list to store tasks
tasks = []

# Priority options
priority_options = ["P1", "P2", "P3", "P4"]

# Create the main application window
root = tk.Tk()
root.title("Task Manager")

# Create a heading label
heading_label = tk.Label(root, text="Task Manager", font=("Helvetica", 16))
heading_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Create input fields for task heading and task remarks
task_heading_label = tk.Label(root, text="Task Heading:")
task_heading_entry = tk.Entry(root, width=40)
task_heading_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
task_heading_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

task_remarks_label = tk.Label(root, text="Task Remarks:")
task_remarks_entry = tk.Entry(root, width=40)
task_remarks_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
task_remarks_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

# Create a dropdown menu for priority
priority_label = tk.Label(root, text="Priority:")
priority_var = tk.StringVar()
priority_var.set(priority_options[0])
priority_menu = tk.OptionMenu(root, priority_var, *priority_options)
priority_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
priority_menu.grid(row=3, column=1, padx=10, pady=5)

# Create a Calendar widget for selecting due dates
due_date_label = tk.Label(root, text="Due Date:")
due_date_calendar = tkcalendar.Calendar(root)
due_date_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
due_date_calendar.grid(row=5, column=1, columnspan=3, padx=10, pady=5)

# Create an input field for categories
category_label = tk.Label(root, text="Category:")
category_entry = tk.Entry(root, width=20)
category_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
category_entry.grid(row=6, column=1, columnspan=3, padx=10, pady=5)

# Create buttons
def add_task():
    task_heading = task_heading_entry.get()
    task_remarks = task_remarks_entry.get()
    priority = priority_var.get()
    category = category_entry.get()
    due_date = due_date_calendar.get_date()

    if task_heading:
        task = {"Sequence": len(tasks) + 1, "Heading": task_heading, "Remarks": task_remarks,
                "Priority": priority, "Category": category, "Due Date": due_date}
        tasks.append(task)
        update_task_listbox()
        task_heading_entry.delete(0, tk.END)
        task_remarks_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        due_date_calendar.delete(0, tk.END)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=4, column=0, padx=10, pady=10)

def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        index = selected_task[0]
        del tasks[index]
        update_task_listbox()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=4, column=1, padx=10, pady=10)

def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task['Sequence']}. Priority: {task['Priority']}, "
                                     f"Category: {task['Category']}, Heading: {task['Heading']} - "
                                     f"Remarks: {task['Remarks']}, Due Date: {task['Due Date']}")

task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60)
task_listbox.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Export tasks to Excel with sequence numbers
def export_tasks():
    if tasks:
        df = pd.DataFrame(tasks)
        df = df[['Sequence', 'Priority', 'Category', 'Heading', 'Remarks', 'Due Date']]
        df.to_excel("tasks.xlsx", index=False)
        messagebox.showinfo("Export Successful", "Tasks exported to tasks.xlsx")
    else:
        messagebox.showerror("Export Error", "No tasks to export.")

export_button = tk.Button(root, text="Export", command=export_tasks)
export_button.grid(row=8, column=0, padx=10, pady=10)

# Task reminder function (customize this)
def remind_due_tasks():
    today = datetime.date.today()
    for task in tasks:
        due_date = task.get("Due Date")
        if due_date and due_date == today:
            messagebox.showinfo("Task Reminder", f"Task: {task['Heading']} is due today!")

# Schedule the reminder function to run periodically (customize this)
