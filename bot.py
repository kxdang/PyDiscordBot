import discord
import asyncio
import myToken
import calendar
import time
import math
from pprint import pprint


# vars that we need to keep
ourServer = None
CSGOvoicechannel = None
Overwatchvoicechannel = None
serverName = "Kienserver"
gameStart = {}
client = discord.Client()
testcard = "################# \n\n" + "Kien" + "\nGame: " + "CSGO" + "\n" + "Duration: " + "30" + " minute(s)" "\n\n#################"



@client.event
async def on_ready():
    global ourServer
    global CSGOvoicechannel
    global Overwatchvoicechannel
    global discordchat
    global rocketleaguevoice 
    global leagueoflegend                                                                                                                       
    global General
    

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    t = iter(client.servers)
    for server in t:
        # we're trying to find one that has serverName (line 20)
        if(server.name == serverName):
            # found it, lets hold on to it for later
            ourServer = server
            # In this server, hold on the voice channels for moving purposes later,
            for channel in ourServer.channels:
                if channel.name == "CS:GO":
                    CSGOvoicechannel = channel
                elif channel.name == "Overwatch":
                    Overwatchvoicechannel = channel
                elif channel.name == "discordchat":
                    discordchat = channel
                elif channel.name == "General":
                    General = channel
                elif channel.name == "Rocket League":
                    rocketleaguevoice = channel
                elif channel.name == "League of Legends":
                    leagueoflegend = channel

    await client.send_message(discordchat, "**Goliath online. All systems functional.**")




@client.event
async def on_member_update(before, after):
    global gameStart


    if before.game != None and after.game == None and gameStart.get(after.name): #GAME END


        timeCalculation = str(math.ceil((calendar.timegm(time.gmtime()) - gameStart.get(after.name))/60)) ## Calculates time duration in minutes

        print(timeCalculation)
        print(gameStart)

        text = str("########### Game Ended ############# \n\n" + after.name + "\nGame: " + before.game.name + "\n" + "Duration played: " + timeCalculation + " minutes" "\n\n#################################")
                    
        await client.send_message(discordchat, text)

        await client.move_member(after, General)

        del gameStart[after.name]

        print(gameStart)

    elif before.game == None and after.game != None: ## If user wasn't playing a game and then started a game, it will run through the list of games to determine which channels to be inserted in
        if after.game.name == 'Counter-Strike: Global Offensive':
            await client.send_message(discordchat, "**"+after.name+"**" + " is playing " + "*"+after.game.name+"*" + ". Moving " + after.name + " to CS:GO voice channel!")
            await client.move_member(before, CSGOvoicechannel)
        
            gameStart[after.name] = calendar.timegm(time.gmtime()) ## this puts user in the dictionary with the start time and then is used in timeCalculation to see how many time has been elapsed
            print(gameStart)

        elif after.game.name == 'Overwatch':
            await client.send_message(discordchat, "**"+after.name+"**" + " is playing " + "*"+after.game.name+"*" + ". Moving " + after.name + " to Overwatch voice channel!")
            await client.move_member(before, Overwatchvoicechannel)

            gameStart[after.name] = calendar.timegm(time.gmtime())


        elif after.game.name == 'Rocket League':
            await client.send_message(discordchat, "**"+after.name+"**" + " is playing " + "*"+after.game.name+"*" + ". Moving " + after.name + " to Rocket League voice channel!") 
            await client.move_member(before, rocketleaguevoice)

            gameStart[after.name] = calendar.timegm(time.gmtime())

        elif after.game.name == 'League of Legends':
            await client.send_message(discordchat, "**"+after.name+"**"+ " is playing " + "*"+after.game.name+"*" + ". Moving " + after.name + " to League of Legends voice channel!") 
            await client.move_member(before, leagueoflegend)

            gameStart[after.name] = calendar.timegm(time.gmtime())
          
        elif after.game.name != None: #if user is playing any other game, assume its casual and can talk to everyone in general voice channel
            await client.send_message(discordchat, "**"+after.name+"**" + " is playing " + "*"+after.game.name+"*" + ". Casual game detected... Feel free to talk to " + after.name + " in general voice channel!") 

            gameStart[after.name] = calendar.timegm(time.gmtime())


            
    


#clear current chat while bot is running, only clears messages for the duration that the bot is ran
async def clear_chat_channel(message):
    currentChannel = message.channel.id
    print(currentChannel)
    listofmessages = []

    for m in client.messages:
        print(m.content)
        if m.channel.id == currentChannel:
            listofmessages.append(m)

    await client.delete_messages(listofmessages)

    # for m in message.channel:
    #     if m.channel == discordstats:
    #         client.delete_messages(m)

@client.event
async def on_message(message):
    loweredCase = message.content.lower()
    if loweredCase.startswith('!clear'):
        await clear_chat_channel(message)
        print('clearing chat')
        await client.send_message(message.channel, "Chat has been cleared.")

    if loweredCase.startswith('!hello'):
        await client.send_message(message.channel, "Hello world")

    if loweredCase.startswith('!info'):
        await client.send_message(message.channel, "Sorry, you have been unlucky to access the command. Please try again :D")
    if loweredCase.startswith('!printcard'):
        await client.send_message(message.channel, testcard)
        print(type(testcard))



client.run(myToken.token)
