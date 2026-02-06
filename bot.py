import discord
from discord.ext import commands, tasks
import datetime, os, json, time

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")

CHANNEL_PHU_ID = 1465291905368854570
CHANNEL_CHINH_ID = 1466801337361764506
ROLE_NONG_DAN = 1465291719087100059

DATA_FILE = "data.json"
COOLDOWN = 10

BANNER_MAIN_URL = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688569311826186/ChatGPT_Image_21_51_11_4_thg_2_2026.png"

NPC_AVATAR = {
    "Yeongman": "https://media.discordapp.net/attachments/1468688509979070565/1468908847694348473/z7504419521891_461a1bd4d3a1c978eea1248c7003ed4b.jpg",
    "Lena": "https://media.discordapp.net/attachments/1468688509979070565/1468908847245561888/z7504419521703_4a9005c06995d2b1eb40ab8df4873d65.jpg",
    "Tiến Sĩ Brown": "https://media.discordapp.net/attachments/1468688509979070565/1468908846914338978/z7504419517485_04a4fe6fdb416725a0c77bf5aeff98e1.jpg"
}

# ================= BOT =================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ================= TIME =================
def vn_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=7)

def time_block():
    h = vn_time().hour
    if 5 <= h < 11: return "sáng"
    if 11 <= h < 14: return "trưa"
    if 14 <= h < 18: return "chiều"
    return "tối"

# ================= DATA =================
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE,"w",encoding="utf8") as f:
            json.dump({"farm":{}, "tools":{}, "weather":{}, "last_reset":time.time()}, f)
    with open(DATA_FILE,"r",encoding="utf8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE,"w",encoding="utf8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

data = load_data()
last_notify = {}

# ================= ALIAS =================
ALIASES = {
    "bí": "bí ngô",
    "dưa": "dưa hấu"
}

# ================= ITEM INFO =================
ITEM_INFO = {
    # -------- FARM --------
    "bí ngô": {"group":"farm","name":"Bí Ngô","emoji":"<:bi_ngo:1468559344676110529>","npc":"Yeongman",
        "lines":{"sáng":"Bí ngô sáng nay tươi lắm!","trưa":"Bí ngô trưa hàng đẹp!","chiều":"Chiều rồi, bí ngô bán chạy!","tối":"Tối đến rồi, bí ngô còn đó!"}},
    "dưa hấu": {"group":"farm","name":"Dưa Hấu","emoji":"<:dua_hau:1468559217316331624>","npc":"Yeongman",
        "lines":{"sáng":"Dưa hấu sáng mát lạnh!","trưa":"Trưa nóng có dưa hấu là chuẩn!","chiều":"Dưa hấu chiều rất ngon!","tối":"Tối rồi, dưa hấu vẫn còn!"}},
    "dừa": {"group":"farm","name":"Dừa","emoji":"<:dua:1468559538159357972>","npc":"Yeongman",
        "lines":{"sáng":"Dừa sáng nay nước nhiều!","trưa":"Trưa, uống dừa mát, giải nhiệt cơ thể đấy!","chiều":"Chiều uống dừa đúng bài luôn!","tối":"Tối rồi mà dừa vẫn còn!"}},
    "xoài": {"group":"farm","name":"Xoài","emoji":"<:xoai:1468559607247933513>","npc":"Yeongman",
        "lines":{"sáng":"Xoài sáng chín vừa!","trưa":"Xoài trưa ngọt đậm!","chiều":"Chiều rồi, xoài bán chạy!","tối":"Tối đến, xoài sắp hết!"}},
    "táo đường": {"group":"farm","name":"Táo Đường","emoji":"<:tao_duong:1468559984693612656>","npc":"Yeongman",
        "lines":{"sáng":"Táo đường sáng hiếm lắm!","trưa":"Táo đường trưa ăn tráng miệng!","chiều":"Chiều rồi, táo đường bán mạnh!","tối":"Tối đến, táo đường còn ít!"}},
    "khế": {"group":"farm","name":"Khế","emoji":"<:khe:1468559895602397343>","npc":"Yeongman",
        "lines":{"sáng":"Khế sáng tươi roi rói!","trưa":"Khế trưa giá tốt!","chiều":"Chiều khế bán ổn!","tối":"Tối rồi, khế vẫn còn!"}},
    "đậu thần": {"group":"farm","name":"Đậu Thần","emoji":"<:dau_than:1468559814236962972>","npc":"Yeongman",
        "lines":{"sáng":"Đậu thần sáng rất hiếm!","trưa":"Đậu thần trưa xuất hiện kìa!","chiều":"Chiều gặp đậu thần là hên!","tối":"Tối rồi, ai nhanh thì có!"}},
    "sung": {"group":"farm","name":"Sung","emoji":"<:sung:1468838967297446149>","npc":"Yeongman",
        "lines":{"sáng":"Sung vừa mới hái đây!","trưa":"Sung trưa bán chạy lắm còn ít hàng!","chiều":"Chiều nhiều người hỏi sung quá còn 1 ít!","tối":"Tối rồi, sung ế rồi!"}},
    "mãng cầu": {"group":"farm","name":"Mãng Cầu","emoji":"<:mang_cau:1468833219758657546>","npc":"Yeongman",
        "lines":{"sáng":"Mãng cầu sáng rất thơm!","trưa":"Mãng cầu chín cây đê bà con cô bác ơi!","chiều":"Chiều mãng cầu bán mạnh!","tối":"Tối rồi, mãng cầu còn ít!"}},
    "đu đủ": {"group":"farm","name":"Đu Đủ","emoji":"<:du_du:1468836544532975708>","npc":"Yeongman",
        "lines":{"sáng":"Đu đủ tươi ngon đây!","trưa":"Đu đủ trưa ăn giải nhiệt đi nào!","chiều":"Chiều ăn đu đủ là hợp nhất!","tối":"Tối rồi, đu đủ ăn đẹp da đấy!"}},

    # -------- TOOLS --------
    "vòi đỏ": {"group":"tools","name":"Vòi Đỏ","emoji":"<:voi_do:1468565773592301619>","npc":"Lena",
        "lines":{"sáng":"Vòi đỏ mới mỗi ngày!","trưa":"Vòi đỏ trưa tăng năng suất cây trồng!","chiều":"Chiều, vòi đỏ bán chạy lắm đấy!","tối":"Tối rồi, mại dzô...mại dzô vòi đỏ sắp hết!"}},
    "vòi xanh": {"group":"tools","name":"Vòi Xanh","emoji":"<:voi_xanh:1468565853074362440>","npc":"Lena",
        "lines":{"sáng":"Vòi xanh hàng mới lên kệ!","trưa":"Cần tưới nước cho hoa màu trong vườn!","chiều":"Vòi xanh sắp hết tranh thủ mua nhanh kẻo hết!","tối":"Tối rồi, vòi xanh hàng vẫn còn ế!"}},

    # -------- WEATHER --------
    "mưa": {"group":"weather","name":"Mưa","emoji":"<:mua:1469282976012435568>","variant":"Ẩm Ướt","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Mưa sáng làm không khí ẩm hơn!","trưa":"Mưa trưa ảnh hưởng mùa vụ!","chiều":"Mưa chiều thay đổi thời tiết!","tối":"Mưa tối khiến môi trường ẩm!"}},
    "bão": {"group":"weather","name":"Bão","emoji":"<:bao:1469282944475725968>","variant":"Nhiễm Điện","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Bão sáng mang điện tích mạnh!","trưa":"Bão trưa cực kỳ nguy hiểm!","chiều":"Bão chiều cần chú ý an toàn!","tối":"Bão tối ảnh hưởng lớn đến khu vực!"}},
    "sương mù": {"group":"weather","name":"Sương Mù","emoji":"<:suong_mu:1468561014844035237>","variant":"Ẩm Ướt","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Sương mù sáng rất dày!","trưa":"Sương mù trưa vẫn chưa tan!","chiều":"Chiều sương mù ảnh hưởng tầm nhìn!","tối":"Sương mù tối rất dày!"}},
    "sương sớm": {"group":"weather","name":"Sương Sớm","emoji":"<:suong_som:1468561105428152543>","variant":"Sương","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Sương sớm sáng chưa tan!","trưa":"Trưa sương dần tan bớt!","chiều":"Sương chiều xuất hiện khá lạ!","tối":"Sương tối xuất hiện nhẹ!"}},
    "cực quang": {"group":"weather","name":"Cực Quang","emoji":"<:cuc_quang:1468561214786371696>","variant":"Cực Quang","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Cực quang sáng rất hiếm đấy!","trưa":"Cực quang trưa đặc biệt đó cần chú ý!","chiều":"Cực quang chiều dần hiện rõ!","tối":"Cực quang tối khá đẹp đấy nhá!"}},
    "ánh trăng": {"group":"weather","name":"Ánh Trăng","emoji":"<:anh_trang:1468561408416546853>","variant":"Ánh Trăng","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Ánh trăng sáng còn sót lại!","trưa":"Ánh trăng trưa khá yếu!","chiều":"Ánh trăng chiều dần xuất hiện!","tối":"Ánh trăng tối rất rõ!"}},
    "gió": {"group":"weather","name":"Gió","emoji":"<:gio:1468561516872732703>","variant":"Gió","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Gió sáng thổi nhẹ!","trưa":"Gió trưa thổi khá mạnh!","chiều":"Gió chiều mát mẻ, dễ chịu!","tối":"Gió tối khá lạnh!"}},
    "gió cát": {"group":"weather","name":"Gió Cát","emoji":"<:gio_cat:1468561637593190632>","variant":"Cát","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Gió cát buổi sáng đang hình thành!","trưa":"Gió cát trưa rất nguy hiểm, cần chú ý tầm nhìn!","chiều":"Gió cát chiều chưa suy giảm!","tối":"Gió cát tối vẫn còn mạnh!"}},
    "nắng nóng": {"group":"weather","name":"Nắng Nóng","emoji":"<:nang_nong:1468561712411316356>","variant":"Khô","npc":"Tiến Sĩ Brown",
        "lines":{"sáng":"Buổi sáng nắng nóng sớm hơn mọi ngày!","trưa":"Nắng trưa 36*C gay gắt, cần trang bị bảo hộ!","chiều":"Chiều nắng nóng kéo dài!","tối":"Tối vẫn còn oi bức!"}}
}

# ================= WEBHOOK =================
async def send_npc(channel, npc, embed):
    hooks = await channel.webhooks()
    hook = discord.utils.get(hooks, name=npc)
    if not hook:
        hook = await channel.create_webhook(name=npc)
    await hook.send(embed=embed, username=npc, avatar_url=NPC_AVATAR[npc])

    # ================= EMOJI TO URL =================
def emoji_to_url(emoji: str):
    if emoji.startswith("<:") and emoji.endswith(">"):
        emoji_id = emoji.split(":")[2].replace(">", "")
        return f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    return None

# ================= LISTENER =================
@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != CHANNEL_PHU_ID:
        return

    text = message.content.lower()
    for a,b in ALIASES.items():
        text = text.replace(a,b)

    channel = bot.get_channel(CHANNEL_CHINH_ID)
    now = time_block()
    pinged = False

    for item,info in ITEM_INFO.items():
        if item in text:
            if item in last_notify and time.time() - last_notify[item] < COOLDOWN:
                continue

            last_notify[item] = time.time()
            data[info["group"]][item] = data[info["group"]].get(item,0) + 1
            save_data(data)

            embed = discord.Embed(
                title=f"📢 THÔNG BÁO {info['group'].upper()}",
                description=f"{info['emoji']} **{info['name']}**",
                color=0x00ffaa
            )
            emoji_url = emoji_to_url(info["emoji"])
            if emoji_url:
                embed.set_thumbnail(url=emoji_url)

            embed.set_author(name=info["npc"], icon_url=NPC_AVATAR[info["npc"]])

            if "variant" in info:
                embed.add_field(name="Biến Thể", value=info["variant"], inline=True)

            embed.add_field(
                name="💬",
                value=f"{info['npc']}: {info['lines'][now]}",
                inline=False
            )

            embed.set_image(url=BANNER_MAIN_URL)

            if not pinged:
                await channel.send(f"<@&{ROLE_NONG_DAN}>")
                pinged = True

            await send_npc(channel, info["npc"], embed)

# ================= TOP WEEK =================
@bot.tree.command(name="top", description="Xem top tuần")
async def top(interaction: discord.Interaction):
    d = load_data()
    embed = discord.Embed(title="🏆 TOP TUẦN", color=0xffd700)

    for g in ["farm","tools","weather"]:
        top3 = sorted(d[g].items(), key=lambda x:x[1], reverse=True)[:3]
        txt = ""
        for i,(n,v) in enumerate(top3):
            medal = ["🥇","🥈","🥉"][i]
            txt += f"{medal} {n}: {v}\n"
        embed.add_field(name=g.upper(), value=txt or "Chưa có dữ liệu", inline=False)

    await interaction.response.send_message(embed=embed)

# ================= RESET WEEK =================
@tasks.loop(hours=1)
async def weekly_reset():
    if time.time() - data["last_reset"] >= 604800:
        data["farm"]={}
        data["tools"]={}
        data["weather"]={}
        data["last_reset"]=time.time()
        save_data(data)

@bot.event
async def on_ready():
    weekly_reset.start()
    await bot.tree.sync()
    print("✅ BOT ONLINE – FULL NPC SYSTEM")

bot.run(TOKEN)
