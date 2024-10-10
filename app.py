import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import geocoder

API_KEY = "your_openweathermap_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


# API Integration: Fetch Weather Data
def get_weather_data(city_name, unit="metric"):
    """Fetch weather data from OpenWeatherMap API with error handling."""
    try:
        complete_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={unit}"
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return None


# User Input Handling: Validate City Input
def validate_input(city_name):
    """Validate user input and check for empty or invalid data."""
    if not city_name:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return False
    return True


# Error Handling: Display Errors or Warnings
def display_error(error_message):
    """Display an error message in the app."""
    messagebox.showerror("Error", error_message)


# Data Visualization: Display Weather Information
def display_weather(data, unit):
    """Display weather information in a user-friendly way, including icons."""
    for widget in weather_frame.winfo_children():
        widget.destroy()

    weather_desc = data['weather'][0]['description']
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']

    # Display text weather information
    weather_label = ttk.Label(weather_frame, text=f"Weather: {weather_desc.capitalize()}")
    weather_label.pack()

    temp_label = ttk.Label(weather_frame, text=f"Temperature: {temp} {'°C' if unit == 'metric' else '°F'}")
    temp_label.pack()

    wind_label = ttk.Label(weather_frame, text=f"Wind Speed: {wind_speed} m/s")
    wind_label.pack()

    # Display weather icon based on weather description
    icon_path = get_weather_icon(data['weather'][0]['icon'])
    image = Image.open(icon_path)
    icon = ImageTk.PhotoImage(image)

    icon_label = ttk.Label(weather_frame, image=icon)
    icon_label.image = icon  # To prevent garbage collection of the image
    icon_label.pack()


# Fetch Weather Icon
def get_weather_icon(icon_code):
    """Get the icon based on the weather condition code."""
    return f"icons/{icon_code}.png"  # Ensure icons are saved in an 'icons' folder


# Fetch City Suggestions (for area suggestions)
def get_city_suggestions(query):
    """Fetch city suggestions from Google Places API."""
    places_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&types=(cities)&key=your_google_places_api_key"
    response = requests.get(places_url)
    suggestions = response.json()
    return [place['description'] for place in suggestions.get('predictions', [])]


def on_city_entry(event):
    """Update suggestions while typing the city name."""
    city = city_entry.get()
    if city:
        suggestions = get_city_suggestions(city)
        city_dropdown['values'] = suggestions


# GPS Integration: Get Current Location
def get_current_location():
    """Fetch the user's current location using IP or GPS."""
    location = geocoder.ip('me')  # For desktop apps, this uses IP geolocation
    if location:
        return location.city
    else:
        display_error("Could not detect location!")
        return None


# Unit Conversion: Fetch and Display Weather with Selected Unit
def get_weather(city_name, unit):
    """Retrieve weather data based on user input and display it in the GUI."""
    if validate_input(city_name):
        data = get_weather_data(city_name, unit)
        if data and data.get('cod') == 200:
            display_weather(data, unit)
        else:
            display_error("City not found!")


# Main GUI Function
def create_gui():
    """Create the main user interface for the weather app."""
    global root, city_entry, weather_frame, city_dropdown

    root = tk.Tk()
    root.title("Advanced Weather App")
    root.geometry("400x500")

    # Label for city input
    city_label = ttk.Label(root, text="Enter City:")
    city_label.pack(pady=10)

    # Entry widget for city input
    city_entry = ttk.Entry(root)
    city_entry.pack(pady=5)

    # Bind event for city suggestions
    city_entry.bind('<KeyRelease>', on_city_entry)

    # Dropdown for city suggestions
    city_dropdown = ttk.Combobox(root)
    city_dropdown.pack(pady=5)

    # Dropdown for unit selection (Celsius/Fahrenheit)
    unit_label = ttk.Label(root, text="Select Unit:")
    unit_label.pack(pady=5)

    unit_var = tk.StringVar(value="metric")  # Default to Celsius
    unit_dropdown = ttk.Combobox(root, textvariable=unit_var, values=["metric", "imperial"])
    unit_dropdown.pack(pady=5)

    # Button to fetch weather data
    weather_button = ttk.Button(root, text="Get Weather", command=lambda: get_weather(city_entry.get(), unit_var.get()))
    weather_button.pack(pady=10)

    # Button to use GPS location
    location_button = ttk.Button(root, text="Use My Location", command=lambda: get_weather(get_current_location(), unit_var.get()))
    location_button.pack(pady=5)

    # Frame to display the weather results
    weather_frame = ttk.Frame(root)
    weather_frame.pack(pady=10)

    root.mainloop()


# Run the GUI
if __name__ == "__main__":
    create_gui()
