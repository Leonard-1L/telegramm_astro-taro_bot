
def return_bot_token() -> str:
    with open("secrets/BOT TOKEN", 'r') as token:
        return token