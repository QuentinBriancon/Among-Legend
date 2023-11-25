import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team



class Player:
    
    def __init__(self, team, poste, name, discord_id):
        self.role = ""
        self.team = team
        self.poste = poste
        self.score = 0
        self.game_in_progress = False
        self.discord_name = name
        self.discord_id = discord_id
        self.state_doubleface = ""
        self.vote = []
        
    async def notify_special_roles(self, ctx):
            role = self.role
            if role == "Double-face":
                asyncio.create_task(self.notify_double_face())
            elif role == "Romeo":
                await self.notify_romeo()

        
    #Notifier le double face selon s'il doit gagner la partie ou la perdre, cela change a des moments aleatoire tant que la partie est en cours
    async def notify_double_face(self):
        while self.game_in_progress:
            rand_time = random.randint(0, 10)*60        
            if random.choice([True, False]):
                await self.discord_name.send("Tu dois gagner la partie.")
                self.state_doubleface = "victoire"
            else:
                await self.discord_name.send("Tu dois perdre la partie.")
                self.state_doubleface = "defaite"
                
            await asyncio.sleep(rand_time) 
            
#Notifier le romeo de son amour secret
    async def notify_romeo(self):
        team = random.choice(["alliee", "ennemie"])
        poste_list = ["TOP","JGL","MID","ADC","SUPP"]
        if team == "alliee":
            poste_list.remove(self.poste)
            poste = random.choice(poste_list)
            await self.discord_name.send(f"Ton amour secret dans l'equipe alliee, il joue {poste}.")
        else:
            poste = random.choice(poste_list)
            await self.discord_name.send(f"Ton amour secret dans l'equipe ennemie, il joue {poste}.")
            

#Recuperer le vote du joueur
    async def get_vote(self, response):
        await self.discord_name.send(f"Quels roles pensez vous qu'ont vos alliee, envoyez dans l'odre des postes de la game")
        
            
    #Calculer le score du joueur selon son role et le resultat de la partie
    def player_objective(self, response):
        
        for mention in response.mentions:
            result = response.replace(mention.mention, "")
        result = result.strip(" ")
        
        top_kill = (response.raw_mentions[0] == self.discord_id)
        top_mort = (response.raw_mentions[1] == self.discord_id)
        top_degats = (response.raw_mentions[2] == self.discord_id)
        worst_participation = (response.raw_mentions[3] == self.discord_id)


        if self.role == "Double-face":
            if self.state_doubleface == result:
                self.score += 1
            else:
                self.score -= 1
                
        elif self.role == "Super-heros":
            if result == "defaite":
                self.score -= 2

        else:
            for role in Team.roles.keys():
                if self.role == role:
                    
                    condition_valid = True
                    
                    if Team.roles[role]["conditions"]["result_game"] == 1:
                        if result == "defaite":
                            condition_valid = False
                            
                    elif Team.roles[role]["conditions"]["result_game"] == 0:
                        if result == "victoire":
                            condition_valid = False
                     
                    if Team.roles[role]["conditions"]["top_kill"] == 1:
                        if not top_kill:
                            condition_valid = False
                            
                    if Team.roles[role]["conditions"]["top_mort"] == 1:   
                        if not top_mort:
                            condition_valid = False

                                
                    if Team.roles[role]["conditions"]["top_degats"] == 1:
                        if not top_degats:
                            condition_valid = False

                                
                    if Team.roles[role]["conditions"]["worst_participation"] == 1:
                        if not worst_participation:
                            condition_valid = False
                                
                                
                    if condition_valid:
                        self.score += 3
                    else:
                        self.score -= 3

                    