import requests

API_KEY = "4e73308307e3516334513ca4ab5a9cec"
TOKEN = "ATTA7def06149d6bb49c737fc2f69fc5555c7530a4864207fe7941db5629660f9d3eB8876B15"
LIST_ID = "697eca10f034980c326d813e"

url = "https://api.trello.com/1/cards"
query = {
    'key': API_KEY,
    'token': TOKEN,
    'idList': LIST_ID,
    'name': "Set up Power BI dashboard for key financial metrics including crypto, Canadian interest rates, and commodity prices"
}

response = requests.post(url, params=query)
if response.status_code == 200:
    print("Task added successfully!")
else:
    print("Failed to add task:", response.text)
