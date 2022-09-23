from datetime import datetime
from io import BytesIO
import requests
import discord
from PIL import Image
from bot_data import *

def user_agent():
    headers = {
        'User-Agent': "sp3-bot Discord Bot (Github: zian999)".encode()
    }
    return headers

def get_schedule(p1, p2):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{p1}/{p2}", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        return data['results']
    else:
        data = None
        return data

def handle(entry):
    st = datetime.strptime(entry['start_time'], "%Y-%m-%dT%H:%M:%S%z")
    et = datetime.strptime(entry['end_time'], "%Y-%m-%dT%H:%M:%S%z")
    if 'weapons' in entry:
        weapons = [w['name'] for w in entry['weapons']]
        stage = entry['stage']['name']
        return [[st, et], stage, weapons]
    if 'stages' in entry:
        rule_name = entry['rule']['name']
        stages = [s['name'] for s in entry['stages']]
        return [[st, et], rule_name, stages]

def timediff(earlier_time, later_time):
    s = str(later_time - earlier_time).split(':')
    if s[0].find(' days, ') > 0:
        dayhour = s[0].split(' days, ')
        s.insert(0, dayhour[0])
        s[1] = dayhour[1]
    elif s[0].find(' day, ') > 0:
        dayhour = s[0].split(' day, ')
        s.insert(0, dayhour[0])
        s[1] = dayhour[1]
    else:
        s.insert(0, '0')
    s[3] = str(round(float(s[3]), 1))
    return s

def embed_content(entry):
    data = handle(entry)
    t = data[0]
    if datetime.now(tz = t[0].tzinfo) > t[0]:
        tdelta = timediff(datetime.now(tz = t[1].tzinfo), t[1])
        embed = discord.Embed(
            title = f"Ends in {tdelta[0]} days, {tdelta[1]} hours, {tdelta[2]} mins."
        )
    else:
        tdelta = timediff(datetime.now(tz = t[0].tzinfo), t[0])
        embed = discord.Embed(
            title = f"Starts in {tdelta[0]} days, {tdelta[1]} hours, {tdelta[2]} mins."
        )
    if 'stages' in entry:
        stage_id1 = stage_ids[data[2][0]]
        stage_id2 = stage_ids[data[2][1]]
        embed.add_field(
            name = "~ RULE ~",
            value = rule_CN_names[rule_ids[data[1]]],
            inline = False
        )
        embed.add_field(
            name = "~ STAGES ~",
            value = stage_CN_names[stage_id1] + '\n' + stage_CN_names[stage_id2],
            inline = False
        )
        file = discord.File(embed_stage_image(stage_id1, stage_id2), filename = "o.png")
        embed.set_image(url="attachment://o.png")
        return [file, embed]
    if 'weapons' in entry:
        weapon_id1 = weapon_ids[data[2][0]]
        weapon_id2 = weapon_ids[data[2][1]]
        weapon_id3 = weapon_ids[data[2][2]]
        weapon_id4 = weapon_ids[data[2][3]]
        stage_id = stage_ids[data[1]]
        embed.add_field(
            name = "~ WEAPONS ~",
            value = (
                weapon_CN_names[weapon_id1] + '\n'
                + weapon_CN_names[weapon_id2] + '\n'
                + weapon_CN_names[weapon_id3] + '\n'
                + weapon_CN_names[weapon_id4]
            ),
            inline = False
        )
        embed.add_field(
            name = "~ STAGE ~",
            value = stage_CN_names[stage_id],
            inline = False
        )
        embed.set_image(url=stage_images[stage_id])
        return embed

def create_image(url1, url2):
    img1 = read_image(url1)
    img2 = read_image(url2)
    img = merge_image(img1, img2)
    return img

def read_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def merge_image(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))
    return im

def embed_stage_image(id1, id2):
    im = create_image(stage_images[id1], stage_images[id2])
    b = BytesIO()
    im.save(b, "PNG")
    b.seek(0)
    return b

