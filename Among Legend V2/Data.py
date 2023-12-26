# Data.py
# -*- coding: latin-1 -*-


# Liste if all the roles, their description and conditions to win
roles = {
    'Imposteur': {
        'description': 'Ton objectif est de faire perdre la partie � ton �quipe sans te faire d�masquer.',
        'conditions': {
            "result_game": 0,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": -1
        }
    },
    'Serpentin': {
        'description' : 'Ton objectif est de gagner la partie en ayant le plus de morts et de d�g�ts de ton �quipe.',
        'conditions': {
            "result_game": 1,
            "top_kill": -1,
            "top_mort": 1,
            "top_degats": 1,
            "worst_participation": -1
        }
    },
    'Double-face':  {
        'description': 'Tu changes de r�le al�atoirement. Tu dois soit gagner la partie, soit la perdre selon le moment de la partie (notifi� en MP).',
        'conditions': {
            "result_game": -1,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": -1
        }
    },
    'Super-heros':  {
        'description': 'Ton objectif est de gagner la partie en ayant le plus de d�g�ts, et de kills. Tu seras gravement p�nalis� en cas de d�faite.',
        'conditions': {
            "result_game": 1,
            "top_kill": 1,
            "top_mort": -1,
            "top_degats": 1,
            "worst_participation": -1
        }
    },
    'Agent double':  {
        'description': 'Ton objectif est de gagner tout en te faisant voter comme imposteur.',
        'conditions': {
            "result_game": 1,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": -1
        }
    },
    'Exile':  {
        'description': 'Ton objectif est de gagner tout en ayant le moins et de participations.',
        'conditions': {
            "result_game": 1,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": 1
        }
    },
    'Romeo':  {
        'description': 'Ton objectif est de gagner mais aussi de prot�ger ton amour secret. Si ton amour secret est un alli�, tu ne peux pas prendre de kill o� il a l\'assist (ks). Si ton amour secret est un ennemi, tu ne peux pas le tuer.',
        'conditions': {
            "result_game": 1,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": -1
        }
    },
    'Innovateur':  {
        'description': 'Ton objectif est de gagner la partie avec un pick exotique',
        'conditions': {
            "result_game": 1,
            "top_kill": -1,
            "top_mort": -1,
            "top_degats": -1,
            "worst_participation": -1
        }
    },
}
#droide, ultimate bravery, kda_player