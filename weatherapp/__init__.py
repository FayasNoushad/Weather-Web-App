import os
import requests
from dotenv import load_dotenv


load_dotenv()

# Add variables in .env file
# API Key from https://www.weatherapi.com/my/
API_KEY = os.environ.get("API_KEY")


def error(r):
    if r.get('error'):
        err = r['error']
        text ="Error ({error['code']}):- "+err['message']
        return text
    else:
        return False


def get_location_details(r):
    l_arr = []
    for i in r:
        if i=="lat":
            name = "Latitude"
        elif i=="lon":
            name = "Longitude"
        elif i=="tz_id":
            name = "Timezone ID"
        else:
            name = i.replace('_', ' ')
            if " " in name:
                words = name.split()
                name = " ".join(word.capitalize() for word in words)
        l_arr.append(f"<b>{name.capitalize()}:</b> {str(r[i])}")
    text = "<br/>".join(l_arr)
    return text


def uv(n):
    if n<2:
        return "Low"
    if n<5:
        return "Moderate"
    if n<7:
        return "High"
    if n<10:
        return "Very High"
    return "Extreme"


def get_current_details(r):
    curr_arr = []
    for i in r:
        if i=="condition":
            pass
        else:
            value = str(r[i])
            if i=="is_day":
                name = "Day/Night"
                if value=="0":
                    value="Night"
                else:
                    value = "Day"
            elif i=="uv":
                name = "Ultraviolet Index"
                value = str(r[i])+f" ({uv(r[i])})"
            else:
                name = i.replace('_', ' ')
                if " " in name:
                    words = name.split()
                    name = " ".join(word.capitalize() for word in words)
            curr_arr.append(f"<b>{name.capitalize()}:</b> {value}")
    text = "<br/>".join(curr_arr)
    return text


# Weather checking module
def weather(query):
    api = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={query}&aqi=no"
    r = requests.get(api).json()
    text = ""
    
    if error(r):
        return error(r)
    text += "<h3>Location Details</h3>"
    text += get_location_details(r['location'])
    text += "<br/><br/>"
    
    text += "<h3>Current Weather Details</h3>"
    text += get_current_details(r['current'])
    
    # text += "Name: "+r['name']
    return text
