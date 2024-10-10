import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

# Function to validate user input for password length and character types
def validate_input(length, char_types):
    if length < 8:
        messagebox.showwarning("Input Error", "Password length must be at least 8 characters.")
        return False
    if not any(char_types):
        messagebox.showwarning("Input Error", "Please select at least one character type.")
        return False
    return True

# Function to generate a random secure password
def generate_password():
    length = int(length_var.get())
    include_upper = upper_var.get()
    include_lower = lower_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()
    avoid_ambiguous = similar_var.get()
    
    char_types = [include_upper, include_lower, include_digits, include_special]
    
    # Validate user input
    if not validate_input(length, char_types):
        return

    # Define character sets
    characters = ''
    if include_upper:
        characters += string.ascii_uppercase
    if include_lower:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    if avoid_ambiguous:
        for char in 'l1I0O':
            characters = characters.replace(char, '')

    # Ensure password contains at least one of each selected character type
    password = []
    if include_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if include_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if include_digits:
        password.append(secrets.choice(string.digits))
    if include_special:
        password.append(secrets.choice(string.punctuation))

    # Fill the rest of the password
    while len(password) < length:
        password.append(secrets.choice(characters))

    # Shuffle to randomize password structure
    secrets.SystemRandom().shuffle(password)
    
    generated_password = ''.join(password)
    
    # Display the generated password
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated_password)
    
    # Automatically copy to clipboard
    pyperclip.copy(generated_password)
    messagebox.showinfo("Success", "Password generated and copied to clipboard!")

# Function to reset fields
def reset_fields():
    length_var.set(12)
    upper_var.set(True)
    lower_var.set(True)
    digits_var.set(True)
    special_var.set(False)
    similar_var.set(False)
    password_entry.delete(0, tk.END)

# Function to show/hide the password
def toggle_password_visibility():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        toggle_button.config(text='Show Password')
    else:
        password_entry.config(show='')
        toggle_button.config(text='Hide Password')

# GUI Setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("450x400")
root.config(bg="#2c3e50")  # Dark background for contrast

# Styling variables
button_bg = "#3498db"
button_fg = "#ffffff"
button_hover_bg = "#2980b9"
entry_bg = "#ecf0f1"
label_font = ("Helvetica", 12, "bold")
button_font = ("Helvetica", 10, "bold")

# Hover effect for buttons
def on_enter(e):
    e.widget['background'] = button_hover_bg

def on_leave(e):
    e.widget['background'] = button_bg

# Variables
length_var = tk.IntVar(value=12)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=False)
similar_var = tk.BooleanVar(value=False)

# Widgets with styling
tk.Label(root, text="Password Length:", bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(pady=5)
length_spinbox = tk.Spinbox(root, from_=8, to=128, textvariable=length_var, width=5, font=("Arial", 12))
length_spinbox.pack(pady=5)

tk.Checkbutton(root, text="Include Uppercase Letters", variable=upper_var, bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Lowercase Letters", variable=lower_var, bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Digits", variable=digits_var, bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Special Characters", variable=special_var, bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Avoid Ambiguous Characters (e.g., l, 1, O, 0)", variable=similar_var, bg="#2c3e50", fg="#ecf0f1", font=label_font).pack(anchor='w', padx=20)

# Password display entry
password_entry = tk.Entry(root, width=30, font=("Arial", 14), show='*', bg=entry_bg)
password_entry.pack(pady=10)

# Toggle password visibility button with styling
toggle_button = tk.Button(root, text="Show Password", command=toggle_password_visibility, bg=button_bg, fg=button_fg, font=button_font)
toggle_button.pack(pady=5)
toggle_button.bind("<Enter>", on_enter)
toggle_button.bind("<Leave>", on_leave)

# Generate button with hover effect and styling
generate_button = tk.Button(root, text="Generate Password", command=generate_password, bg=button_bg, fg=button_fg, font=button_font)
generate_button.pack(pady=5)
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

# Reset button with hover effect and styling
reset_button = tk.Button(root, text="Reset", command=reset_fields, bg=button_bg, fg=button_fg, font=button_font)
reset_button.pack(pady=5)
reset_button.bind("<Enter>", on_enter)
reset_button.bind("<Leave>", on_leave)

# Start GUI loop
root.mainloop()

