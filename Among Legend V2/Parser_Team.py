import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player


teams={}

# Crée l'équipe
async def CreateTeam(ctx):
    content = ctx.message.content
    command = ctx.command.name  # Nom de la commande utilisée (dans ce cas, "CreateTeam")
    mentions = ctx.message.mentions  # Liste des mentions dans le message
    
    # Extrait le contenu qui n'est ni les mentions ni la commande
    team_name = content.replace(f"!{command}", "")
    for mention in mentions:
        team_name = team_name.replace(mention.mention, "")
    team_name = team_name.strip(" ")

    if team_name in teams:
        await ctx.send(f"L'equipe {team_name} existe deja. Supprimer une equipe en utilisant !DeleteTeam.")
        return
    
    if team_name == "":
        await ctx.send(f"Vous devez donner un nom a votre equipe.")
        return

    teams[team_name] = Team()
    await teams[team_name].create_team(ctx, team_name)


# Modifie l'équipe
async def ModifyTeam(ctx, team_name, index1: int, index2: int):
    if team_name not in teams:
        await ctx.send(f"L'equipe {team_name} n'existe pas. Creez une equipe en utilisant !CreateTeam.")
        return
    await teams[team_name].modify(ctx, index1, index2)


# Affiche les équipes
async def ShowTeams(ctx):
    if teams == {}:
        await ctx.send(f"Aucune equipe n'a ete creee pour le moment. Creez une equipe en utilisant !CreateTeam.")
        return
    for team_name  in teams:
        await teams[team_name].show_team(ctx)


# Supprime l'équipe
async def DeleteTeam(ctx, team_name):
    if team_name not in teams:
        await ctx.send(f"L'equipe {team_name} n'existe pas.")
        return
    del teams[team_name]
    await ctx.send(f"L'equipe {team_name} a ete supprimee.")

#Echange deux joueurs entre deux equipes
async def SwitchPlayer(ctx, team_name1, index1: int, team_name2, index2: int):
    if team_name1 not in teams or team_name2 not in teams:
        if team_name1 not in teams:
            await ctx.send(f"L'equipe {team_name1} n'existe pas. Creez une equipe en utilisant !CreateTeam.")
            return
        else:
            await ctx.send(f"L'equipe {team_name2} n'existe pas. Creez une equipe en utilisant !CreateTeam.")
            return
        
    index1 -= 1
    index2 -= 1
    
    players_team1 = [teams[team_name1].TOP, teams[team_name1].JNG, teams[team_name1].MID, teams[team_name1].ADC, teams[team_name1].SUPP]
    players_team2 = [teams[team_name2].TOP, teams[team_name2].JNG, teams[team_name2].MID, teams[team_name2].ADC, teams[team_name2].SUPP]
    players_team1[index1], players_team2[index2] = players_team2[index2], players_team1[index1]
    
    
    teams[team_name1].define_team(players_team1)
    teams[team_name2].define_team(players_team2)
    
    await ctx.send(f"Les joueurs {players_team1[index1]} et {players_team2[index2]} ont ete echanges entre les equipes {team_name1} et {team_name2}.")
    
#Ajouter un joueur ne peut etre que dans une equipe au total

