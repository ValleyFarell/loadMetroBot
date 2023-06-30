from database.database import users_db, user_template
from copy import deepcopy
def data_read(path: str | None) -> None:
    users_base_file = open('database/base.txt', 'r+')
    users_base = users_base_file.read().split(',')
    for user_id in users_base:
        users_db[int(user_id)] = deepcopy(user_template)
        users_db[int(user_id)]['score'] = 0
        users_db[int(user_id)]['bot_score'] = 0
        users_db[int(user_id)]['is_wait_game'] = False
        users_db[int(user_id)]['is_move'] = False
        users_db[int(user_id)]['in_game'] = False