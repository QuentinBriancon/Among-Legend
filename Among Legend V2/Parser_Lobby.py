import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player
from Parser_Team import *


lobbies={}

# Crée le lobby
async def CreateLobby(ctx, team_name1, team_name2 ,lobby_name):
    
    if team_name1 not in teams or team_name2 not in teams:
        if team_name1 not in teams:
            await ctx.send(f"L'equipe {team_name1} n'existe pas. Creez une equipe en utilisant !CreateTeam.")
            return
        else:
            await ctx.send(f"L'equipe {team_name2} n'existe pas. Creez une equipe en utilisant !CreateTeam.")
            return
        
    if lobby_name in lobbies:
        await ctx.send(f"Le lobby {lobby_name} existe deja. Supprimer un lobby en utilisant !DeleteLobby.")
        return
    lobbies[lobby_name]= [team_name1, team_name2, False]
    
    if lobby_name == "":
        await ctx.send(f"Vous devez donner un nom a votre lobby.")
        return
        
    await ctx.send(f"Le lobby entre les equipes {team_name1} et {team_name2} a ete cree.")
    await ctx.send(f"Les equipes {team_name1} et {team_name2} sont :")
    await teams[team_name1].show_team(ctx)
    await teams[team_name2].show_team(ctx)
    

# Supprime le lobby
async def DeleteLobby(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    del lobbies[lobby_name]
    await ctx.send(f"Le lobby {lobby_name} a ete supprime.")


# Choix des roles
async def SendRoles(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    
    await ctx.send("Les joueurs vont se voir repartir leur role.")
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
    
    for team_name in [team_name1, team_name2]:
        await teams[team_name].assign_roles(ctx)
        await ctx.send(f"Les roles ont ete assignes pour la team {team_name}. Les joueurs vont les recevoir en MP.")
        await teams[team_name].send_roles()
    
    lobbies[lobby_name][2] = True
        
# Lance la partie avec le lobby donné
async def StartGame(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    
    await ctx.send("La partie va commencer.")
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
    if role_attribue == False:
        await ctx.send("Les roles n'ont pas ete assignes. Utilisez !SendRoles.")
        return
    
    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():
            await player.notify_special_roles(ctx)
            player.game_in_progress = True


# Arrete la partie pour le lobby donne
async def StopGame(ctx, lobby_name, response):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    
    await ctx.send("La partie va s'arreter.")
    
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
 

    #player_vote

    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():        
            player.player_objective(response)


    for team_name in [team_name1, team_name2]:
        await teams[team_name].results(ctx)
    
    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():
            player.game_in_progress = False
            player.role = None
            team.assigned_roles = {}
    await ctx.send('La partie de Among Legend est termine. Mais pas le lobby, vous pouvez relancer directement avec !SendRoles Puis !StartGame')

    
