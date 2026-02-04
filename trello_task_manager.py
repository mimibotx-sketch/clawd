import os
import json
import requests

API_KEY = os.getenv('TRELLO_API_KEY')
TOKEN = os.getenv('TRELLO_TOKEN')

LIST_IDS = {
    'To Do': '697eca10f034980c326d813e',
    'In Progress': '697eca1157ea34ac00d48330',
    'Failed': '697eebeca78088d8c641941a',
    'Done': '697eca114b26b25b1f16593b'
}

STORAGE_FILE = 'trello_tasks.json'

# Load or initialize task storage mapping task names to card IDs
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, 'r') as f:
        task_cards = json.load(f)
else:
    task_cards = {}

def save_storage():
    with open(STORAGE_FILE, 'w') as f:
        json.dump(task_cards, f)

def create_card(task_name, list_name):
    url = 'https://api.trello.com/1/cards'
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'idList': LIST_IDS[list_name],
        'name': task_name
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        card = response.json()
        card_id = card['id']
        task_cards[task_name] = card_id
        save_storage()
        print(f"Task '{task_name}' added to list '{list_name}' with card ID {card_id}.")
        return True
    else:
        print(f"Failed to add task '{task_name}': {response.text}")
        return False

def move_card(task_name, list_name):
    if task_name not in task_cards:
        print(f"Task '{task_name}' not found in storage.")
        return False
    card_id = task_cards[task_name]
    url = f'https://api.trello.com/1/cards/{card_id}'
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'idList': LIST_IDS[list_name]
    }
    response = requests.put(url, params=query)
    if response.status_code == 200:
        print(f"Task '{task_name}' moved to list '{list_name}'.")
        return True
    else:
        print(f"Failed to move task '{task_name}': {response.text}")
        return False

def add_task_to_do(task_name):
    if task_name in task_cards:
        print(f"Task '{task_name}' already exists.")
        return False
    return create_card(task_name, 'To Do')

def start_task(task_name):
    if task_name in task_cards:
        return move_card(task_name, 'In Progress')
    else:
        return create_card(task_name, 'In Progress')

def complete_task(task_name):
    return move_card(task_name, 'Done')

def fail_task(task_name):
    return move_card(task_name, 'Failed')

def resume_task(task_name):
    # Move failed task back to In Progress
    return move_card(task_name, 'In Progress')

if __name__ == '__main__':
    # Example usage
    add_task_to_do('Example Task 1')
    start_task('Example Task 1')
    fail_task('Example Task 1')
    resume_task('Example Task 1')
    complete_task('Example Task 1')
