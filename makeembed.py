import discord
import requests
import json

def dicttool(details, category):
    '''
    Deals with categories with varying number of elements, like genres or studios.
    Input:
        details: dict. Dictionary given from Jikai API
        category: string. Category to handle.
    Output:
        string.
    '''
    out = ''
    if type(details[category][0]) != list:
        out = details[category][1]
    else:
        out = ', '.join([details[category][a][1] for a in range(len(details[category]))])
    return out

def makeembed(type, id):
    '''
    Creates an embed using the given details.
    Input: 
        id: ID of the series on MyAnimeList
        type: string. Either 'anime' or 'manga'
    Output: 
        embed.
    '''
    
    url = 'https://jikan.me/api/v1.1/{}/{}'.format(type, id)
    r = requests.get(url)
    details = json.loads(r.text)

    try:
        description = '**{}**'.format(details['title-english'].replace('amp;', ''))
    except KeyError:
        description = '**{}**'.format(details['title'].replace('amp;', ''))

    embed = discord.Embed(title = details['title'].replace('amp;', ''), description = description, url = details['link-canonical'], colour=0x2E51A2)
    embed.set_footer(text='MALBot made by /u/HexaHx using Jikan API.', icon_url='http://i.imgur.com/vEy5Zaq.png')
    embed.set_thumbnail(url=details['image'])
    
    genre = dicttool(details, 'genre')

    if type ==  'anime':

        studio = dicttool(details, 'studio')

        if details['type'] == 'TV':
            anime_info = '''
            **Type:** {0}\n**Episodes:** {1}\n**Status:** {2}\n**Aired:** {3}\n**Season:** {4}\n**Studios:** {5}\n**Source:** {6}\n**Genres:** {7}\n**Duration:** {8}\n**Rating:** {9}
            '''.format(details['type'], details['episodes'], details['status'], details['aired'],
                       details['premiered'], studio.replace('</a>  </div>', ''), details['source'],
                       genre, details['duration'], details['rating'].replace('amp;', ''))
        else:
            anime_info = '''
            **Type:** {0}\n**Episodes:** {1}\n**Status:** {2}\n**Aired:** {3}\n**Studios:** {4}\n**Source:** {5}\n**Genres:** {6}\n**Duration:** {7}\n**Rating:** {8}
            '''.format(details['type'], details['episodes'], details['status'], details['aired'],
                       studio.replace('</a>  </div>', ''), details['source'], genre,
                       details['duration'], details['rating'].replace('amp;', ''))
        
        embed.add_field(name='__**Information**__', value=anime_info, inline=False)


    elif type == 'manga':
        author = '; '.join([details['author'][a]['name'] for a in range(len(details['author']))])

        if len(details['serialization']) == 0:
            serialization = 'None'
        else:
            serialization = details['serialization'][0]

        manga_info = '''
        **Type:** {0}\n**Volumes:** {1}\n**Chapters:** {2}\n**Status:** {3}\n**Published:** {4}\n**Genre:** {5}\n**Author:** {6}\n**Serialization:** {7}
        '''.format(details['type'], details['volumes'], details['chapters'], details['status'],
                   details['published'], genre, author, serialization)
        
        embed.add_field(name='__**Information**__', value=manga_info, inline=False)


    else:
        print('Bad input.')
        return None

    try:
        statistics = '''
        **Score:** {0} (scored by {1} users)\n**Ranked:** #{2}\n**Popularity:** #{3}\n**Members:** {4}
        '''.format(details['score'][0], details['score'][1], details['ranked'], details['popularity'], details['members'])
    except KeyError:
        statistics = '''
        **Score:** {0} (scored by {1} users)\n**Ranked:** #{2}\n**Popularity:** #{3}\n**Members:** {4}
        '''.format(details['score'][0], details['score'][1], 'None', details['popularity'], details['members'])	

    embed.add_field(name='__**Statistics**__', value=statistics, inline=False)
    
    return embed