import tkinter as tk
import requests
from tkinter import messagebox
from PIL import ImageTk, Image
import ttkbootstrap
from io import BytesIO
root = ttkbootstrap.Window(themename='morph')
root.title("Weather App")
root.geometry("600x500")


def get_weather(city):
    API_key = 'caa854ba9f3e141a383bca0bf29201e3'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror('Error', 'City not found')
        return None

    # Parse the json to get weather details
    weather = res.json()
    try:
        icon_id = weather['weather'][0]['icon']
        temperature = weather['main']['temp'] - 273.15
        description = weather['weather'][0]['description']
        city_name = weather['name']
        country_name = weather['sys']['country']

        # get the icon URL and return all the weather details
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}.png"
        return (icon_url, temperature, description, city_name, country_name)
    except KeyError:
        messagebox.showerror('Error', 'Failed to fetch weather details')
        return None


def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # if the city is not found, unpack the weather information
    icon_url, temperature, description, city_name, contry_name = result
    location_label.configure(text=f'{city_name},{contry_name}')
    # get the weatehr icon image from the URL and update the icon label
    image_data = requests.get(icon_url, stream=True).content
    image = Image.open(BytesIO(image_data))
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    # update the temperature and description labels
    temp_label.configure(text=f'{temperature:.2f}°C', font='comicsans,25')
    desc_label.configure(
        text=f'Description: {description}', font='comicsans,25')


# entry widget -> to enter city name
city_entry = ttkbootstrap.Entry(root, font='comicsans,18', width=30)
city_entry.pack(pady=20)

# Button widget -> to search for the weather infomation
search_btn = ttkbootstrap.Button(
    root, text='Search Weather', width=15, command=search, bootstyle='warning')
search_btn.pack(pady=20)
# label widget -> to show city name and country name
location_label = tk.Label(root, font='comicsans,25')
location_label.pack(pady=20)

# label widget -. to show weather icon
icon_label = tk.Label(root)
icon_label.pack()

# label widget -> to show temperature
temp_label = tk.Label(root, font='comicsans,25')
temp_label.pack(pady=20)

# label widget -> to show weather description
desc_label = tk.Label(root, font='comicsans,25')
desc_label.pack(pady=20)

root.mainloop()
