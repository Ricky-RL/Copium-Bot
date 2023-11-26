import discord
import responses
from discord.ext import commands
from secrets import TOKEN
from datetime import datetime
from data import allchamp, people
import random


members_global = []
response_list = {}


async def send_message(members, message):
        for member in members:
            if 'iplaygam' in member.name:
                try:
                    await member.send(message)
                except discord.Forbidden:
                    # Handle the case where sending a message is forbidden
                    print(f"Could not send a message to {member.name}")

            # if  'jaycsee' in member.name:
            #     try:
            #         await member.send(message)
            #     except discord.Forbidden:
            #         # Handle the case where sending a message is forbidden
            #         print(f"Could not send a message to {message.author.name}#{message.author.discriminator}.")
            # if 'epickc123' in member.name:
            #     try:
            #         await member.send(message)
            #     except discord.Forbidden:
            #         # Handle the case where sending a message is forbidden
            #         print(f"Could not send a message to {member.name}")

            # if  'masterfireking' in member.name:
            #     try:
            #         await member.send(message)
            #     except discord.Forbidden:
            #         # Handle the case where sending a message is forbidden
            #         print(f"Could not send a message to {message.author.name}#{message.author.discriminator}.")
            # if 'warscout101' in member.name:
            #     try:
            #         await member.send(message)
            #     except discord.Forbidden:
            #         # Handle the case where sending a message is forbidden
            #         print(f"Could not send a message to {member.name}")





def run_discord_bot():
    intents = discord.Intents.default()
    intents.typing = True
    intents.messages = True
    intents.message_content = True
    intents.members = True
    #client = discord.Client(intents=intents)
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is running!')


    @client.command(name='league')
    async def list_members(ctx):
        guild = ctx.guild

        # Fetch all members in the guild
        async for member in guild.fetch_members(limit=None):
            pass  

        members = guild.members
        global members_global
        members_global = members

        message = 'leagueee'
        await send_message(members, message)
        message = 'to respond yes or no, please type y or n preceded by `?`. Example: `?y` `?n`'
        await send_message(members, message)
        message = 'if you need more time, please enter the amount of time you require in minutes with a number in minutes preceded by `?`. Example: `?10`'
        await send_message(members, message)
        message = 'Use `?help` to see a complete list of commands'
        await send_message(members, message)

        # message = 'also just dm me if you need more time cuz i havent tested this shit yet and idk if it works'
        # await send_message(members, message)


                

    @client.event
    async def on_message(message):
        members = members_global
        # Ignore messages from the bot itself to avoid an infinite loop
        if message.author == client.user:
            return
        
        response_prefix = '?'

        user_message = message.content[len(response_prefix):].strip()
        global response_list


        if isinstance(message.channel, discord.DMChannel):
            # Message sent in DM
            user_message = message.content.strip()
            print(f'{message.author}: {user_message}')
            if(message.content.startswith(response_prefix)):
                user_message = message.content[len(response_prefix):].strip()
                current_time = datetime.now().strftime("%H:%M:%S")
                if(user_message.isdigit()):
                    time = int(user_message)
                    if time > 60:
                        await message.author.send(f"we arent waiting that long dipshiit")
                        return
                    await message.author.send(f"ok, forwarding a {user_message} minute delay to everyone else")
                    response_message = f"{message.author} will be ready in {time} minutes"
                    response_list[str(message.author)] = f"{current_time}: {message.author} will be ready in {user_message} minutes"
                    await send_message(members, response_message)
                    return
                elif(user_message.lower() == 'y'):
                    await message.author.send(f"ok, forwarding a 'yes' response to everyone else")
                    response_message = f"{message.author} is playing"
                    response_list[str(message.author)] = f"{current_time}: {message.author} is coming"
                    await send_message(members, response_message)
                    return
                elif(user_message.lower() == 'n'):
                    await message.author.send(f"ok, forwarding a 'no' response to everyone else")
                    response_message = f"{message.author} is not playing"
                    response_list[str(message.author)] = f"{current_time}: {message.author} is not coming"
                    await send_message(members, response_message)
                    return                
                elif(user_message.lower() == 'help'):
                    await message.author.send(f"`?y`: confirm that you are playing tonight\n`?n`: confirm that you are not playing tonight\n`?{{time in minute(s)}}`: request a delay of the specified length. Ex `?10`\n`?list`: view the people that have already responsed\n`?recommend`: propreiteary trained via deep neural net model custom gpt ML algorithm that recommends items based on projected player performance\n`?clear`: clears the list of players that are coming to play\n`?remind`: send a reminder to all players that have yet to respond")
                elif(user_message.lower() == 'recommend'):
                    await message.author.send(f"idk play {random.choice(allchamp)} or something")
                elif(user_message.lower() == 'list'):
                    print(response_list)
                    if response_list:
                        await message.author.send('\n'.join(response_list.values())) 
                    else:
                        await message.author.send('no one has responded yet. Maybe be the first to respond??')
                elif(user_message.lower() == 'clear'):
                    if str(message.author) == 'iplaygam':
                        response_list = {}
                        await message.author.send('cleared')
                    else:
                        await message.author.send('bold of you to assume I would let you delete this dictionary')
                elif(user_message.lower() == 'remind'):
                    temp_members = []
                    temp_people = people
                    for member in members:
                        for key in response_list:
                            if key and key == member.name:
                                temp_people.remove(key)

                    for member in members:
                        for player in people:
                            if member.name == player:   
                                temp_members.append(member)
                                await send_message(temp_members, f'{member.mention} a reminder to hurry up, courtesy of {message.author}')
                                temp_members = []

                else:
                    await message.author.send(f"invalid input. Please enter a valid command")


            if(message.content.startswith('*')):
                user_message = message.content[len(response_prefix):].strip()
                message = f"{message.author}: {user_message}"
                await send_message(members, message)
                return

            # response = responses.handle_response(user_message)
            # try: 
            #     await message.author.send(response)
            # except discord.Forbidden:
            #     print("error")
            
        else:
            await client.process_commands(message)

    client.run(TOKEN)