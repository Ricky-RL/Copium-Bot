allchamp = ["Aatrox","Ahri","Akali","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion Sol","Azir","Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","ChoGath","Corki","Darius","Diana","Dr. Mundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Hecarim","Heimerdinger","Illaoi","Irelia","Ivern","Janna","Jarvan IV","Jax","Jayce","Jhin","Jinx","KaiSa","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","KhaZix","Kindred","Kled","KogMaw","LeBlanc","Lee Sin","Leona","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Master Yi","Miss Fortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus","Neeko","Nidalee","Nocturne","Nunu and Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn","Rakan","Rammus","RekSai","Renekton","Rengar","Riven","Rumble","Ryze","Sejuani","Senna","Sett","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra","Tahm Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted Fate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar","VelKoz","Vi","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin Zhao","Yasuo","Yorick","Yuumi","Zac","Zed","Ziggs","Zilean","Zoe","Zyra"]
people = ["iplaygam", "epickc123", "azpochita", "warscout101", "jaycsee", "iplaygamv2", "fyukka"]
people_test = ['iplaygam', 'iplaygamv2']
help_str_1 = """
**PLAY GAMES**
- `!play [profile_name]`: Sends a request to play the profile-specific game to its members.
- `!vote [profile_1] [profile_2] [duration (minutes)]`: Starts a vote between two profiles. Duration determines the length of the vote. Copium bot will automatically handle tiebreakers. Respond to vote with `?A` `?B` `?random` `?abstain`.

**PROFILE MANAGEMENT COMMANDS**
- `!get_status`: Returns the status of the server.
- `!get_profiles`: Prints out a list of all profiles.
- `!create_profile [profile_name] [member_name1] [member_name2] ...`: Adds all members to the profile. 
   - Example: `!create_profile hearts of iron iv iplaygam iplaygamv2`
- `!delete_profile [profile_name]`: Deletes the profile with the given name.

**ANNOY PEOPLE COMMANDS**
- `?nudge [discord_tag_1] [discord_tag_2] ...`: nudges the player(s) specified in the tag to hop on. Requires at least one tag in input. Run `?tags` to see valid player tags
- `?remind`: Send a reminder to all players that have yet to respond.

**RESPONSE COMMANDS**
- `?y`: Confirm that you are playing tonight.
- `?n`: Confirm that you are not playing tonight.
- `?time in minute(s)`: Request a delay of the specified length.
   - Example: `?10`
- `?clear`: Clears the list of players that are coming to play.
- `?A`: Vote for profile A
- `?B`: Vote for profile B
"""
help_str_2 = """
** Communication Commands**
- `*{OPTIONAL: profile_name} any text`: Send a message to all users.
    - Example: `*overwatch test` sends the message `test` to all users in the overwatch profile
    - Example: `*test` sends the message `test` to all users

**Server Management Commands**
- `!start_server {profile_name}`: Start up specific server to profile.
   - **Note:** *MAKE SURE TO SHUT DOWN THE SERVER AFTERWARDS.*
- `!stop_server {profiile_name`: Stop specific server to profle.
- `!get_status {profile_name}`: Get information on specific server to profile.

**MISCELLANEOUS COMMANDS**
- `?tags`: See the list of all valid Discord tags.
- `?recommend`: Proprietary trained deep neural net model custom GPT ML algorithm that recommends champions based on projected player performance and meta shifts.
- `?list`: View the people who have already responded.
- `!get_vote`: Obtains the current vote

"""
