import os
import requests

API_KEY = os.getenv('TRELLO_API_KEY')
TOKEN = os.getenv('TRELLO_TOKEN')

LIST_IDS = {
    'To Do': '697eca10f034980c326d813e',
    'In Progress': '697eca1157ea34ac00d48330',
    'Failed': '697eebeca78088d8c641941a',
    'Done': '697eca114b26b25b1f16593b'
}

def move_task(card_id, target_list_name):
    if target_list_name not in LIST_IDS:
        print(f"Error: list name '{target_list_name}' not recognized.")
        return

    target_list_id = LIST_IDS[target_list_name]
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        'key': API_KEY,
        'token': TOKEN,
        'idList': target_list_id
    }
    response = requests.put(url, params=params)
    if response.status_code == 200:
        print(f"Card {card_id} moved successfully to list '{target_list_name}'.")
    else:
        print(f"Failed to move card {card_id}: {response.text}")

# Example usage
if __name__ == "__main__":
    test_card_id = "your-card-id-here"
    move_task(test_card_id, "In Progress")
