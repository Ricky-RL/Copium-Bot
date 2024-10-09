
def fetch_profile(profile_name=None):
    try:
        with open('profiles/profiles.txt', 'r') as file:
            file_content = file.read().strip()
            if file_content:
                profiles = eval(file_content)
            else:
                profiles = {}
    except FileNotFoundError:
        return None

    if profile_name:
        return profiles.get(profile_name, None)
    else:
        return profiles

def add_new_profile(profile_name, temp_profile):
    try:
        with open('profiles/profiles.txt', 'r') as file:
            file_content = file.read().strip()
            if file_content:
                profiles = eval(file_content)
            else:
                profiles = {}
    except FileNotFoundError:
        print("error: file not found")
        profiles = {}

    if profile_name in profiles:
        return f"Profile {profile_name} already exists."
    else:
        profiles[profile_name] = temp_profile[profile_name]
        with open('profiles/profiles.txt', 'w') as file:
            file.write(str(profiles))
        return f"Created profile {profile_name} with members {temp_profile[profile_name]}"

def delete_profile(profile_name):
    try:
        with open('profiles/profiles.txt', 'r') as file:
            file_content = file.read().strip()
            if file_content:
                profiles = eval(file_content)
                if profile_name in profiles:
                    del profiles[profile_name]
                    with open('profiles/profiles.txt', 'w') as file:
                        file.write(str(profiles))
                    return f"Deleted profile {profile_name}."
                else:
                    return f"Profile {profile_name} does not exist."
            else:
                return f"No profiles found."
    except FileNotFoundError:
        return f"Error file file not found."