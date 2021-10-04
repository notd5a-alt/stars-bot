import os

import discord 
from discord.ext import commands
from dotenv import load_dotenv

import datetime
import time
import json 
import requests

load_dotenv()

DISC_TOKEN = os.environ.get('discord')
NASA_API_KEY = os.environ.get('nasa')
NASA_ICON = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/2449px-NASA_logo.svg.png'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='~', intents = intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Looking at the Stars :) Use ~commands for help."))


# HELP

@bot.command()
async def commands(ctx, arg: str = ""):
    if arg == "mars":
        embed = discord.Embed(title="Heres some help with this Command", description="Here are the parameter's needed!")
        embed.add_field(name="mars rover_name sols num !camera_type", value="This is the command format for the mars command.", inline=False)
        embed.add_field(name="rover_name", value="Choose 1 for the Curiosity Rover, 2 for the Opportunity Rover, 3 for the Spirit Rover.", inline=False)
        embed.add_field(name="sols", value="These are the martian days (integers), choose which day you want to get the mars pictures for.", inline=False)
        embed.add_field(name="num", value="Number of photos to return")
        embed.add_field(name="camera_type", value="(OPTIONAL) There are 9 total available camera types: `fhaz, rhaz, mast, chemcham, mahli, mardi, navcam, pancam, minites`.", inline=False)
        embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)
    elif arg == "":
        embed = discord.Embed(title="Here's the help you asked for :)", description="Commands you can use!")
        embed.set_author(name=ctx.author)
        embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
        embed.add_field(name="`picofday`", value="Returns the Astronomy Picture of the day, alongside a caption describing what it is!", inline=False)
        embed.add_field(name="`neos p count`", value="Near Earth Object's - Use this command supplied with the page and number of asteroids you want returned, `e.g. neos 10 10` returns 10 asteroids from the 10th page.", inline=False)
        embed.add_field(name="`earth lon lat`", value="Returns a LandSat image of earth from the longitude and latitude of your choosing. Use as follows: `e.g. earth 10 11` for longitude 10 and latitude 11.", inline=False)
        embed.add_field(name="`epic`", value="Returns the Latest Natural color image of earth using the EPIC API. Try it!", inline=False)
        embed.add_field(name="`mars r sols num !camera`", value="Returns mars rover photos from any of the 3 rovers on mars right now!", inline=False)
        embed.add_field(name="`purge x`", value="Purges x number of messages in the channel", inline=False)
        embed.add_field(name="`nasalib s`", value="Searches the Nasa Image Library for pictures of the `s` search value you put in.")
        await ctx.send(embed=embed)


# CLEAR

@bot.command()
async def purge(ctx, amount: int = 0):
    await ctx.channel.purge(limit=amount)

# APOD

@bot.command()
async def picofday(ctx): # shows the astronomy picture of the day
    # api calls
    apod_url = 'https://api.nasa.gov/planetary/apod?api_key=' + NASA_API_KEY
    response = requests.get(apod_url)
    data = response.json()
    image_url = data["hdurl"]
    description = data["explanation"]
    title = data["title"]

    # creating the embed
    embed = discord.Embed(title=title, description=description)
    embed.set_author(name="NASA", icon_url=NASA_ICON)
    embed.set_thumbnail(url=image_url)
    embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
    await ctx.send(embed=embed)


@bot.command()
async def neos(ctx, a: int = 0, b: int = 1): # near earth objects
    # takes parameter a and b which can be used to specificy the page and no. of asteroids to return, max 20 per page
    # api calls
    neows_url = 'https://api.nasa.gov/neo/rest/v1/neo/browse/?page=' + str(a) + '&size=20&api_key=' + NASA_API_KEY
    response = requests.get(neows_url)
    data = response.json()
    neo = data["near_earth_objects"]


    for x in range(0, b):
        name = neo[x]["name"]
        embed = discord.Embed(title=name, description='Has an estimated diameter of MIN: {0}, MAX: {1} and holds the ID: {2}'.format(neo[x]["estimated_diameter"]["kilometers"]["estimated_diameter_min"], neo[x]["estimated_diameter"]["kilometers"]["estimated_diameter_max"], neo[x]["id"]))
        embed.set_thumbnail(url=neo[x]["nasa_jpl_url"])
        embed.add_field(name="Designation", value=neo[x]["designation"])
        embed.add_field(name="Absolute Magnitude", value=neo[x]["absolute_magnitude_h"])
        embed.add_field(name="Orbit ID", value=neo[x]["orbital_data"]["orbit_id"])
        embed.add_field(name="Orbit Class Type", value=neo[x]["orbital_data"]["orbit_class"]["orbit_class_type"])
        embed.add_field(name="Orbit Class Range", value=neo[x]["orbital_data"]["orbit_class"]["orbit_class_range"])
        embed.add_field(name="Description", value=neo[x]["orbital_data"]["orbit_class"]["orbit_class_description"])
        embed.add_field(name="Is hazardous?", value=neo[x]["is_potentially_hazardous_asteroid"])
        embed.set_author(name="NASA", icon_url=NASA_ICON)
        embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
        await ctx.send(embed=embed)


# EARTH API

@bot.command()
async def earth(ctx, a: str, b: str): # Earth command that returns landsat data for that specific lat and long
    # a for lon and b for lat 
    earth_url = 'https://api.nasa.gov/planetary/earth/assets?lon=' + a + '&lat=' + b + '&dim=0.20&api_key=' + NASA_API_KEY
    earth_image_url = 'https://api.nasa.gov/planetary/earth/imagery?lon=' + a + '&lat=' + b + '&dim=0.20&api_key=' + NASA_API_KEY
    response = requests.get(earth_url)
    data = response.json()
    x = json.loads(response.text)
    if "msg" in x:
        await ctx.send(data["msg"])
    else:
        id = data["id"]
        date = data["date"] # TODO: Format the date to make it look better
        image = data["url"]
        embed = discord.Embed(title=id, description=date) # TODO: Format the date to make it look better
        embed.set_thumbnail(url=image)
        embed.set_author(name="NASA", icon_url=NASA_ICON)
        embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
        await ctx.send(embed=embed)
        await ctx.send(image)

# EONET

# EPIC API

@bot.command()
async def epic(ctx):
    # https://api.nasa.gov/EPIC/archive/natural/2019/05/30/png/epic_1b_20190530011359.png?api_key=DEMO_KEY for image
    # https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY call to get data for the latest image
    epic_url = 'https://api.nasa.gov/EPIC/api/natural?api_key=' + NASA_API_KEY
    image_url = 'https://api.nasa.gov/EPIC/archive/natural/2019/05/30/png/epic_1b_20190530011359.png?api_key=DEMO_KEY'
    response = requests.get(epic_url)
    data = response.json()
    x = data[0]["identifier"] # 20190530
    x = x[:4] + '/' + x[4:] # 2019/0530
    x = x[:7] + '/' + x[7:] # 2019/05/30
    date = x[:10]
    name = data[0]["image"]
    img_url = 'https://api.nasa.gov/EPIC/archive/natural/' + date + '/png/' + name + '.png?api_key=' + NASA_API_KEY
    embed = discord.Embed(title="Earth", description=data[0]["caption"])
    embed.set_thumbnail(url = img_url)
    embed.set_author(name="NASA", icon_url=NASA_ICON)
    embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
    await ctx.send(embed=embed)

# MARS ROVER PHOTOS

async def rover_name(x: int):
    rover_namee = "curiosity"
    if x == 1:
        pass
    elif x == 2:
        rover_namee = "opportunity"
    elif x == 3:
        rover_namee = "spirit"
    else:
        pass
    return rover_namee

@bot.command() # query by martian sol (days) 
async def mars(ctx, rover: int, sol: int, num: int, camera: str = ""):
    # cameras:
    # FHAZ RHAZ MAST CHEMCHAM MAHLI MARDI NAVCAM PANCAM MINITES
    rover_namee = await rover_name(rover)
    if camera == "":
        mars_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/" + rover_namee + "/photos?sol=" + str(sol) + "&api_key=" + NASA_API_KEY
    else: 
        mars_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/" + rover_namee + "/photos?sol=" + str(sol) + "&camera=" + camera + "&api_key=" + NASA_API_KEY
    response = requests.get(mars_url)
    data = response.json()
    try:
        for x in range(0, num):
            rov_name = data["photos"][x]["rover"]["name"]
            cam_name = data["photos"][x]["camera"]["full_name"]
            photo_id = data["photos"][x]["id"]
            date = data["photos"][x]["earth_date"]
            rov_status = data["photos"][x]["rover"]["status"]
            img = data["photos"][x]["img_src"]

            embed = discord.Embed(title=rov_name, description="Camera: {0}, Photo ID: {1}, Taken On: {2}, Rover Status: {3}.".format(cam_name, photo_id, date, rov_status))
            embed.set_thumbnail(url=img)
            embed.set_author(name="NASA", icon_url=NASA_ICON)
            embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
            await ctx.send(embed=embed)
    except IndexError:
        await ctx.send("Not enough photos to send :(")


# NASA IMAGE AND VIDEO LIBRARY API

@bot.command()
async def nasalib(ctx, search: str = "", num: int = 5):
    nasa_lib_url = 'https://images-api.nasa.gov/search?q=' + search.replace(" ", "%").lower() + '&media_type=image'
    try:
        response = requests.get(nasa_lib_url)
        data = response.json()
        data_collection = data["collection"]["items"]
        for x in range(0, num): 
            image = data_collection[x]["links"][0]["href"]
            title = data_collection[x]["data"][0]["title"]
            desc = data_collection[x]["data"][0]["description"]
            date_taken = data_collection[x]["data"][0]["date_created"]

            # embed
            embed = discord.Embed(title=title, description=desc)
            embed.set_author(name="NASA", icon_url=NASA_ICON)
            embed.set_footer(text="Using the NASA API. Made by notd5a-alt.")
            embed.set_thumbnail(url=image)
            embed.add_field(name="Date Taken", value=date_taken)
            await ctx.send(embed=embed)
    except discord.errors.HTTPException as err:
        await ctx.send("Error Sending Request! Error: " + str(err) + "\n\nReport this Error to https://github.com/notd5a-alt")
    except IndexError:
        await ctx.send("No Entries for that search query.")

        

bot.run(DISC_TOKEN)