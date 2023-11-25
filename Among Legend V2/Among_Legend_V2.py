import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player
from Parser_Team import *
from Parser_Lobby import *

#########
#########  COMMANDE A CHANGER
######## 


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
    for role, description in Team.roles.items():
        role_list += f"\n\n{role}:\n{description}"
    await ctx.send(f"Le jeu se deroule comme une partie normale de league of legends mais des roles sont assignes et les joueurs peuvent avoir des objectifs un peu differents. Les roles sont :{role_list}")

@bot.command()
async def team(ctx,event, arg1=None, arg2=None, Arg3=None, Arg4=None):
    if event == "create":
        await CreateTeam(ctx)
    elif event == "modify":
        team_name1= arg1
        index1 = int(arg2)
        index2 = int(Arg3)
        await ModifyTeam(ctx, team_name1, index1, index2)
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
        await ctx.send("L'event n'est pas reconnu, les events possibles sont : create, modify, show, delete, switch")


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
        await ctx.channel.send(
            "La partie est sur le point de se terminer. Veuillez fournir les informations suivantes en mentionnant les personnes concernees pour les informations (dans le meme ordre):"
            "\n victoire/defaite, top kill, top mort, top degats, pire participation aux kill"
        )

        def check(response_message):
            # Vérifie que le message provient du même utilisateur et du même salon
          return (
                response_message.author == ctx.author
                and response_message.channel == ctx.channel
                and len(response_message.raw_mentions) == 4
                and ("victoire" in response_message.content.lower() or "defaite" in response_message.content.lower())
            )
        

        try:
            # Attend une réponse pendant 120 secondes
            response = await bot.wait_for("message", check=check, timeout=120)
            await ctx.channel.send(f"Merci pour les informations ! Vous avez répondu : {response.content}")
        except asyncio.TimeoutError:
            await ctx.channel.send("Le temps imparti pour la réponse est écoulé.")

        await bot.process_commands(response)
        await StopGame(ctx, lobby_name, response)
    else:
        await ctx.send("L'event n'est pas reconnu, les events possibles sont : create, delete, send, start")
    

        
bot.run('MTA5ODY0MTgzNTg2NzUxMjk4Mg.Gmx0h3.mVuueXOiAeBTEB-HI-QqagZDoEyTtajalcmm9w')

