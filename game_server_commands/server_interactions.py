import asyncio
import discord
import responses
import hmac
import requests
import hashlib
from secrets import TOKEN_LOCAL_SERVER

secret = bytes.fromhex(TOKEN_LOCAL_SERVER)


def generate_challenge():
    challenge = requests.post("https://play.jaysee.ca/generate_challenge").json()["challenge"]
    challenge_result = hmac.new(secret, bytes.fromhex(challenge), hashlib.sha256).hexdigest()

    return challenge, challenge_result

def start_server(server_name):
    challenge, challenge_result = generate_challenge()
    resp = requests.post("https://play.jaysee.ca/health", params = {"challenge": challenge, "challenge_result": challenge_result, "authority": "copium_bot"}).json()

    if resp["status"] != 'ok' or not resp["authorized"]:
        print(f"ERROR: {resp}")
        return resp
    challenge, challenge_result = generate_challenge()
    resp = requests.post(f"https://play.jaysee.ca/servers/{server_name}/start", params = {"challenge": challenge, "challenge_result": challenge_result, "authority": "copium_bot"}).json()
    return resp

def stop_server(server_name):
    challenge, challenge_result = generate_challenge()
    resp = requests.post("https://play.jaysee.ca/health", params = {"challenge": challenge, "challenge_result": challenge_result, "authority": "copium_bot"}).json()

    if resp["status"] != 'ok' or not resp["authorized"]:
        print(f"ERROR: {resp}")
        return resp

    challenge, challenge_result = generate_challenge()
    resp = requests.post(f"https://play.jaysee.ca/servers/{server_name}/stop", params = {"challenge": challenge, "challenge_result": challenge_result, "authority": "copium_bot"})
    print(resp)
    print(resp.text)
    return resp

def get_status(server_name):
    challenge, challenge_result = generate_challenge()
    resp = requests.post(f"https://play.jaysee.ca/servers/{server_name}/query", params = {"challenge": challenge, "challenge_result": challenge_result, "authority": "copium_bot"})
    return resp