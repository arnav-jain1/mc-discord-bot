# mc-discord-bot
## Info
Python program that creates a discord bot to control a minecraft server \
Supported commands: 
* !on: Turns the server on.
* !off: Turns the server off.
* !status: Checks the server status.
* !ping: Check if the bot is up and running.
* !help: Shows the available commands.
* !playerCount: Gives the amount of players currently on the server.
* !players: Provides the names of the players currently on the server.
* !shutdown: Turns off the bot (requires bot owner)
* !help: lists commands

Future commands in progress: !kick, !ban, admin privileges
## How to run
1. Create a minecraft server
2. In the server folder, create a start.bat with the command to start the server
3. Download the bot.py and save it inside the server folder
4. Install dependencies (pip install -r requirements.txt)
5. Create a .env file with IP, DISCORD_TOKEN, and ADMIN_ID (discord ID of user that is running the server)
6. Run the bot
