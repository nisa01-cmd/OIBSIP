import tkinter as tk
from tkinter import messagebox
import requests
from PIL import ImageTk, Image
import io
import time

# --- API Key ---
API_KEY = "a02f9436567cc8facb143ead344f78c3"

# --- Initialize Main Window ---
root = tk.Tk()
root.title("Weather App")
root.geometry("400x550")
root.configure(bg="#e8f0f2")
root.resizable(False, False)

# --- Fonts ---
font_main = ("Segoe UI", 12)
font_title = ("Segoe UI", 14, "bold")
font_small = ("Segoe UI", 10)

# --- Icon Display ---
icon_label = tk.Label(root, bg="#e8f0f2")
icon_label.pack()

# --- Forecast Frame (Global) ---
forecast_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
forecast_frame.pack(pady=10, fill="both", padx=10)

# --- Functions ---

def get_weather(city, units='metric'):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_forecast(city, units='metric'):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            return data["list"]  # List of forecast entries
        else:
            return []
    except Exception as e:
        print(f"Forecast Error: {e}")
        return []

def show_weather():
    city = city_entry.get()
    unit = unit_var.get()
    data = get_weather(city, unit)

    if data:
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        condition = data['weather'][0]['description']
        wind = data['wind']['speed']
        visibility = data.get('visibility', 0) // 1000
        sunrise = time.strftime('%H:%M:%S', time.localtime(data['sys']['sunrise']))
        sunset = time.strftime('%H:%M:%S', time.localtime(data['sys']['sunset']))
        icon_code = data['weather'][0]['icon']

        unit_symbol = "°C" if unit == 'metric' else "°F"

        result = (
            f"City: {data['name']}\n"
            f"Condition: {condition.capitalize()}\n"
            f"Temperature: {temp}{unit_symbol}\n"
            f"Feels Like: {feels_like}{unit_symbol}\n"
            f"Humidity: {humidity}%\n"
            f"Pressure: {pressure} hPa\n"
            f"Visibility: {visibility} km\n"
            f"Wind Speed: {wind} m/s\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )

        result_label.config(text=result)

        # Load icon from OpenWeatherMap
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            image_data = icon_response.content
            image = Image.open(io.BytesIO(image_data))
            icon = ImageTk.PhotoImage(image)
            icon_label.config(image=icon)
            icon_label.image = icon
        except Exception as e:
            print(f"Icon error: {e}")

        # Clear old forecast
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        forecast_data = get_forecast(city, unit)
        if forecast_data:
            tk.Label(forecast_frame, text="3-Hourly Forecast", font=font_title, bg="#ffffff").pack(pady=5)

            for i in range(0, 16, 2):  # Show approx. 24 hours
                entry = forecast_data[i]
                dt = entry["dt_txt"]
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"].capitalize()
                forecast_str = f"[{dt[8:10]} {dt[11:16]}] {desc} — {temp}°"
                tk.Label(forecast_frame, text=forecast_str, font=font_small, bg="#ffffff").pack(anchor="w", padx=10)
    else:
        messagebox.showerror("Error", "Could not retrieve weather data.\nPlease check the city name.")

def detect_location():
    try:
        response = requests.get("http://ip-api.com/json")
        data = response.json()
        if response.status_code == 200:
            city = data.get("city", "")
            if city:
                city_entry.delete(0, tk.END)
                city_entry.insert(0, city)
                show_weather()
            else:
                messagebox.showerror("Location Error", "City not found from IP.")
        else:
            messagebox.showerror("Location Error", "Could not detect location.")
    except Exception as e:
        print(f"Location error: {e}")
        messagebox.showerror("Network Error", "Failed to fetch location. Check your internet.")

# --- Input UI ---

tk.Label(root, text="Enter City:", font=font_main, bg="#e8f0f2").pack(pady=(15, 5))
city_entry = tk.Entry(root, font=font_main, width=30)
city_entry.pack(pady=(0, 5))

# Unit selection
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(root, bg="#e8f0f2")
tk.Label(unit_frame, text="Units:", font=("Arial", 10), bg="#e8f0f2").pack(side="left")
tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="metric", bg="#e8f0f2").pack(side="left")
tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="imperial", bg="#e8f0f2").pack(side="left")
unit_frame.pack(pady=5)

# Buttons
tk.Button(root, text="📍 Use My Location", command=detect_location,
          font=font_small, bg="#d9edf7", fg="black").pack(pady=2)

tk.Button(root, text="Get Weather", command=show_weather,
          font=font_main, bg="#00bfff", fg="white").pack(pady=(5, 10))

# Weather Result Label
result_label = tk.Label(root, text="", font=font_main, justify="left", bg="#e8f0f2")
result_label.pack(pady=(10, 5))

root.mainloop()
