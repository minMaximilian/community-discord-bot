# EU4 Bot
This is a bot used for a game called Europa Univeralis IV. The main purpose of it is to help keep track of players, track reveservations, add fun commands, use an api to parse saves, and more as needs arise. 

# How to run and install
To run this bot smoothly with little errors, you require docker. First you need to download this

`git clone https://github.com/minMaximilian/community-discord-bot`

Then you need to build the image by running this.

`docker build . -t {Insert the image name here brackets excluded}`

`docker run -e DISCORD_TOKEN={The bot discord token} {whatever you named the file}`

The bot should be succesfully running. If there is any confusion that arises during these instructions please send an issue and I will try to reclarify more succinctly.