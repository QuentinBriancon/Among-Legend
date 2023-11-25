import random
import discord
from discord.ext import commands, tasks
import asyncio



class Player:
    
    def __init__(self):
        self.role = None
        self.team = None
        self.poste = None
        self.score = 0
        self.game_in_progress = False
        
    async def notify_special_roles(self, ctx):
            role = self.role
            if role == "Double-face":
                self.loop.create_task(self.notify_double_face())
            elif role == "Romeo":
                await self.notify_romeo()

        
    #Notifier le double face selon s'il doit gagner la partie ou la perdre, cela change a des moments aleatoire tant que la partie est en cours
    async def notify_double_face(self):
        while self.game_in_progress:
            rand_time = random.randint(0, 10)*60        
        
            if random.choice([True, False]):
                await self.send("Tu dois gagner la partie.")
            else:
                await self.send("Tu dois perdre la partie.")
            await asyncio.sleep(rand_time) 
            
#Notifier le romeo de son amour secret
    async def notify_romeo(self):
        team = random.choice(["alliee", "ennemie"])
        poste_list = ["TOP","JGL","MID","ADC","SUPP"]
        if team == "alliee":
            poste_list.remove(self.poste)
            poste = random.choice(poste_list)
            await self.send(f"Ton amour secret dans l'equipe alliee, il joue {poste}.")
        else:
            poste = random.choice(poste_list)
            await self.send(f"Ton amour secret dans l'equipe ennemie, il joue {poste}.")
            
            
        


  