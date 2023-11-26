import discord
import responses
from discord.ext import commands
from secrets import TOKEN

members_global = []
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
        message = 'if you need more time, please enter the amount of time you require in minutes with a number in minutes preceded by `?`. Example: `?10`'
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

        if isinstance(message.channel, discord.DMChannel):
            # Message sent in DM
            user_message = message.content.strip()
            print(f'{message.author}: {user_message}')
            if(message.content.startswith(response_prefix)):
                user_message = message.content[len(response_prefix):].strip()
                if(user_message.isdigit()):
                    time = int(user_message)
                    if time > 60:
                        await message.author.send(f"we arent waiting that long dipshiit")
                        return

                    await message.author.send(f"ok, forwarding a {user_message} minute delay to everyone else")
                    message = f"{message.author} will be ready in {time} minutes"
                    await send_message(members, message)
                    return
                else:
                    await message.author.send(f"invalid input: please enter a number")


            if(message.content.startswith('*')):
                user_message = message.content[len(response_prefix):].strip()
                message = f"{message.author}: {user_message}"
                await send_message(members, message)
                return

            response = responses.handle_response(user_message)
            try: 
                await message.author.send(response)
            except discord.Forbidden:
                print("error")
            
        else:
            await client.process_commands(message)

    client.run(TOKEN)