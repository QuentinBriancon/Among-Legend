# -*- coding: latin-1 -*-
import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player


teams={}

# Create a team with the given name and players
async def CreateTeam(ctx):
    content = ctx.message.content
    command = "team create"  
    mentions = ctx.message.mentions  # Lisist of the mentions
    
    # Extract the team name from the message
    team_name = content.replace(f"!{command}", "")
    for mention in mentions:
        team_name = team_name.replace(mention.mention, "")
    team_name = team_name.strip(" ")

    if team_name in teams:
        await ctx.send(f"L'équipe {team_name} existe déjà. Supprimer une équipe en utilisant !team delete <nom de l'équipe>.")
        return
    
    if team_name == "":
        await ctx.send(f"Vous devez donner un nom à votre équipe.")
        return

    teams[team_name] = Team()
    await teams[team_name].create_team(ctx, team_name)


# Print the teams
async def ShowTeams(ctx):
    if teams == {}:
        await ctx.send(f"Aucune équipe n'a été créée pour le moment. Créez une équipe en utilisant !team create <nom de l'équipe>.")
        return
    for team_name  in teams:
        await teams[team_name].show_team(ctx)


# Delete the team with the given name
async def DeleteTeam(ctx, team_name):
    if team_name not in teams:
        await ctx.send(f"L'équipe {team_name} n'existe pas.")
        return
    del teams[team_name]
    await ctx.send(f"L'équipe {team_name} a été supprimée.")

# Exchange two players between two teams
#pb
#
async def SwitchPlayer(ctx, team_name1, index1: int, team_name2, index2: int):
    if team_name1 not in teams or team_name2 not in teams:
        if team_name1 not in teams:
            await ctx.send(f"L'équipe {team_name1} n'existe pas. Créez une équipe en utilisant !team create <nom de l'équipe>.")
            return
        else:
            await ctx.send(f"L'équipe {team_name2} n'existe pas. Créez une équipe en utilisant !team create <nom de l'équipe>.")
            return
        
    index1 -= 1
    index2 -= 1
    
    if 0 <= index1 < len(teams[team_name1].players_in_team) and 0 <= index2 < len(teams[team_name2].players_in_team):

        players_team1 = [teams[team_name1].TOP, teams[team_name1].JGL, teams[team_name1].MID, teams[team_name1].ADC, teams[team_name1].SUPP]
        players_team2 = [teams[team_name2].TOP, teams[team_name2].JGL, teams[team_name2].MID, teams[team_name2].ADC, teams[team_name2].SUPP]
        players_team1[index1], players_team2[index2] = players_team2[index2], players_team1[index1]
    
    
        teams[team_name1].define_team(players_team1)
        teams[team_name2].define_team(players_team2)
    
        # exchange the player objects
        teams[team_name1].players_in_team[players_team1[index1]], teams[team_name2].players_in_team[players_team2[index2]] = teams[team_name2].players_in_team[players_team2[index2]], teams[team_name1].players_in_team[players_team1[index1]]
    
        await ctx.send(f"Les joueurs {players_team1[index1]} et {players_team2[index2]} ont été échangés entre les équipes {team_name1} et {team_name2}.")
    
    else:
        await ctx.send(f"Les indices doivent être entre 1 et 5.")
        return
    
#Ajouter un joueur ne peut etre que dans une equipe au total