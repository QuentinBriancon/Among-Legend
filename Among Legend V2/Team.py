import random
import discord
from discord.ext import commands, tasks
import asyncio
from Player import Player


postes = ["TOP", "JGL", "MID", "ADC", "SUPP"]

        

class Team:

    roles = {
        'Imposteur': {
            'description': 'Ton objectif est de faire perdre la partie à ton équipe sans te faire démasquer.',
            'conditions': {
                "result_game": 0,
                "top_kill": -1,
                "top_mort": -1,
                "top_degats": -1,
                "worst_participation": -1
            }
        },
        'Serpentin': {
            'description' : 'Ton objectif est de gagner la partie en ayant le plus de morts et de dégâts de ton équipe.',
            'conditions': {
                "result_game": 1,
                "top_kill": -1,
                "top_mort": 1,
                "top_degats": 1,
                "worst_participation": -1
            }
        },
        'Double-face':  {
            'description': 'Tu changes de rôle aléatoirement. Tu dois soit gagner la partie, soit la perdre selon le moment de la partie (notifié en MP).',
            'conditions': {
                "result_game": -1,
                "top_kill": -1,
                "top_mort": -1,
                "top_degats": -1,
                "worst_participation": -1
            }
        },
        'Super-heros':  {
            'description': 'Ton objectif est de gagner la partie en ayant le plus de dégâts, et de kills. Tu seras gravement pénalisé en cas de défaite.',
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
            'description': 'Ton objectif est de gagner mais aussi de protéger ton amour secret. Si ton amour secret est un allié, tu ne peux pas le tuer. Si ton amour secret est un ennemi, tu ne peux pas le tuer.',
            'conditions': {
                "result_game": 1,
                "top_kill": -1,
                "top_mort": -1,
                "top_degats": -1,
                "worst_participation": -1
            }
        },
        'L\'Innovateur':  {
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
    
    #droide, ultimate bravery


    def __init__(self):
        self.TOP = None
        self.JGL = None
        self.MID = None
        self.ADC = None
        self.SUPP = None
        self.team_name = ""
        self.players_in_team = {}
        self.assigned_roles = {}

    async def create_team(self, ctx, team_name):
        players = ctx.message.mentions
        if len(players) != 2:
            await ctx.send('Une equipe est composee de exactement 5 joueurs')
            return

        self.TOP = players[0]
        self.JGL = players[1]
        '''
        self.MID = players[2]
        self.ADC = players[3]
        self.SUPP = players[4]
        '''

        for index, player in enumerate(players):
            self.players_in_team[player] = Player(self, postes[index], player, player.id)

            

        self.team_name = team_name

        await ctx.send(f"L'equipe {self.team_name} a ete creee.")
   
    def define_team(self, players):
        self.TOP, self.JGL, self.MID, self.ADC, self.SUPP = (
        players[0],
        players[1],
        players[2],
        players[3],
        players[4],
        )



    async def modify(self, ctx, index1: int, index2: int):
        if not (1 <= index1 <= 5) or not (1 <= index2 <= 5):
            await ctx.send("Les indices doivent etre entre 1 et 5.")
            return


        # Convertir les indices en indices Python (decrementer de 1)
        index1 -= 1
        index2 -= 1

        players = [self.TOP, self.JGL, self.MID, self.ADC, self.SUPP]

        players[index1], players[index2] = players[index2], players[index1]
        self.define_team(players)
        
        for index, player in enumerate(players):
            self.players_in_team[player].poste = postes[index]
        
        await self.show_team(ctx)

    async def show_team(self, ctx):
        await ctx.send(f"Equipe {self.team_name} :\n"
                       f"TOP: {self.TOP.mention}\nJGL: {self.JGL.mention}\n")
                       #f"MID: {self.MID.mention}\nADC: {self.ADC.mention}\n"
                       #f"SUPP: {self.SUPP.mention}.")

                        
    async def send_roles(self):
        players = [self.TOP, self.JGL] #, self.MID, self.ADC, self.SUPP]
        for player in players:
            role = self.assigned_roles[player]
            description = Team.roles[role]
            await player.send(f"Ton role dans Among Legends est : {role}.\nDescription : {description}")
            
    async def assign_roles(self, ctx):
        players = [self.TOP, self.JGL] #, self.MID, self.ADC, self.SUPP]

        impo = random.choice(players)        

        roles_list = list(Team.roles.keys())
        roles_list.remove('Imposteur')
        
        for player in players:
            if player == impo:
                self.assigned_roles[player] = 'Imposteur'
                description = Team.roles['Imposteur']
                self.players_in_team[player].role = 'Imposteur'
                continue
            else:
                role = random.choice(roles_list)
                self.assigned_roles[player] = role
                description = Team.roles[role]
                self.players_in_team[player].role = role
                roles_list.remove(role)
            

    async def results(self, ctx):
    # Affiche les rôles de chaque joueur
        player_mentions = "\n".join([
            f"{poste}: {player.mention} - Rôle: {self.players_in_team[player].role}"
            for poste, player in zip(postes, [self.TOP, self.JGL])#, self.MID, self.ADC, self.SUPP])
        ])
    
        await ctx.send(f"Equipe {self.team_name} :\n{player_mentions}")
    
              