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
    return [st, et]

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
    t = handle(entry)
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
    if ('is_tricolor' in entry) and entry['is_tricolor']:
        stage_id1 = stage_ids[entry['stages'][0]['name']]
        stage_id2 = stage_ids[entry['stages'][1]['name']]
        tc_stage_id = stage_ids[entry['tricolor_stage']]
        stage_url1 = entry['stages'][0]['image']
        stage_url2 = entry['stages'][1]['image']
        embed.add_field(
            name = "~ RULE ~",
            value = rule_CN_names[rule_ids[entry['rule']['name']]],
            inline = False
        )
        embed.add_field(
            name = "~ STAGES ~",
            value = stage_CN_names[stage_id1] + '\n' + stage_CN_names[stage_id2],
            inline = False
        )
        embed.add_field(
            name = "~ TRICOLOR STAGE ~",
            value = stage_CN_names[tc_stage_id],
            inline = False
        )
        file = discord.File(embed_tc_stage_image(stage_url1, stage_url2), filename = "o.png")
        embed.set_image(url="attachment://o.png")
    else:
        stage_id1 = stage_ids[entry['stages'][0]['name']]
        stage_id2 = stage_ids[entry['stages'][1]['name']]
        embed.add_field(
            name = "~ RULE ~",
            value = rule_CN_names[rule_ids[entry['rule']['name']]],
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

def embed_content_coop(entry):
    t = handle(entry)
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
    weapon_id1 = weapon_ids[entry['weapons'][0]['name']]
    weapon_id2 = weapon_ids[entry['weapons'][1]['name']]
    weapon_id3 = weapon_ids[entry['weapons'][2]['name']]
    weapon_id4 = weapon_ids[entry['weapons'][3]['name']]
    stage_id = stage_ids[entry['stage']['name']]
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
    embed.set_image(url=entry['stage']['image'])
    return embed

def create_image(url1, url2):
    img1 = read_image(url1)
    img2 = read_image(url2)
    img = merge_image(img1, img2)
    return img

def create_tc_image(url1, url2, url3):
    img1 = read_image(url1)
    img2 = read_image(url2)
    img3 = read_image(url3)
    img = merge_image(merge_image(img1, img2), img3)
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

def embed_tc_stage_image(id1, id2, tcid):
    im = create_tc_image(stage_images[id1], stage_images[id2], stage_images[tcid])
    b = BytesIO()
    im.save(b, "PNG")
    b.seek(0)
    return b