import requests
import json
import valve.source.a2s
import discord
from discord.ext import commands, tasks
import asyncio
bot = commands.Bot(command_prefix=';', description="Ojo de a")

@bot.command()
async def getservers(ctx, server):
    embed = discord.Embed(title="Search results", color=0xff3300)
    serv = getservers(server)
    print(serv)
    for a in range(len(serv[0])):
        sv = str("""```css\n{sv}```""".format(sv=serv[1][a]))
        embed.add_field(name=serv[0][a], value=sv, inline=False)
    em = await ctx.send(embed=embed)


def svinfoeasystyle(id, af=''):
    embed = discord.Embed(title="Server info", color=0xff3300)
    serv = getserverinfo(id)
    embed.add_field(name="[IP]", value=str("""```css\n[NAME] {name}\n[IP] {sv}\n[PLAYER COUNT] {count}\n[STATUS] {status}```""".format(sv=serv['ip'],name=serv['name'], count=serv['players'], status=serv['status'])), inline=False)
    po = ""
    for b in serv['playerlist']:
        po = po+"""[*] {sv}\n""".format(sv=b)
    embed.add_field(name="**PLAYERS**", value=po, inline=False)
    if af:
        embed.add_field(name='**Segundos restantes: **', value=af, inline=False)
    return embed


def svinfoembed(id, af=''):
    embed = discord.Embed(title="Server info", color=0xff3300)
    serv = getserverinfo(id)
    embed.add_field(name="**[NAME]**",value="**"+serv['name']+"**", inline=False)
    embed.add_field(name="[IP]", value=str("""```css\n[{sv}]```""".format(sv=serv['ip'])), inline=False)
    embed.add_field(name="[STATUS]", value="**"+serv['status']+"**", inline=False)
    embed.add_field(name="[PLAYER COUNT]", value="**"+str(serv['players'])+"**", inline=False)
    embed.add_field(name="[MAP]", value=serv['map'], inline=False)
    for b in serv['playerlist']:
        embed.add_field(name="[*]", value=str("""```css\n[{sv}]```""".format(sv=b)), inline=False)
    if af:
        embed.add_field(name='**Segundos restantes: **', value=af, inline=False)
    return embed


@bot.command()
async def ww(ctx, id, seconds, style='0'):
    if style != '0':
        embed = svinfoeasystyle(id)
    else:
        embed = svinfoembed(id)
    em = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    for a in range(0,int(seconds)):
        if style != '0':
            embed = svinfoeasystyle(id, str(int(seconds)-a))
        else:
            embed = svinfoembed(id, str(int(seconds) - a))
        await asyncio.sleep(0.7)
        await em.edit(embed=embed)
    await em.delete()

def getserverinfo(id):
    pet = json.loads(requests.get('https://api.battlemetrics.com/servers/' + id).text)['data']
    serverDetails = (pet['attributes']['ip'], pet['attributes']['portQuery'])
    server = valve.source.a2s.ServerQuerier(serverDetails, timeout=3)
    players = ""
    ap = ""
    server.info()
    try:
        players = server.players()
        info = server.info()
    except Exception as e:
        print(str(e))
    print(players)
    for player in players["players"]:
        ap = ap + "{name}\n".format(**player)
    ap = [line for line in ap.split('\n') if line.strip() != ""]
    data = {
        'name': pet['attributes']['name'],
        'ip': pet['attributes']['ip'] + ':' + str(pet['attributes']['portQuery']),
        'status': pet['attributes']['status'],
        'players': pet['attributes']['players'],
        'playerlist': ap,
        'map': info['map']
    }
    return data

def getservers(server):
    data = json.loads(
        requests.get('https://api.battlemetrics.com/servers?filter[game]=ark&filter[search]=' + server).text)
    data1 = list()
    data2 = list()
    for a in data['data']:
        data1.append(a['attributes']['id'])
        data2.append(a['attributes']['name'])
    return [data1, data2]

bot.run("")