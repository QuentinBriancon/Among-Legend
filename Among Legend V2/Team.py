# -*- coding: latin-1 -*-
import random
import discord
from discord.ext import commands, tasks
import asyncio
from Player import Player
from Data import *
     

class Team:

    def __init__(self):
        self.team_name = ""
        self.players_in_team = {}

    async def create_team(self, ctx, team_name):
        players = ctx.message.mentions
        if len(players) != 5:
            await ctx.send('Une équipe est composée de exactement 5 joueurs')
            return
        
        for index, player in enumerate(players):
            self.players_in_team[player] = Player(player)
            
        self.team_name = team_name

        await ctx.send(f"L'équipe {self.team_name} a été créée.")

    # Print the 5 players in the team with their score
    async def show_team(self, ctx):
        message = (f"Équipe {self.team_name} :\n")
        for player in self.players_in_team:
            message += f"{player.mention} - Score: {self.players_in_team[player].score}\n"
        await ctx.send(message)
                       
                        
    async def send_roles(self):
        for player in self.players_in_team:
            role = self.players_in_team[player].role
            description = roles[role]['description']
            await player.send(f"Ton rôle dans Among Legends est : {role}.\nDescription : {description}")
            
    async def assign_roles(self, ctx):
        players_list = list(self.players_in_team.keys())
        impo = random.choice(players_list)        

        roles_list = list(roles.keys())
        roles_list.remove('Imposteur')
        
        for index, player in enumerate(self.players_in_team):
            if players_list[index] == impo:
                self.players_in_team[player].role = 'Imposteur'
                continue
            else:
                role = random.choice(roles_list)
                self.players_in_team[player].role = role
                roles_list.remove(role)
            

    async def results(self, ctx):
    # Print the results of the game
        player_mentions = "\n".join([
            f"{player.mention} - Rôle: {self.players_in_team[player].role} - Score: {self.players_in_team[player].score}"
            for player in self.players_in_team
        ])
    
        await ctx.send(f"Équipe {self.team_name} :\n{player_mentions}")
        
    async def vote(self, ctx):        
        # Calculate the score of the players according to the votes
        players_list = list(self.players_in_team.keys())
        for index_player, player in enumerate(self.players_in_team):
            for index_vote, vote in enumerate(self.players_in_team[player].vote):
                if index_vote >= index_player:
                    index = index_vote + 1
                else:
                    index = index_vote
                    
                if vote == self.players_in_team[players_list[index]].role:
                    self.players_in_team[player].score += 1
                    self.players_in_team[players_list[index]].score -= 1