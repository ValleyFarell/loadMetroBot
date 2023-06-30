from database.database import users_db
def data_reset(user_id: int) -> None:
    users_db[user_id]['score'] = 0
    users_db[user_id]['bot_score'] = 0
    users_db[user_id]['is_wait_game'] = False
    users_db[user_id]['is_move'] = False
    users_db[user_id]['in_game'] = False