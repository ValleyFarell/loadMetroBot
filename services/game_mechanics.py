from lexicon.lexicon_RU import MOVES
from random import randint

def get_bot_move() -> str:
    return list(MOVES.keys())[randint(0, 2)]

def spot_winner(f_player_move: str, s_player_move: str) -> str:
    if MOVES[f_player_move] == s_player_move:
        return 'w'
    elif f_player_move == s_player_move:
        return 'd'
    else:
        return 'l'
    
