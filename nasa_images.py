import requests

API_KEY = "J3gNT5GSEJBFVCanDTzj9aDUMdBuMDd94SGNPXcz"
URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2015-6-3&api_key=DEMO_KEY"
r = requests.get(URL)
data = r.json()

print(data)
