import random
import discord
from discord.ext import commands, tasks
import asyncio
from Team import Team
from Player import Player
from Parser_Team import *
from Parser_Lobby import *


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
async def team(ctx,event ,team_name1=None, index1: int=None, team_name2=None, index2: int=None):
    if event == "create":
        await CreateTeam(ctx)
    elif event == "modify":
        await ModifyTeam(ctx, team_name1, index1, index2)
    elif event == "show":
        await ShowTeams(ctx)
    elif event == "delete":
        await DeleteTeam(ctx, team_name1)
    elif event == "switch":
        await SwitchPlayer(ctx, team_name1, index1, team_name2, index2)
    else:
        await ctx.send("L'event n'est pas reconnu, les events possibles sont : create, modify, show, delete, switch")


@bot.command()
async def lobby(ctx,event ,team_name1=None, team_name2=None, lobby_name=None):
    if event == "create":
        await CreateLobby(ctx, team_name1, team_name2, lobby_name)
    elif event == "delete":
        await DeleteLobby(ctx, lobby_name)
    elif event == "preload":
        await SendRoles(ctx, lobby_name)
    elif event == "start":
        await StartGame(ctx, lobby_name)
    elif event == "stop":
        await StopGame(ctx, lobby_name)
    else:
        await ctx.send("L'event n'est pas reconnu, les events possibles sont : create, delete, send, start")
    

bot.run('MTA5ODY0MTgzNTg2NzUxMjk4Mg.Gmx0h3.mVuueXOiAeBTEB-HI-QqagZDoEyTtajalcmm9w')

