import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import subprocess
import json

#Basic discord python stuff
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!', help_command=None)
process = None


#Gets all the info from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
IP = os.getenv("IP")
ADMIN_ID = os.getenv("ADMIN_ID")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def help(ctx):
    await ctx.send('!on: \t\tTurns the server on')
    await ctx.send('!off: \t\tTurns the server off')
    await ctx.send('!status: \t\tChecks the server status')
    await ctx.send('!ping: \t\tCheck if the bot is up')
    await ctx.send('!help: \t\tShows commands')
    await ctx.send("!playerCount: \t\tGives the amount of players on.")
    await ctx.send("!players: \t\tGives the names of players on.")
    await ctx.send('***PLEASE TURN OFF THE SERVER ONCE YOU ARE DONE***')



@bot.command()
async def status(ctx):
    # Gets status of the bot 
    if get_status():
        await ctx.send("Server is up")
    else:
        await ctx.send("Server is down")


@bot.command()
async def shutdown(ctx):
    #Makes sure the author is the admin listed in the .env
    if str(ctx.author.id) == str(ADMIN_ID): 
        await ctx.send("Shutting down...")
        #turns off the bot
        await bot.close()
    else:
        await ctx.send("You do not have permission to shut down the bot.")
    

@bot.command()
async def on(ctx):
    if get_status():
        await ctx.send("Server is already on")
    else:
        #Turn on the server by using the subproceesses 
        await ctx.send("Starting server. It will be up in a moment")
        global process
        process = subprocess.Popen("start.bat", shell=True, stdin=subprocess.PIPE)
        #when the server is on according to the website send a message
        while get_status() == False:
            await asyncio.sleep(1)
        await ctx.send("Server is up")
 
@bot.command()
async def off(ctx):
    #Turns the server off by writing stop to the stdin 
    global process
    if process is not None:
        await ctx.send("Stopping server")
        process.stdin.write(b'stop\n')
        process.stdin.flush()

        #Wait until the server is stopped and then continue
        while get_status():
            await asyncio.sleep(1)
        await ctx.send("Server is off")
         # Terminate the process
        process.terminate()
        # Wait briefly for the process to terminate
        process.wait(timeout=5)
        process = None
    else:
        await ctx.send("Server is already off")

@bot.command()
async def playerCount(ctx):
    #Gets the amount of people on using the API
    if not get_status():
        await ctx.send("Server is off, no players currently on")
    else:
        url = f"https://api.mcsrvstat.us/3/{IP}"
        response = requests.get(url)
        response = json.loads(response.text)
        await ctx.send(f"There are {response['players']['online']} player(s) online.")

@bot.command()
async def players(ctx):
    if not get_status():
        await ctx.send("Server is off, no players currently on")
    else:
        #Gets the amount of players using the api
        url = f"https://api.mcsrvstat.us/3/{IP}"
        try:
            response = requests.get(url)
            response = json.loads(response.text)["players"]["list"]
            people =[]
            for person in response:
                people.append(person["name"])
            if len(people) > 0:
                await ctx.send(f"The players on are: {', '.join(people)}")
            else:
                await ctx.send("There is no one on.")
        except:
            await ctx.send("API is being slow. Try again in a minute or so.")
        
        
@bot.command()
async def command(ctx, arg):
    #Broken, WIP, want to allow running commands from the user
    if str(ctx.author.id) == str(ADMIN_ID): 
        global process
        if process is not None:
            command_string = arg + '\n'
            process.stdin.write(command_string.encode('utf-8'))
            process.stdin.flush()
    else:
        await ctx.send("You do not have permission to run commands.")
        

def get_status():
    #Get status functiont that uses the base IP because it is not cached.
    url = f"https://mcsrvstat.us/server/{IP}"
    response = requests.get(url)
    if "Could not get the server status" in response.text:
        return False
    else:
        return True

bot.run(DISCORD_TOKEN)