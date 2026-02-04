import os
import json
import requests

API_KEY = "4e73308307e3516334513ca4ab5a9cec"
TOKEN = "ATTA7def06149d6bb49c737fc2f69fc5555c7530a4864207fe7941db5629660f9d3eB8876B15"
BOARD_ID = "8f7EjVuI"

# Get all lists on the board
lists_url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
lists_params = {'key': API_KEY, 'token': TOKEN}
lists_resp = requests.get(lists_url, params=lists_params)
lists_resp.raise_for_status()
lists = lists_resp.json()

board_tasks = {}

for lst in lists:
    list_id = lst['id']
    list_name = lst['name']
    # Get cards in this list
    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards_params = {'key': API_KEY, 'token': TOKEN}
    cards_resp = requests.get(cards_url, params=cards_params)
    cards_resp.raise_for_status()
    cards = cards_resp.json()
    board_tasks[list_name] = [{'id': card['id'], 'name': card['name']} for card in cards]

# Save to file
with open('trello_board_tasks_backup.json', 'w') as f:
    json.dump(board_tasks, f, indent=2)

print("Saved current Trello board tasks to trello_board_tasks_backup.json")
