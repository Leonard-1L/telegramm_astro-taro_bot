def get_bot_token():
    with open('secrets/bot_token', 'r') as f:
        return f.read().strip()
