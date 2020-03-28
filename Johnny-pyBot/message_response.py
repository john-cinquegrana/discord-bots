import random
import text_manip

def respond(message):
    chance = random.randint(1, 100)
    response = ""
    if chance > 95:
        response = text_manip.get_bot_response
    return response