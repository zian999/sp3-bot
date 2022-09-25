from datetime import datetime
import os
from io import BytesIO
from socket import getnameinfo
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
            title = f"Ends in {tdelta[0]} day(s), {tdelta[1]} hour(s), {tdelta[2]} min(s)."
        )
    else:
        tdelta = timediff(datetime.now(tz = t[0].tzinfo), t[0])
        embed = discord.Embed(
            title = f"Starts in {tdelta[0]} day(s), {tdelta[1]} hour(s), {tdelta[2]} min(s)."
        )
    if ('is_tricolor' in entry) and entry['is_tricolor']:
        rule_id = rule_ids[entry['rule']['name']]
        stage_id1 = stage_ids[entry['stages'][0]['name']]
        stage_id2 = stage_ids[entry['stages'][1]['name']]
        tc_stage_id = stage_ids[entry['tricolor_stage']['name']]
        stage_url1 = entry['stages'][0]['image']
        stage_url2 = entry['stages'][1]['image']
        tc_stage_url = entry['tricolor_stage']['image']
        embed.add_field(
            name = "~ RULE ~",
            value = get_name("rule", rule_id),
            inline = False
        )
        embed.add_field(
            name = "~ STAGES ~",
            value = get_name("stage", stage_id1) + '\n' + get_name("stage", stage_id2),
            inline = False
        )
        embed.add_field(
            name = "~ TRICOLOR STAGE ~",
            value = get_name("stage", tc_stage_id),
            inline = False
        )
        file = discord.File(embed_tc_stage_image(stage_url1, stage_url2, tc_stage_url), filename = "o.png")
        embed.set_image(url="attachment://o.png")
    else:
        rule_id = rule_ids[entry['rule']['name']]
        stage_id1 = stage_ids[entry['stages'][0]['name']]
        stage_id2 = stage_ids[entry['stages'][1]['name']]
        stage_url1 = entry['stages'][0]['image']
        stage_url2 = entry['stages'][1]['image']
        embed.add_field(
            name = "~ RULE ~",
            value = get_name("rule", rule_id),
            inline = False
        )
        embed.add_field(
            name = "~ STAGES ~",
            value = get_name("stage", stage_id1) + '\n' + get_name("stage", stage_id2),
            inline = False
        )
        file = discord.File(embed_stage_image(stage_url1, stage_url2), filename = "o.png")
        embed.set_image(url="attachment://o.png")
    return [file, embed]

def embed_content_coop(entry):
    t = handle(entry)
    if datetime.now(tz = t[0].tzinfo) > t[0]:
        tdelta = timediff(datetime.now(tz = t[1].tzinfo), t[1])
        embed = discord.Embed(
            title = f"Ends in {tdelta[0]} day(s), {tdelta[1]} hour(s), {tdelta[2]} min(s)."
        )
    else:
        tdelta = timediff(datetime.now(tz = t[0].tzinfo), t[0])
        embed = discord.Embed(
            title = f"Starts in {tdelta[0]} day(s), {tdelta[1]} hour(s), {tdelta[2]} min(s)."
        )
    weapon_id1 = weapon_ids[entry['weapons'][0]['name']]
    weapon_id2 = weapon_ids[entry['weapons'][1]['name']]
    weapon_id3 = weapon_ids[entry['weapons'][2]['name']]
    weapon_id4 = weapon_ids[entry['weapons'][3]['name']]
    stage_id = stage_ids[entry['stage']['name']]
    embed.add_field(
        name = "~ WEAPONS ~",
        value = (
            get_name("weapon", weapon_id1) + '\n'
            + get_name("weapon", weapon_id2) + '\n'
            + get_name("weapon", weapon_id3) + '\n'
            + get_name("weapon", weapon_id4)
        ),
        inline = False
    )
    embed.add_field(
        name = "~ STAGE ~",
        value = get_name("stage", stage_id),
        inline = False
    )
    embed.set_image(url = entry['stage']['image'])
    return embed



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

def merge_tc_image(im1, im2, im3):
    w = max(im1.size[0], im2.size[0], im3.size[0])
    h = im1.size[1] + im2.size[1] + im3.size[1]
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))
    im.paste(im3, (0, im1.size[1]+im2.size[1]))
    return im

def create_image(url1, url2):
    img1 = read_image(url1)
    img2 = read_image(url2)
    img = merge_image(img1, img2)
    return img

def create_tc_image(url1, url2, url3):
    img1 = read_image(url1)
    img2 = read_image(url2)
    img3 = read_image(url3)
    img = merge_tc_image(img1, img2, img3)
    return img

def embed_stage_image(url1, url2):
    im = create_image(url1, url2)
    b = BytesIO()
    im.save(b, "PNG")
    b.seek(0)
    return b

def embed_tc_stage_image(url1, url2, tcid):
    im = create_tc_image(url1, url2, tcid)
    b = BytesIO()
    im.save(b, "PNG")
    b.seek(0)
    return b

def get_name(name_type: str, name_id: int):
    if name_type == 'stage':
        return stage_names[name_id][os.getenv('BOT_LANG')]
    elif name_type == 'weapon':
        return weapon_names[name_id][os.getenv('BOT_LANG')]
    elif name_type == 'rule':
        return rule_names[name_id][os.getenv('BOT_LANG')]

def archive_menu():
    if os.getenv('BOT_LANG') == "CN":
        embed = discord.Embed(
            title = f"目前库中有{len(sp3db)}个条目."
            )
        embed.add_field(
                name = "~ Contents ~",
                value = (
                    '\n'.join(['\t'.join(['`'+str(n)+'`',l[1]]) for (n,l) in sp3db.items()])
                    + '\n\n**请使用`?archive n`来查看第`n`个 条目。**' 
                ),
                inline = False
            )
        return embed
    if (os.getenv('BOT_LANG') == "EN") or (os.getenv('BOT_LANG') == "JP"):
        embed = discord.Embed(
            title = f"There are {len(sp3db)} entries in the archive."
            )
        embed.add_field(
                name = "~ Contents ~",
                value = (
                    '\n'.join(['\t'.join(['`'+str(n)+'`',l[2]]) for (n,l) in sp3db.items()])
                    + '\n\n**Please use `?archive n` to view `n`th entry.**' 
                ),
                inline = False
            )
        return embed

def show_archive(n: int):
    if (n < 1) or (n > len(sp3db)):
        return {
            'CN': f'无效的n，请输入一个在[1, {len(sp3db)}]之内的n！',
            'EN': 'The index is invalid. Please input an `n` in [1, {len(sp3db)}]',
            'JP': 'The index is invalid. Please input an `n` in [1, {len(sp3db)}]'
            }
    else:
        return (f'**#{n}: ' + ' / '.join(sp3db[n][1:3]) + '**\n' + sp3db[n][0])