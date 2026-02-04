import requests
from datetime import datetime, timedelta

# Your Trello API credentials - replace with your actual key/token
API_KEY = "4e73308307e3516334513ca4ab5a9cec"
TOKEN = "ATTA7def06149d6bb49c737fc2f69fc5555c7530a4864207fe7941db5629660f9d3eB8876B15"

# Trello board and endpoint info
BOARD_ID = "8f7EjVuI"
BASE_URL = "https://api.trello.com/1"

def get_cards(board_id):
    url = f"{BASE_URL}/boards/{board_id}/cards"
    query = {
        'key': API_KEY,
        'token': TOKEN
    }
    response = requests.get(url, params=query)
    response.raise_for_status()
    return response.json()

def update_card_due_date(card_id, due_date_iso):
    url = f"{BASE_URL}/cards/{card_id}"
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'due': due_date_iso
    }
    response = requests.put(url, params=query)
    response.raise_for_status()
    return response.json()

def get_lists(board_id):
    url = f"{BASE_URL}/boards/{board_id}/lists"
    query = {
        'key': API_KEY,
        'token': TOKEN
    }
    response = requests.get(url, params=query)
    response.raise_for_status()
    return response.json()

def estimate_complexity(card_name):
    length_score = len(card_name) / 20
    keywords = ['setup', 'design', 'integration', 'security', 'audit', 'fix', 'monitor', 'deploy', 'automation', 'system']
    keyword_score = sum(1 for kw in keywords if kw in card_name.lower())
    complexity = length_score + keyword_score
    return max(1, complexity)

def estimate_due_dates_by_list(cards, lists):
    list_name_to_id = {lst['name']: lst['id'] for lst in lists}

    in_progress_cards = [c for c in cards if c['idList'] == list_name_to_id.get('In Progress')]
    to_do_cards = [c for c in cards if c['idList'] == list_name_to_id.get('To Do')]

    in_progress_due_dates = {}
    for card in in_progress_cards:
        if card.get('due'):
            in_progress_due_dates[card['id']] = datetime.fromisoformat(card['due'].replace('Z','+00:00'))
        else:
            in_progress_due_dates[card['id']] = datetime.now() + timedelta(days=1)

    if in_progress_due_dates:
        base_date = max(in_progress_due_dates.values()) + timedelta(days=1)
    else:
        base_date = datetime.now() + timedelta(days=1)

    due_dates = {}
    max_tasks_per_day = 5

    for card_id, due in in_progress_due_dates.items():
        due_dates[card_id] = due.isoformat()

    to_do_cards.sort(key=lambda c: estimate_complexity(c['name']), reverse=True)

    day_cursor = 0
    tasks_in_current_day = 0

    for card in to_do_cards:
        complexity = estimate_complexity(card['name'])
        if tasks_in_current_day >= max_tasks_per_day:
            day_cursor += 1
            tasks_in_current_day = 0

        duration_days = max(1, int(round(complexity)))
        due_date = base_date + timedelta(days=day_cursor + duration_days - 1)
        due_dates[card['id']] = due_date.isoformat()

        tasks_in_current_day += 1

    return due_dates

def main():
    print("Fetching cards from board...")
    cards = get_cards(BOARD_ID)
    print(f"Found {len(cards)} cards")

    print("Fetching lists from board...")
    lists = get_lists(BOARD_ID)

    due_dates = estimate_due_dates_by_list(cards, lists)

    for card in cards:
        card_id = card['id']
        if card_id in due_dates:
            new_due_date = due_dates[card_id]
            print(f"Updating card '{card['name']}' due date to {new_due_date}")
            update_card_due_date(card_id, new_due_date)
        else:
            print(f"Skipping card '{card['name']}' (likely in 'Done' or unhandled list)")

    print("All applicable cards updated.")

if __name__ == "__main__":
    main()
