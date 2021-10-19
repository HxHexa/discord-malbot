import requests
from bs4 import BeautifulSoup
import html.parser as htmlparser
import discord
from discord.ext import commands

from makeembed import makeembed

description = '''MALBot. A basic bot used to look up for infos on anime or manga on MyAnimeList.'''

bot = commands.Bot(command_prefix=commands.when_mentioned, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def anime(ctx, *, name):
    '''
    Looks up for details on an anime on MyAnimeList.
    Syntax: @bot anime <name>
    '''
    channel = ctx.message.channel
    author = ctx.message.author

    url = 'https://myanimelist.net/api/anime/search.xml?q='
    r = requests.get(url + name, auth=('maldiscbot', 'myanimelistbotbyhxhexa'))
    idfetch = BeautifulSoup(r.text, 'html.parser')
    titles_raw = idfetch.find_all('title')

    if len(titles_raw) == 0:
        id = None
    elif len(titles_raw) == 1:
        id = idfetch.id.string
    else:
        titles = []
        for i in titles_raw:
            titles.append(i.string)
        page = 1
        max_page = len(titles)// 5 + 1
        while True:
            id = ''
            all_titles = ''
            for i in range(5):
                try:
                    index = i + (page - 1) * 5
                    all_titles += '{0}. {1}\n'.format(i + 1, titles[index])
                except IndexError:
                    break
            out = '''```Page {0}/{1}\n\n{2}\nType a number to select.\nType 'n' to go to the next page, 'p' to go to the previous page, 'q' to quit.```
            '''.format(page, max_page, all_titles)
            await bot.say(out)
            while True:
                inp = await bot.wait_for_message(timeout=10, author=author, channel=channel)
                if inp == None:
                    await bot.say('`Command timed out.`')
                    id = None
                    break
                elif inp.content in '12345':
                    try:
                        r = requests.get(url + titles[int(inp.content) - 1 + (page - 1) * 5], auth=('maldiscbot', 'myanimelistbotbyhxhexa'))
                        idfetch = BeautifulSoup(r.text, 'html.parser')
                        id = idfetch.id.string
                        break
                    except IndexError:
                        await bot.say('`Invalid input.`')
                elif inp.content == 'n':
                    if page == max_page:
                        await bot.say('`No next page.`')
                    else:
                        page += 1
                        break
                elif inp.content == 'p':
                    if page == 1:
                        await bot.say('`No previous page.`')
                    else:
                        page -= 1
                        break
                elif inp.content == 'q':
                    id = None
                    break
                else:
                    await bot.say('`Invalid input.`')
            if id != '':
                break

    if id == None:
        await bot.say('`Search failed. No results found.`')
    else:
        await bot.say(embed=makeembed('anime', id))

@bot.command(pass_context=True)
async def manga(ctx, *, name):
    '''
    Looks up for details on a manga on MyAnimeList.
    Syntax: @bot manga <name>
    '''
    channel = ctx.message.channel
    author = ctx.message.author

    url = 'https://myanimelist.net/api/manga/search.xml?q='
    '''still dont know how to obfuscate this in an open-source project'''
    r = requests.get(url + name, auth=('', ''))
    idfetch = BeautifulSoup(r.text, 'html.parser')
    titles_raw = idfetch.find_all('title')

    if len(titles_raw) == 0:
        id = None
    elif len(titles_raw) == 1:
        id = idfetch.id.string
    else:
        titles = []
        for i in titles_raw:
            titles.append(i.string)
        page = 1
        max_page = len(titles)// 5 + 1
        while True:
            id = ''
            all_titles = ''
            for i in range(5):
                try:
                    index = i + (page - 1) * 5
                    all_titles += '{0}. {1}\n'.format(i + 1, titles[index])
                except IndexError:
                    break
            out = '''```Page {0}/{1}\n\n{2}\nType a number to select.\nType 'n' to go to the next page, 'p' to go to the previous page, 'q' to quit.```
            '''.format(page, max_page, all_titles)
            await bot.say(out)
            while True:
                inp = await bot.wait_for_message(timeout=10, author=author, channel=channel)
                if inp == None:
                    await bot.say('`Command timed out.`')
                    id = None
                    break
                elif inp.content in '12345':
                    try:
                        r = requests.get(url + titles[int(inp.content) - 1 + (page - 1) * 5], auth=('maldiscbot', 'myanimelistbotbyhxhexa'))
                        idfetch = BeautifulSoup(r.text, 'html.parser')
                        id = idfetch.id.string
                        break
                    except IndexError:
                        await bot.say('`Invalid input.`')
                elif inp.content == 'n':
                    if page == max_page:
                        await bot.say('`No next page.`')
                    else:
                        page += 1
                        break
                elif inp.content == 'p':
                    if page == 1:
                        await bot.say('`No previous page.`')
                    else:
                        page -= 1
                        break
                elif inp.content == 'q':
                    id = None
                    break
                else:
                    await bot.say('`Invalid input.`')
            if id != '':
                break
    if id == None:
        await bot.say('`Search failed. No results found.`')
    else:
        await bot.say(embed=makeembed('manga', id))

bot.run('')

