 ![image](https://github.com/user-attachments/assets/3bbe30c6-b178-45c2-83a7-2316c17a330a)
 # Copium Bot
a bot that helps invite people to play video games 

**PLAY GAMES**
- `!play [profile_name]`: Sends a request to play the profile-specific game to its members.

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
