import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player
from Parser_Team import *


lobbies={}

# Create a lobby between two teams with the given name
async def CreateLobby(ctx, team_name1, team_name2 ,lobby_name):
    
    if team_name1 not in teams or team_name2 not in teams:
        if team_name1 not in teams:
            await ctx.send(f"L'équipe {team_name1} n'existe pas. Créez une équipe en utilisant !team create <nom de l'équipe>")
            return
        else:
            await ctx.send(f"L'équipe {team_name2} n'existe pas. Créez une équipe en utilisant !team create <nom de l'équipe>.")
            return
        
    if lobby_name in lobbies:
        await ctx.send(f"Le lobby {lobby_name} existe déjà. Supprimer un lobby en utilisant !lobby delete.")
        return
    lobbies[lobby_name]= [team_name1, team_name2, False]
    
    if lobby_name == "":
        await ctx.send(f"Vous devez donner un nom à votre lobby.")
        return
        
    await ctx.send(f"Le lobby entre les équipes {team_name1} et {team_name2} a été créé.")
    await ctx.send(f"Les équipes {team_name1} et {team_name2} sont :")
    await teams[team_name1].show_team(ctx)
    await teams[team_name2].show_team(ctx)
    # -*- coding: latin-1 -*-


# Delete the lobby with the given name
async def DeleteLobby(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    del lobbies[lobby_name]
    await ctx.send(f"Le lobby {lobby_name} a été supprimé.")


# Send the roles to the players in the lobby
async def SendRoles(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas. Créez un lobby avec !lobby create <nom du lobby>")
        return
    
    await ctx.send("Les joueurs vont se voir répartir leur rôle.")
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
    
    if role_attribue == True:
        await ctx.send(f"Les rôles ont déjà été assignés. Utilisez !game start {lobby_name}.")
        return
    
    for team_name in [team_name1, team_name2]:
        await teams[team_name].assign_roles(ctx)
        await ctx.send(f"Les rôles ont été assignés pour la team {team_name}. Les joueurs vont les recevoir en MP.")
        await teams[team_name].send_roles()
    
    lobbies[lobby_name][2] = True
        
# Launch the game for the lobby
async def StartGame(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    
    await ctx.send("La partie va commencer.")
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
    if role_attribue == False:
        await ctx.send("Les rôles n'ont pas été assignés. Utilisez !lobby preload.")
        return
    
    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():
            await player.notify_special_roles(ctx)
            player.game_in_progress = True


# Test if the game can be stopped
async def test_stop_game(ctx, lobby_name):
    if lobby_name not in lobbies:
        await ctx.send(f"Le lobby {lobby_name} n'existe pas.")
        return
    
    if lobby_name == "":
        await ctx.send(f"Vous devez donner un nom à votre lobby.")
        return
    
    team_name1, team_name2, role_attribue = lobbies[lobby_name]
    
    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():
            if player.game_in_progress == False:
                await ctx.send(f"La partie n'est pas en cours. Utilisez !lobby start {lobby_name}.")
                return
    return team_name1, team_name2

# Stop the game for the lobby
async def StopGame(ctx, lobby_name, response_team1, response_team2):
    
    await ctx.send("La partie va s'arrêter.")
    
    team_name1, team_name2, role_attribue = lobbies[lobby_name]

    # Calculate the score    
    
    # Objectives
    for team_name, response in zip([team_name1, team_name2], [response_team1, response_team2]):
        team = teams[team_name]
        for player in team.players_in_team.values():        
            player.player_objective(response)

    # Votes
    for team_name in [team_name1, team_name2]:
        await teams[team_name].vote(ctx)
        
        
    # Results

    for team_name in [team_name1, team_name2]:
        await teams[team_name].results(ctx)
    
    # Reset the game
    for team_name in [team_name1, team_name2]:
        team = teams[team_name]
        for player in team.players_in_team.values():
            player.game_in_progress = False
            player.role = ""
            team.assigned_roles = {}
    await ctx.send('La partie de Among Legend est terminée. Mais pas le lobby, vous pouvez relancer directement avec !lobby preload Puis !lobby start')
    lobbies[lobby_name][2] = False

    
