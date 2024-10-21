import asyncio
import discord
import responses
from discord.ext import commands
from secrets import TOKEN, PROJECT, ZONE, INSTANCE_NAME
from datetime import datetime, timedelta
from data import allchamp, people, help_str
import random
from google.cloud import compute_v1
from google.oauth2 import service_account
from profiles.profiles_db import add_new_profile, fetch_profile, delete_profile

SERVICE_ACCOUNT_FILE = './secrets_gcp.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)

members_global= []
response_list = {}
current_members = set()
operation_results = {2104194: 'DONE', 35394935: 'PENDING', 121282975: 'RUNNING'}
async def send_message(members, message):
        for member in members:
            await member.send(message)
async def handle_instance_start(task, message, client, channel, operation_results, msg):
    # Wait for the task to complete and get the result
    operation = await task

    # Now that the task is done, send the message to the channel
    if channel:
        await channel.send(f'{message.author} {msg} the valheim server\n status: `{operation_results[operation.status] if operation_results[operation.status] else operation.status}`')



async def start_instance(members, author):

    profiles = fetch_profile()
    profile = profiles.get('valheim', None)
    if profile:
        for member in members:
            for player in profile:
                if member.name == player:  
                    current_members.add(member)

    # for member in current_members:
    #     await member.send(f'valheim server is starting')
    print(f"Starting instance: {INSTANCE_NAME}")
    await get_status(current_members)

    client = compute_v1.InstancesClient(credentials=credentials)
    operation = client.start(project=PROJECT, zone=ZONE, instance=INSTANCE_NAME)

    operation.result()  # Wait for the operation to complete
    for member in current_members:    
        await member.send(f'valheim server started by {author}\n status: `{operation_results[operation.status] if operation_results[operation.status] else operation.status}`')

    print('server started')
    return operation

async def stop_instance(members, author):

    profile = fetch_profile('valheim')
    if profile:
        for member in members:
            for player in profile:
                if member.name == player:  
                    current_members.add(member)

    for member in current_members:
        await member.send(f'valheim server is stopping')
    print(f"Stopping instance: {INSTANCE_NAME}")
    await get_status(current_members)

    client = compute_v1.InstancesClient(credentials=credentials)
    operation = client.stop(project=PROJECT, zone=ZONE, instance=INSTANCE_NAME)
    operation.result()
    # operation.result()
    print(f"Stopped instance: {INSTANCE_NAME}")
          
    for member in current_members:
        await member.send(f'valheim server stopped by {author}\nstatus: `{operation_results[operation.status] if operation_results[operation.status] else operation.status}`')


    return operation

async def get_status(members):
    print(f"Getting status of instance: {INSTANCE_NAME}")
    client = compute_v1.InstancesClient(credentials=credentials)
    operation = client.get(project=PROJECT, zone=ZONE, instance=INSTANCE_NAME)
    print(f"Got status of instance: {INSTANCE_NAME}")
    print(operation.status)
    for member in members:
        await member.send(f'valheim server status: `{operation_results[operation.status] if operation.status in operation_results else operation.status}`')
    return

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
        temp_members = []
        for member in members:
            for player in people:
                if member.name == player:   
                    temp_members.append(member)
                    message = f'{member.mention} leagueee\nto respond yes or no, please type y or n preceded by `?`. Example: `?y` `?n`\nif you need more time, please enter the amount of time you require in minutes with a number in minutes preceded by `?`. Example: `?10`\nUse `?help` to see a complete list of commands'
                    await send_message(temp_members, message)
                    temp_members = []

    @client.command(name='overwatch')
    async def list_members(ctx):
        guild = ctx.guild

        # Fetch all members in the guild
        async for member in guild.fetch_members(limit=None):
            pass  

        members = guild.members
        global members_global
        members_global = members
        temp_members = []
        for member in members:
            for player in people:
                if member.name == player:   
                    temp_members.append(member)
                    message = f'{member.mention} overwatch\nto respond yes or no, please type y or n preceded by `?`. Example: `?y` `?n`\nif you need more time, please enter the amount of time you require in minutes with a number in minutes preceded by `?`. Example: `?10`\nUse `?help` to see a complete list of commands'
                    await send_message(temp_members, message)
                    temp_members = []

        # message = 'also just dm me if you need more time cuz i havent tested this shit yet and idk if it works'
        # await send_message(members, message)
    
    @client.command(name='test2')
    async def list_members(ctx):
        guild = ctx.guild

        # Fetch all members in the guild
        async for member in guild.fetch_members(limit=None):
            pass  

        members = guild.members
        global members_global
        members_global = members
        temp_members = []

        for member in members:
            for player in people:
                if member.name == 'iplaygam':   
                    temp_members.append(member)
                    message = f'{member.mention} overwatch\n begin testing'
                    await send_message(temp_members, message)
                    temp_members = []
                    break

    @client.command(name='start')
    async def list_members(ctx):
        guild = ctx.guild

        # Fetch all members in the guild
        async for member in guild.fetch_members(limit=None):
            pass  

        members = [member for member in guild.members if member.name in people]
        global members_global
        members_global = members
        temp_members = []

        for member in members:
            for player in people:
                if member.name == ctx.author.name:   
                    temp_members.append(member)
                    message = f'Bot activated'
                    await send_message(temp_members, message)
                    temp_members = []
                    break

                

    @client.event
    async def on_message(message):
        global current_members

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
                unformatted_current_time = datetime.now()
                current_time = unformatted_current_time.strftime("%I:%M %p")


                if(user_message.isdigit()):
                    time = int(user_message)
                    if time == 69:
                        await message.author.send(f"nice")
                    if time > 69:
                        await message.author.send(f"we arent waiting that long dipshiit")
                        return
                    if time == 0:
                        await message.author.send(f"bruh just respond yes at this point")

                    await message.author.send(f"ok, forwarding a {user_message} minute delay to {[n.name for n in current_members]}")

                    ready_time = (unformatted_current_time + timedelta(minutes=time)).strftime("%I:%M %p")

                    response_message = f"{message.author} will be ready in {time} minutes. They claim to be ready at {ready_time}"
                    response_list[str(message.author)] = f"{current_time}: {message.author} will be ready in {time} minutes. They claim to be ready at {ready_time}"
                    print(current_members)
                    await send_message(current_members, response_message)
                    return
                elif(user_message.lower() == 'y'):
                    await message.author.send(f"ok, forwarding a 'yes' response to {[n.name for n in current_members]}")
                    response_message = f"{message.author} is playing"
                    response_list[str(message.author)] = f"{current_time}: {message.author} is coming"
                    await send_message(current_members, response_message)

                    return
                elif(user_message.lower() == 'n'):
                    await message.author.send(f"ok, forwarding a 'no' response to {[n.name for n in current_members]}")
                    response_message = f"{message.author} is not playing"
                    response_list[str(message.author)] = f"{current_time}: {message.author} is not coming"
                    await send_message(current_members, response_message)
                    return                
                elif(user_message.lower() == 'help'):
                    await message.author.send(help_str)
                elif(user_message.lower() == 'recommend'):
                    await message.author.send(f"idk play {random.choice(allchamp)} or something")
                elif(user_message.lower() == 'list'):
                    print(response_list)
                    if response_list:
                        await message.author.send('\n'.join(response_list.values())) 
                    else:
                        await message.author.send('no one has responded yet. Maybe be the first to respond??')
                elif(user_message.lower() == 'clear'):
                    #if str(message.author) == 'iplaygam':
                    response_list = {}
                    current_members = set()
                    await message.author.send('cleared')
#
                elif(user_message.lower() == 'remind'):
                    temp_members = []
                    temp_people = people
                    for member in members:
                        for key in response_list:
                            if key and key == member.name:
                                temp_people.remove(key)

                    for member in members:
                        for player in temp_people:
                            if member.name == player:   
                                temp_members.append(member)
                                await send_message(temp_members, f'{member.mention} a reminder to hurry up, courtesy of {message.author}')
                                temp_members = []
                elif(user_message.lower() == 'tags'):
                    await message.author.send(f"{people}")

                else:
                    await message.author.send(f"invalid input. Please enter a valid command")


            if(message.content.startswith('*')):
                user_message = message.content[len(response_prefix):].strip()
                message = f"{message.author}: {user_message}"
                await send_message(members, message)
                return
            
            if message.content.startswith('!'):
                user_message = message.content[len(response_prefix):].strip().split(' ')
                print(user_message)
                if user_message[0] == 'create_profile':
                    if len(user_message) < 3:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 3 or more arguments. Received {len(user_message)}")
                        return
                    
                    profile_name = user_message[1]
                    user_message_members = user_message[2:]

                    temp_profile = {profile_name: []}
                    for member in members:
                        for player in user_message_members:
                            if member.name == player:
                                # print(f'player: {player} | member: {member.name}')
                                temp_profile[profile_name].append(player)
                                await message.author.send(f"adding {player} to {profile_name}")
                                # await message.author.send(f"asking {member} to play {user_message[0]}")
                                # await send_message([member], f'{message.author.name} is asking you to play {user_message[0]} bro')     
                    # Read existing profiles from file
                    print(temp_profile)

                    result_message = add_new_profile(profile_name, temp_profile)
                    await message.author.send(result_message)
                elif user_message[0] == 'delete_profile':
                    if len(user_message) < 2:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 2 arguments. Received {len(user_message)}")
                        return
                    
                    profile_name = user_message[1]
                    result_message = delete_profile(profile_name)
                    await message.author.send(result_message)
                elif user_message[0] == 'get_profiles':    
                    result_message = fetch_profile()
                    formatted_message = "Profiles:\n" + "\n".join([f"- {profile}: {', '.join(members)}" for profile, members in result_message.items()])
                    await message.author.send(formatted_message)
                    return
                elif user_message[0] == 'play':
                    current_members = set()
                    if len(user_message) < 2:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 2 or more arguments. Received {len(user_message)}")
                        return
                    profile_name = user_message[1]
                    profiles = fetch_profile()
                    profile = profiles.get(profile_name, None)
                    if profile:
                        for member in members:
                            for player in profile:
                                if member.name == player:  
                                    current_members.add(member)
                                    
                        await message.author.send(f"asking {[n.name for n in current_members]} to play {profile_name}")
                        for member in current_members:
                            await member.send(f'{member.mention}\n{message.author.name} is asking you to play {user_message[1]} bro')
                elif user_message[0] == 'start_server':
                    # operation = await start_instance(members, message.author)
                    # instance_message = 'a'
                    operation_task = asyncio.create_task(start_instance(members, message.author))

                    channel = client.get_channel(1295284991064018945)
                    if channel:
                        operation_task.add_done_callback( lambda task: asyncio.create_task(handle_instance_start(operation_task, message, client, channel, operation_results, 'started'))    )    
                elif user_message[0] == 'stop_server':
                    operation_task = asyncio.create_task(stop_instance(members, message.author))
                    channel = client.get_channel(1295284991064018945)

                    if channel:
                        operation_task.add_done_callback( lambda task: asyncio.create_task(handle_instance_start(operation_task, message, client, channel, operation_results, 'started'))    )    
                
                elif user_message[0] == 'get_status':
                    profile = fetch_profile('valheim')
                    if profile:
                        for member in members:
                            for player in profile:
                                if member.name == player:  
                                    current_members.add(member)
                    await get_status(current_members)
                
                    # if channel:
                    #         await channel.send(f'{message.author} stopped the valheim server\n status: `{operation_results[operation.status] if operation_results[operation.status] else operation.status}`') 
                
                else:
                    await message.author.send(f"Profile {profile_name} does not exist.")
                

            
        else:
            await client.process_commands(message)


    client.run(TOKEN)