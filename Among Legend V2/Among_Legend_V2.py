# -*- coding: latin-1 -*-
import random
import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv
import sys
from Team import Team
from Parser_Team import *
from Parser_Lobby import *
from Data import *

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

                               
@bot.command()
async def rules(ctx):
    role_list = ""
    for role in roles.keys():
        role_list += f"\n\n{role} {roles[role]['emoji']}:\n{roles[role]['description']}"
    await ctx.send(f"Le jeu se d�roule comme une partie normale de League of Legends, mais des r�les sont assign�s et les joueurs peuvent avoir des objectifs un peu diff�rents. Les r�les sont :{role_list}")

@bot.command()
async def custom_help(ctx):
    await ctx.send("Les commandes disponibles sont : "
                   "\n !team create <nom_equipe> <@joueur1> <@joueur2> <@joueur3> <@joueur4> <@joueur5>"
                  "\n !team modify <nom_equipe> <index_joueur1> <index_joueur2>"
                 "\n !team show "
                 "\n !team delete <nom_equipe>" 
                 "\n !team switch <nom_equipe1> <index_joueur1> <nom_equipe2> <index_joueur2>" 
                 "\n !lobby create <nom_equipe1> <nom_equipe2> <nom_lobby>" 
                 "\n !lobby delete <nom_lobby>" 
                 "\n !lobby start <nom_lobby>" 
                 "\n !lobby stop <nom_lobby>" 
                 "\n !lobby preload <nom_lobby>"
                 "\n !rules" 
                 "\n !help")
    

@bot.command()
async def team(ctx,event, arg1=None, arg2=None, Arg3=None, Arg4=None):
    if event == "create":
        await CreateTeam(ctx)
    elif event == "show":
        await ShowTeams(ctx)
    elif event == "delete":
        team_name1 = arg1
        await DeleteTeam(ctx, team_name1)
    elif event == "switch":
        team_name1 = arg1
        index1 = int(arg2)
        team_name2 = Arg3
        index2 = int(Arg4)
        await SwitchPlayer(ctx, team_name1, index1, team_name2, index2)
    else:
        await ctx.send("L'�v�nement n'est pas reconnu, les �v�nements possibles sont : create, modify, show, delete, switch")


@bot.command()
async def lobby(ctx,event, lobby_name=None ,team_name1=None, team_name2=None):
    if event == "create":
        await CreateLobby(ctx, team_name1, team_name2, lobby_name)
    elif event == "delete":
        await DeleteLobby(ctx, lobby_name)
    elif event == "preload":
        await SendRoles(ctx, lobby_name)
    elif event == "start":
        await StartGame(ctx, lobby_name)
    elif event == "stop":
        
        try:
            team_name1, team_name2 = await test_stop_game(ctx, lobby_name)
        except:
            return
        
        # Get the information of the game
        # Ask the two teams for the information
        async def Get_info(ctx, team_name):
            await ctx.channel.send(
                f"La partie est sur le point de se terminer. Veuillez fournir les informations suivantes en mentionnant les personnes concern�es pour les informations suivantes dans la team {team_name} (dans le m�me ordre):"
                "\n victoire/d�faite, top kill, top mort, top d�g�ts, pire participation aux kill"
            )

            def check(response_message):
                # Verify that the message is from the same author and channel
              return (
                    response_message.author == ctx.author
                    and response_message.channel == ctx.channel
                    and len(response_message.raw_mentions) == 4
                    and ("victoire" in response_message.content.lower() or "defaite" in response_message.content.lower())
                )
        

            try:
                # Wait for a response with the check
                response = await bot.wait_for("message", check=check, timeout=300)
                await ctx.channel.send(f"Merci pour les informations ! Vous avez r�pondu : {response.content}")
            except asyncio.TimeoutError:
                await ctx.channel.send("Le temps imparti pour la r�ponse est �coul�.")

            await bot.process_commands(response)
            
            return response
        
        #
        # Check the syntax   
        #    
        async def Get_vote(player):
            await player.discord_infos.send(
                    ".\n Quels r�les pensez-vous qu'ont vos alli�s, envoyez dans l'ordre des postes de la game"
                    "\n Exemple: si je suis mid et que je pense que le top est imposteur, le jgl super-h�ros, l'adc romeo et le supp Serpentin il faut envoyer:"
                    "\n Imposteur, Super-heros, Romeo, Serpentin"
                    "\n Faites attention � la syntaxe, il est conseill� de copier-coller au cas o� :"
                    "\n Imposteur, Serpentin, Double-face, Super-h�ros, Agent double, Romeo, Innovateur"
                )
            
            try:
                vote_original = await bot.wait_for("message",check=lambda m: m.author == player.discord_infos, timeout=120)  
                vote = vote_original.content.split(",")
                player.vote = vote
                await player.discord_infos.send(f"Vous avez vot� pour {vote_original}")
            except asyncio.TimeoutError:
                await player.discord_infos.send("Le temps imparti pour la r�ponse est �coul�.")
            

        response_team1 = await Get_info(ctx, team_name1)
        response_team2 = await Get_info(ctx, team_name2)
        
        
        # Get the vote of the players
        vote_tasks = [Get_vote(player) for team_name in [team_name1, team_name2] for player in teams[team_name].players_in_team.values()]
        await asyncio.gather(*vote_tasks)
                


        await StopGame(ctx, lobby_name, response_team1, response_team2)
    else:
        await ctx.send("L'�v�nement n'est pas reconnu, les �v�nements possibles sont : create, delete, send, start")
    

# Load the environment variables .env
load_dotenv(sys.path[1]+"/.env")

# Get the discord token
discord_token = os.getenv('DISCORD_TOKEN')
        
bot.run(discord_token)