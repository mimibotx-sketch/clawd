import os
import requests

API_KEY = os.getenv('TRELLO_API_KEY')
TOKEN = os.getenv('TRELLO_TOKEN')
BOARD_ID = "8f7EjVuI"

url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
params = {'key': API_KEY, 'token': TOKEN}
response = requests.get(url, params=params)
response.raise_for_status()
lists = response.json()

list_id_map = {lst['name']: lst['id'] for lst in lists}
print(list_id_map)
