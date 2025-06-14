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
root.geometry("400x600")
root.resizable(False, False)

# --- Load default background image ---
try:
    default_bg = Image.open("default.jpg").resize((400, 600))
except:
    default_bg = Image.new("RGB", (400, 600), color="#87ceeb")  # fallback
bg_photo = ImageTk.PhotoImage(default_bg)

# --- Background label ---
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Fonts ---
font_main = ("Segoe UI", 12)
font_title = ("Segoe UI", 14, "bold")
font_small = ("Segoe UI", 10)

# --- Overlay Frame for UI Content ---
overlay = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", highlightbackground="black", highlightthickness=1)
overlay.place(relx=0.05, rely=0.03, relwidth=0.9, relheight=0.9)

# --- Input Section ---
input_frame = tk.Frame(overlay, bg="#f5f5f5")
input_frame.pack(pady=10, fill="x", padx=10)

tk.Label(input_frame, text="Enter City:", font=font_main, bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=5, pady=5)
city_entry = tk.Entry(input_frame, font=font_main, width=25)
city_entry.grid(row=0, column=1, padx=5, pady=5)

# --- Units Selection ---
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(input_frame, bg="#f5f5f5")
unit_frame.grid(row=1, columnspan=2, pady=5)
tk.Label(unit_frame, text="Units:", font=font_small, bg="#f5f5f5").pack(side="left", padx=5)
tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="metric", bg="#f5f5f5").pack(side="left")
tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="imperial", bg="#f5f5f5").pack(side="left")

# --- Buttons ---
button_frame = tk.Frame(overlay, bg="#f5f5f5")
button_frame.pack(pady=5)

tk.Button(button_frame, text="📍 Use My Location", command=lambda: detect_location(),
          font=font_small, bg="#e0f7fa", fg="black").pack(side="left", padx=10)
tk.Button(button_frame, text="Get Weather", command=lambda: show_weather(),
          font=font_main, bg="#0288d1", fg="white").pack(side="left", padx=10)

# --- Forecast Mode Toggle ---
forecast_mode = tk.StringVar(value="hourly")
forecast_mode_frame = tk.Frame(overlay, bg="#f5f5f5")
forecast_mode_frame.pack(pady=5)
tk.Label(forecast_mode_frame, text="Forecast Type:", font=font_small, bg="#f5f5f5").pack(side="left")
tk.Radiobutton(forecast_mode_frame, text="Hourly", variable=forecast_mode, value="hourly", bg="#f5f5f5").pack(side="left", padx=5)
tk.Radiobutton(forecast_mode_frame, text="Daily", variable=forecast_mode, value="daily", bg="#f5f5f5").pack(side="left", padx=5)

# --- Weather Icon & Output ---
icon_label = tk.Label(overlay, bg="#ffffff")
icon_label.pack()

result_label = tk.Label(overlay, text="", font=font_main, justify="left", bg="#ffffff")
result_label.pack(pady=5)

# --- Forecast Section ---
forecast_frame = tk.Frame(overlay, bg="#ffffff", bd=1, relief="solid")
forecast_frame.pack(pady=10, fill="both", expand=True, padx=10)

# --- Weather Functions ---
def get_weather(city, units='metric'):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': API_KEY, 'units': units}
    try:
        response = requests.get(BASE_URL, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_forecast(city, units='metric'):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {'q': city, 'appid': API_KEY, 'units': units}
    try:
        response = requests.get(url, params=params)
        return response.json()["list"] if response.status_code == 200 else []
    except Exception as e:
        print(f"Forecast Error: {e}")
        return []

def update_background(condition):
    condition_lower = condition.lower()
    if "clear" in condition_lower:
        bg_file = "clear.jpg"
    elif "cloud" in condition_lower:
        bg_file = "clouds.jpg"
    elif "rain" in condition_lower:
        bg_file = "rain.jpg"
    elif "snow" in condition_lower:
        bg_file = "snow.jpg"
    else:
        bg_file = "default.jpg"
    try:
        new_bg = Image.open(bg_file).resize((400, 600))
        new_bg_photo = ImageTk.PhotoImage(new_bg)
        bg_label.config(image=new_bg_photo)
        bg_label.image = new_bg_photo
    except Exception as e:
        print(f"Background load error: {e}")

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

        # Set background image based on condition
        update_background(condition)

        # Weather Icon
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

        # Forecast Display
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        forecast_data = get_forecast(city, unit)
        mode = forecast_mode.get()

        if forecast_data:
            tk.Label(forecast_frame, text=f"{mode.capitalize()} Forecast", font=font_title, bg="#ffffff").pack(pady=5)

            if mode == "hourly":
                for i in range(0, 16, 2):
                    entry = forecast_data[i]
                    dt = entry["dt_txt"]
                    temp = entry["main"]["temp"]
                    desc = entry["weather"][0]["description"].capitalize()
                    forecast_str = f"[{dt[8:10]} {dt[11:16]}] {desc} — {temp}°"
                    tk.Label(forecast_frame, text=forecast_str, font=font_small, bg="#ffffff").pack(anchor="w", padx=10)
            else:
                daily_done = set()
                for entry in forecast_data:
                    dt = entry["dt_txt"]
                    day = dt[:10]
                    time_of_day = dt[11:16]
                    if day not in daily_done and time_of_day == "12:00":
                        temp = entry["main"]["temp"]
                        desc = entry["weather"][0]["description"].capitalize()
                        forecast_str = f"[{day}] {desc} — {temp}°"
                        tk.Label(forecast_frame, text=forecast_str, font=font_small, bg="#ffffff").pack(anchor="w", padx=10)
                        daily_done.add(day)
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

# --- Run App ---
root.mainloop()
