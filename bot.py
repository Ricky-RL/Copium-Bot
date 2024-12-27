import discord
import json
from discord.ext import commands
from secrets import TOKEN, PROJECT, ZONE, INSTANCE_NAME, TOKEN_LOCAL_SERVER
from datetime import datetime, timedelta
from data import allchamp, people, help_str, people_test
import random   
from google.cloud import compute_v1
from google.oauth2 import service_account
from profiles.profiles_db import add_new_profile, fetch_profile, delete_profile, add_new_profile_test
from game_server_commands.server_interactions import start_server, stop_server, get_status

SERVICE_ACCOUNT_FILE = './secrets_gcp.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)

members_global= []
response_list = {}
current_members = set()
global_ctx = None
log_channel = None
server_channel = None
operation_results = {2104194: 'DONE', 35394935: 'PENDING', 121282975: 'RUNNING'}
async def send_message(members, message):
        for member in members:
            await member.send(message)

def get_temp_member_profile(members, people):
    temp_members = []
    for member in members:
        if member.name in people:
            temp_members.append(member)
    
    return temp_members

# data_file = 'profiles/profiles.json'

# # Save member data to a file
# async def save_member_data(members):
#     members_data = {member.name: member.id for member in members if not member.bot}
#     with open(data_file, 'w') as file:
#         json.dump(members_data, file)


# # Fetch member data and send a message
# async def fetch_and_message_member(ctx, member_name):

#     with open(data_file, 'r') as file:
#         members_data = json.load(file)
#         await ctx.send(f"member_data: {members_data}")

#     member_id = members_data.get(member_name)
#     if not member_id:
#         await ctx.send(f"No member found with the name {member_name}.")
#         return

#     member = ctx.guild.get_member(member_id)
#     if member:
#         try:
#             await member.send("Hello! This is a message sent via the bot.")
#             await ctx.send(f"Message sent to {member_name}.")
#         except discord.Forbidden:
#             await ctx.send(f"Unable to send a message to {member_name}. They might have DMs disabled.")
#     else:
#         await ctx.send(f"Member {member_name} is not in this guild.")

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
                    message = f'{member.mention} begin testing'
                    await send_message([member], message)
                    break
            
            if member.name in people: # want to create a smaller list of members
                temp_members.append(member)

        members = temp_members
        global global_ctx
        global_ctx = ctx

        global log_channel
        log_channel = client.get_channel(1322339152632610876)

        global server_channel
        server_channel = channel = client.get_channel(1295284991064018945)

        # await add_new_profile_test('hi', members)      

    @client.event
    async def on_message(message):
        global current_members
        channel = client.get_channel(1322339152632610876)

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
            await log_channel.send(f"{message.author}: {user_message}")

            if(message.content.startswith(response_prefix)):
                user_message = message.content[len(response_prefix):].strip()

                unformatted_current_time = datetime.now()
                current_time = unformatted_current_time.strftime("%I:%M %p")
                if (user_message == 'test'):
                    print('test')
                    await log_channel.send('test')

                if(user_message.isdigit()):
                    time = int(user_message)
                    if time == 69:
                        await message.author.send(f"nice")
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
                

                # following fns require param so we must split input string
                user_message = user_message.split(' ')
                if user_message[0] == 'nudge':
                    # no tags found in input
                    if len(user_message) == 1:
                        await message.author.send(f'Error: No tags found')

                    persons = user_message[1:]
                    # invalid tag
                    for person in persons:
                        if person not in people: 
                            await message.author.send(f'{person} is an invalid tag. Valid tags can be found here: {people}')
                            return
                
                    for person in persons:
                        for member in members:
                            if person == member.name:
                                await send_message([member], f'{member.mention} HURRYYYYYYY!!!!')
                                await message.author.send(f'nudge successfully sent to {member.name}')   

                # await message.author.send(f"invalid input. Please enter a valid command")

            if(message.content.startswith('*')):
                user_message = message.content[len(response_prefix):].strip().split(' ')

                profiles_dict =  fetch_profile()
                profile_names = profiles_dict.keys()
                if user_message[0] in profile_names:
                    temp_members = get_temp_member_profile(members,  profiles_dict[user_message[0]])
                    await send_message(temp_members, f"({user_message[0]}) {message.author}: {' '.join(user_message[1:])}")
                else:
                    message = f"(global) {message.author}: {' '.join(user_message)}"
                    for member in members:
                        if member.name in people:
                            await member.send(message)
                # await send_message(members, message)
                return
            
            if message.content.startswith('!'):
                user_message = message.content[len(response_prefix):].strip().split(' ')
                print(user_message)
                # code for when I want to test stuff
                if user_message[0] == 'test':
                    print(fetch_profile())
                    return
                    
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
                                temp_profile[profile_name].append(player)
                                await message.author.send(f"adding {player} to {profile_name}")

                    result_message = add_new_profile(profile_name, temp_profile)
                    for member in members:
                        if member.name in temp_profile:
                            await member.send(f"you have been added to {profile_name} by {message.author.name}" )
                            
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
                            if member.name != message.author.name:
                                await member.send(f'{member.mention}\n{message.author.name} is asking you to play {user_message[1]} bro. See `?help` for valid commands')
                elif user_message[0] == 'start_server':
                    if len(user_message) != 2:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 2 arguments `!start_server (profile_name)`. Run `!get_profiles` to see the list of valid profiles. Received {len(user_message)}")
                        return
                    
                    profile = fetch_profile(user_message[1])
                    if not profile:
                        await message.author.send(f"invalid profile. Profile {profile} was not found in the list of valid profiles `!get_profiles`.")

                    for member in members:
                        for player in profile:
                            if member.name == player:
                                current_members.add(member)

                    resp = start_server(user_message[1])
                                            
                    await send_message(current_members, f"{message.author} is starting server {profile}. \n Connect to server at `play.jaysee.ca`")
                    await server_channel.send(f"Server {profile} started by {message.author}. Server status: {resp}")
                    
                elif user_message[0] == 'stop_server':
                    if len(user_message) != 2:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 2 arguments `!stop_server (profile_name)`. Run `!get_profiles` to see the list of valid profiles. Received {len(user_message)}")
                        return
                    
                    profile = fetch_profile(user_message[1])
                    if not profile:
                        await message.author.send(f"invalid profile. Profile {profile} was not found in the list of valid profiles `!get_profiles`.")

                    resp = stop_server(user_message[1])
                    print(resp)
                    
                    await message.author.send(f"{profile} Server Stopped. Status {resp.text}")

                elif user_message[0] == 'get_status':
                    if len(user_message) != 2:
                        await message.author.send(f"invalid input. Please enter a valid command expecting 2 arguments `!get_status (profile_name)`. Run `!get_profiles` to see the list of valid profiles. Received {len(user_message)}")
                        return
                    
                    profile = fetch_profile(user_message[1])
                    if not profile:
                        await message.author.send(f"invalid profile. Profile {profile} was not found in the list of valid profiles `!get_profiles`.")

                    resp = get_status(user_message[1])
                    if resp.status_code == 200:
                        await message.author.send(f"{profile} Server status: {resp.text}")
                    else:
                        await message.author.send(f"ERROR Response code: {resp.status_code}. Response body: {resp.text}")    
                else:
                    await message.author.send(f"Invalid Command")
                

            
        else:
            await client.process_commands(message)


    client.run(TOKEN)