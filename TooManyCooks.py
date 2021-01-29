import datetime
import asyncio
from discord.ext import commands
import discord
import Moodle as mood
import random
import requests
from youtube_dl import YoutubeDL
import os
import giphy_client
from giphy_client.rest import ApiException
import csv
from discord import FFmpegPCMAudio
import re


TOKEN = os.environ.get("TOKEN")
courses = {'qazi': 'CMPT 364 Cloud Computing and Virtualization', 'tina': 'CMPT 438 Algorithms', 'arafat': 'CMPT 456 Software Engineering'}
version = 'v1.2'
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'))
giphy_token = os.environ.get("G-TOKEN")
api_instance = giphy_client.DefaultApi()

players ={}


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.total = 1.00

    @commands.command(pass_context=True)
    async def moodle(self, ctx, message: str):
        if message in courses.keys():
            instance = mood.Moodle()
            courseData = instance.findCourse(message)
            titles, hrefs = instance.parsingCourseData(courseData)
            embed = discord.Embed()
            embed.set_author(name='Manhattan College Moodle LMS')  # title of course
            embed.title = courses[message]  # name of link to course page
            embed.url = 'https://lms.manhattan.edu/my/'  # actual link to course
            embed.description = version  # description
            embed.set_thumbnail(url=ctx.author.avatar_url)  # image top right small
            embed.colour = ctx.author.colour  # left line color
            count = 0
            for title in titles:
                embed.add_field(name=title, value=hrefs[count], inline=False)
                count += 1
            embed.set_footer(text='In Development')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Command not Found!")

    @commands.command(pass_context=True)
    async def hw(self, ctx, message: str):
        if message in courses.keys():
            instance = mood.Moodle()
            courseData = instance.findCourse(message)
            assignments = instance.assignments(courseData)
            embed = discord.Embed()
            embed.set_author(name='Manhattan College Moodle LMS')  # title of course
            embed.title = courses[message]  # name of link to course page
            embed.url = 'https://lms.manhattan.edu/my/'  # actual link to course
            embed.description = version  # description
            embed.set_thumbnail(url=ctx.author.avatar_url)  # image top right small
            embed.colour = ctx.author.colour  # left line color
            for hw in assignments:
                ddobj = datetime.datetime.strptime(assignments[hw][0], '%A, %B %d, %Y, %I:%M %p')
                if (datetime.datetime.now() < ddobj):
                    embed.add_field(name='{} --- **ACTIVE**'.format(hw),
                                    value='{}\nDue Date: {}'.format(assignments[hw][1], assignments[hw][0]), inline=False)
                else:
                    embed.add_field(name='{} --- **IN-ACTIVE**'.format(hw),
                                    value='{}\nDue Date: {}'.format(assignments[hw][1], assignments[hw][0]), inline=False)
            embed.set_footer(text='In Development')
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def sanjay(self, ctx):
        author = ctx.message.author.id
        a = '<@{0}>'.format(author)
        msg = ', did you know Sanjay is god?'
        await ctx.send(a + msg)

    @commands.command(pass_context=True)
    async def eric(self, ctx):
        a = ['LIGMA', 'SUGMA', 'SUGONDESE', 'SUKAPONMA', 'SLUrPONDESE', 'FUGMA', 'BOFA', 'EETMA']
        lol = random.randint(0, 7)
        ericid = '<@104348613735358464>'
        msg = ' has been infected with '
        await ctx.send(ericid + msg + a[lol])

    @commands.command(pass_context=True)
    async def natalie(self, ctx):
        natid = '<@534788195964157952>'
        self.total += 0.01
        msg = ' has been given 1 cent. Her total balance is '
        await ctx.send(natid + msg + "{:.2f}".format(self.total))

    @commands.command(pass_context=True)
    async def mike(self, ctx):
        mikeid = 298282227047989262
        print(ctx.author.id)
        if ctx.author.id == mikeid:
            await ctx.send("Mike is here!")
        else:
            await ctx.send("You are An Impostor")

    @commands.command(pass_context=True)
    async def jeremy(self, ctx):
        await ctx.send("Jeremy use to eat chapstick in Kindergarten")

    @commands.command(pass_context=True)
    async def emelia(self, ctx):
        await ctx.send("Doc Martens is not a personality trait")

    @commands.command(pass_context=True)
    async def spam(self, ctx):
        striy = ctx.message.content
        strigy = striy[6:]
        lol = random.randint(4, 8)
        for x in range(0,lol):
            await ctx.send(strigy)

    @commands.command(pass_context=True)
    async def gif(self, ctx):
        stry = ctx.message.content
        strgy = stry[5:]
        gif = await search_gifs(strgy)
        with open('D:\\Downloads\\buss.gif', 'wb') as f:
            f.write(requests.get('https://media.giphy.com/media/' + gif + '/giphy.gif').content)
        await ctx.send(file=discord.File('D:\\Downloads\\buss.gif'))

    @commands.command(pass_context=True)
    async def vote(self, ctx, message: str):
        stry = message.capitalize()
        votedict = {}
        with open('voting.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                votedict[row[0]] = row[1]
        with open('voting.csv', mode='w', newline='') as vwf:
            writer = csv.writer(vwf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if stry in votedict.keys():
                temp = votedict[stry]
                count = int(temp)
                count += 1
                votedict[stry] = str(count)
            else:
                votedict[stry] = '1'
            for line in votedict.keys():
                writer.writerow([line, votedict[line]])
        await ctx.send("Vote Submitted")

    @commands.command(pass_context=True)
    async def result(self, ctx):
        myid = 235185011941310468
        print(ctx.author.id)
        if ctx.author.id == myid:
            votedict = {}
            with open('voting.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    votedict[row[0]] = row[1]
            await ctx.send(str(votedict))
        else:
            await ctx.send("Results will be revealed on Election Day!")

    @commands.command(pass_context=True)
    async def loading(self, ctx):
        y = 1
        dot = ' . '
        msg = await ctx.send('Loading')
        while y <= 2:
            con = 'Loading'
            x = 1
            while x <= 10:
                await asyncio.sleep(0.5)
                await msg.edit(content=con)
                con += dot
                x += 1
            y += 1

    @commands.command(pass_context=True)
    async def time(self, ctx):
        timestr = ctx.message.content
        time = int(timestr[6:])
        count = time
        msg = await ctx.send(str(time))
        while count >= 0:
            count -= 1
            await asyncio.sleep(1)
            await msg.edit(content=str(count))


    @commands.command(pass_context=True)
    async def embed(self, ctx):
        embed = discord.Embed()
        embed.set_author(name='School') #title of course
        embed.title = 'KSFSKDJSKFH' #name of link to course page
        embed.url = 'https://www.google.com/' #actual link to course
        embed.description = 'description' #description
        embed.set_thumbnail(url='https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg') #image top right small
        embed.colour = 0x046a38 #left line color

        embed.add_field(name='Syllabus', value='[test](https://www.google.com/)')
        
        
        embed.set_footer(text='Challenge Released')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def yt(self, ctx):
        emeliaid = 442044853728051200
        print(ctx.author.id)
        if ctx.author.id != emeliaid:
            striy = ctx.message.content
            strgy = striy[4:]
            url = self.getYTurl(strgy)
            await ctx.send(url)
        else:
            await ctx.send("Emelia it is a NO for you!")


    def getYTurl(self, ctx):
        y = 0
        output = re.sub(' ', '+', ctx)
        session = requests.Session()
        api = os.environ.get("Y-API")
        maxResults = "20"

        query = output
        print('Query:', query)
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet" \
              "&q=" + query + \
              "&key=" + api + \
              '&maxResults=' + maxResults
        reqJson = session.get(url).json()
        # numResults = int(reqJson['pageInfo']['resultsPerPage'])
        while reqJson['items'][y]['id']['kind'] != "youtube#video" and y < int(maxResults):
            y += 1
        if reqJson['items'][y]['id']['kind'] == "youtube#video":
            video = "https://www.youtube.com/watch?v=" + reqJson['items'][y]['id']['videoId']
            return str(video)
        else:
            return None

    @commands.command(pass_context=True)
    async def play(self, ctx):
        striy = ctx.message.content
        strgy = striy[6:]
        url = self.getYTurl(strgy)
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        x = 10
        author = ctx.message.author
        if author.voice is None:
            await ctx.send("Join a Voice Channel")
            while x > 0 and author.voice is None:
                await asyncio.sleep(1)
                x -= 1
        if author.voice is None:
            await ctx.send(
                "You have somehow failed a simple task of joining a voice channel within 10 seconds. Very Sad.")
            return
        voice = await author.voice.channel.connect()
        print(voice)
        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
        else:
            await ctx.send("Already playing song")
            return
        msg = "Should Be Playing"
        await ctx.send(msg)
        mem = author.voice.channel.members
        mount = 0
        print(mem)
        while voice.is_playing():
            await asyncio.sleep(3)
        if not (voice.is_playing()):
            await ctx.voice_client.disconnect()
            print("Bot left the voice channel")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=10, rating='r')
        lst = list(response.data)
        gif = random.choices(lst)

        return gif[0].id

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


bot.add_cog(Main(bot))
bot.run(TOKEN)

