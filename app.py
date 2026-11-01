
from flask import Flask,render_template,request
import requests
app=Flask(__name__)
API_KEY="28ea75a6263b44079f9f9c1693387023"
@app.route("/",methods=["GET","POST"])
def home():
    weather=None
    error=None
    if request.method=="POST":
        city=request.form.get("city","").strip()
        if not city:
            error="Please Enter a city name"
        elif API_KEY=="":
            error="Please Configure an API KEY"
        else:
            url="http://api.openweathermap.org/data/2.5/weather"
            params={
                "q":city,
                "appid":API_KEY,
                "units":"metric"
            }
            response=requests.get(url,params=params,timeout=10)
            data=response.json()
            if response.status_code==200:
                weather={
                    "city":data["name"],
                    "country":data["sys"]["country"],
                    "temperature":data["main"]["temp"],
                    "feels_like":data["main"]["feels_like"],
                    "humidity":data["main"]["humidity"],
                    "condition":data["weather"][0]["description"],
                    "icon":data["weather"][0]["icon"],
                    "wind":data["wind"]["speed"]
                    
                }
            elif response.status_code==404:
                error="City not found Try another City"
            elif response.status_code==401:
                error="Invalid Api Key or inactive api key"
            else:
                error=data.get("message","Unable to get weather data")
    return render_template("index.html",weather=weather,error=error)
if __name__=="__main__":
    app.run(debug=True)