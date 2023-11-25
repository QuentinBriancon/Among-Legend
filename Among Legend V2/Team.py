import random
import discord
from discord.ext import commands, tasks
import asyncio



postes = ["TOP", "JNG", "MID", "ADC", "SUPP"]

        

class Team:

    roles = {
        'Imposteur': 'Ton objectif est de faire perdre la partie à ton équipe sans te faire démasquer.',
        'Serpentin': 'Ton objectif est de gagner la partie en ayant le plus de morts et de dégâts de ton équipe.',
        'Double-face': 'Tu changes de rôle aléatoirement. Tu dois soit gagner la partie, soit la perdre selon le moment de la partie (notifié en MP).',
        'Super-heros': 'Ton objectif est de gagner la partie en ayant le plus de dégâts, d\'assistances et de kills. Tu seras gravement pénalisé en cas de défaite.',
        'Agent double': 'Ton objectif est de gagner tout en te faisant voter comme imposteur.',
        'Exile': 'Ton objectif est de gagner tout en ayant le moins de kills et de participations possibles.',
        'Romeo': 'Ton objectif est de gagner mais aussi de protéger ton amour secret. Si ton amour secret est un allié, tu ne peux pas le tuer. Si ton amour secret est un ennemi, tu ne peux pas le tuer.',
        'L\'Innovateur': 'Ton objectif est de gagner la partie avec un pick exotique'
    }
    
    #droide, ultimate bravery


    def __init__(self):
        self.TOP = None
        self.JNG = None
        self.MID = None
        self.ADC = None
        self.SUPP = None
        self.team_name = None
        self.players_in_team = {}
        self.assigned_roles = {}

    async def create_team(self, ctx, team_name):
        players = ctx.message.mentions
        if len(players) != 2:
            await ctx.send('Une equipe est composee de exactement 5 joueurs')
            return

        self.TOP = players[0]
        self.JNG = players[1]
        '''
        self.MID = players[2]
        self.ADC = players[3]
        self.SUPP = players[4]
        '''

        for index, player in enumerate(players):
            self.players_in_team[player] = Player()
            self.players_in_team[player].team = self
            self.players_in_team[player].poste = postes[index]
            

        self.team_name = team_name

        await ctx.send(f"L'equipe {self.team_name} a ete creee.")
   
    def define_team(self, players):
        self.TOP, self.JNG, self.MID, self.ADC, self.SUPP = (
        players[0],
        players[1],
        players[2],
        players[3],
        players[4],
        )



    async def modify(self, ctx, index1, index2):
        if not (1 <= index1 <= 5) or not (1 <= index2 <= 5):
            await ctx.send("Les indices doivent etre entre 1 et 5.")
            return


        # Convertir les indices en indices Python (decrementer de 1)
        index1 -= 1
        index2 -= 1

        players = [self.TOP, self.JNG, self.MID, self.ADC, self.SUPP]

        players[index1], players[index2] = players[index2], players[index1]
        self.define_team(self, players)
        
        for index, player in enumerate(players):
            self.players_in_team[player].poste = postes[index]
        
        await self.show_team(ctx)

    async def show_team(self, ctx):
        await ctx.send(f"Equipe {self.team_name} :\n"
                       f"TOP: {self.TOP.mention}\nJNG: {self.JNG.mention}\n")
                       #f"MID: {self.MID.mention}\nADC: {self.ADC.mention}\n"
                       #f"SUPP: {self.SUPP.mention}.")

                        
    async def send_roles(self):
        players = [self.TOP, self.JNG] #, self.MID, self.ADC, self.SUPP]
        for player in players:
            role = self.assigned_roles[player]
            description = roles[role]
            await player.send(f"Ton role dans Among Legends est : {role}.\nDescription : {description}")
            
    async def assign_roles(self, ctx):
        players = [self.TOP, self.JNG] #, self.MID, self.ADC, self.SUPP]
        while True:
            roles_list = list(roles.keys())
            for player in players:
                role = random.choice(roles_list)
                self.assigned_roles[player] = role
                description = roles[role]
                self.players_in_team[player].role = role
                roles_list.remove(role)

        
            # Check if at least one impostor is present
            if any(role for role in self.assigned_roles.values() if "imposteur" in role.lower()):
                break
            else:
                assigned_roles = {}
                await asyncio.sleep(1)

    async def results(self, ctx):
    # Affiche les rôles de chaque joueur
        player_mentions = "\n".join([
            f"{poste}: {player.mention} - Rôle: {self.players_in_team[player].role}"
            for poste, player in zip(postes, [self.TOP, self.JNG, self.MID, self.ADC, self.SUPP])
        ])
    
        await ctx.send(f"Equipe {self.team_name} :\n{player_mentions}")
    
              