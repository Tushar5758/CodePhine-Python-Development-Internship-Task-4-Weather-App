import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("600x400")
        self.root.config(bg="#1C9CF6")

        self.frame = ttk.Frame(root, padding=(20, 20, 20, 20), style='TFrame')
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
         
        title_label = ttk.Label(self.frame, text="Weather Application", font=("Times New Roman", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")

        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(self.frame, textvariable=self.location_var, font=("Times New Roman", 16), style="TEntry")
        self.location_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.search_button = ttk.Button(self.frame, text="Search", command=self.get_weather, style="TButton")
        self.search_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.weather_label = ttk.Label(self.frame, text="", font=("Times New Roman", 18), wraplength=400, justify="left")
        self.weather_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.icon_label = ttk.Label(self.frame, text="")
        self.icon_label.grid(row=3, column=0, columnspan=2)

        style = ttk.Style()
        style.configure('TFrame', background='#E3F4FE')
        style.configure('TButton', font=("Times New Roman", 16), background='#1C9CF6')
        style.configure('TEntry', font=("Times New Roman", 16), padding=10)

    def get_weather(self):
        api_key = "b80d85cd18c190579de73a0e9ddc7dd3"
        location = self.location_var.get()
        if not location:
            return

        endpoint = "http://api.weatherstack.com/current"
        params = {"access_key": api_key, "query": location, "units": "m"}
        response = requests.get(endpoint, params=params)
        data = response.json()

        if response.status_code == 200:
            current_weather = data['current']
            current_conditions = f"Current Conditions in {location}:\n"
            current_conditions += f"Temperature: {current_weather['temperature']}°C\n"
            current_conditions += f"Humidity: {current_weather['humidity']}%\n"
            current_conditions += f"Wind Speed: {current_weather['wind_speed']} m/s"
            self.weather_label.config(text=current_conditions)

            icon_url = current_weather['weather_icons'][0]
            self.update_icon(icon_url)

        else:
            self.weather_label.config(text=f"Error: {data['error']['info']}")

    def update_icon(self, icon_url):
        response = requests.get(icon_url, stream=True)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

        self.icon_label.config(image=photo)
        self.icon_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
