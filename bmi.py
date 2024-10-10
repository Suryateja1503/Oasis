import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import pandas as pd
import os

# File to store user data
DATA_FILE = 'bmi_data.csv'

# Initialize DataFrame if file doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Name', 'Weight', 'Height', 'BMI', 'Category'])
    df.to_csv(DATA_FILE, index=False)

def calculate_bmi(weight, height):
    """Calculate BMI using weight and height."""
    return weight / (height ** 2)

def classify_bmi(bmi):
    """Classify BMI into categories."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(name, weight, height, bmi, category):
    """Save user data to CSV file."""
    df = pd.read_csv(DATA_FILE)
    df = df.append({'Name': name, 'Weight': weight, 'Height': height, 'BMI': bmi, 'Category': category}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def view_history():
    """View historical data and plot BMI trend."""
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        messagebox.showinfo("No Data", "No historical data available.")
        return

    # Plotting BMI trend
    plt.figure(figsize=(10, 5))
    plt.plot(df['Name'], df['BMI'], marker='o', linestyle='-')
    plt.title('BMI Trend')
    plt.xlabel('User')
    plt.ylabel('BMI')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

def view_data():
    """View historical data in a table format."""
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        messagebox.showinfo("No Data", "No historical data available.")
        return

    # Show the data in a new window with a table
    data_window = tk.Toplevel()
    data_window.title("User Data")
    
    tree = ttk.Treeview(data_window, columns=("Name", "Weight", "Height", "BMI", "Category"), show='headings')
    tree.heading("Name", text="Name")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (m)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")
    
    for i, row in df.iterrows():
        tree.insert("", "end", values=(row["Name"], row["Weight"], row["Height"], row["BMI"], row["Category"]))

    tree.pack(fill="both", expand=True)

def calculate():
    """Handle the BMI calculation and data storage."""
    name = name_entry.get()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        save_data(name, weight, height, bmi, category)
        
        result_label.config(text=f"Your BMI is: {bmi:.2f}\nYou are classified as: {category}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for weight and height.")

def clear_fields():
    """Clear all input fields."""
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")

# Setting up the GUI
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x400")
root.configure(bg="#f2f2f2")

# Title Label
title_label = tk.Label(root, text="BMI Calculator", font=("Arial", 18, "bold"), bg="#f2f2f2", fg="#333")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Input Fields
tk.Label(root, text="Name:", font=("Arial", 12), bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg):", font=("Arial", 12), bg="#f2f2f2").grid(row=2, column=0, padx=10, pady=10, sticky="e")
weight_entry = tk.Entry(root)
weight_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m):", font=("Arial", 12), bg="#f2f2f2").grid(row=3, column=0, padx=10, pady=10, sticky="e")
height_entry = tk.Entry(root)
height_entry.grid(row=3, column=1, padx=10, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f2f2f2", fg="#333")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.grid(row=4, column=0, columnspan=2)

calculate_button = tk.Button(button_frame, text="Calculate BMI", command=calculate, width=15, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
calculate_button.grid(row=0, column=0, padx=5, pady=10)

clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_fields, width=15, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
clear_button.grid(row=0, column=1, padx=5, pady=10)

view_data_button = tk.Button(root, text="View User Data", command=view_data, width=15, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
view_data_button.grid(row=6, column=0, padx=10, pady=10)

history_button = tk.Button(root, text="View History", command=view_history, width=15, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
history_button.grid(row=6, column=1, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
