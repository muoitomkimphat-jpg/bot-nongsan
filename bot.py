import discord
from discord.ext import commands, tasks
import os, time, json, datetime, difflib

# ==========================
# 🔑 TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("❌ Chưa thêm TOKEN!")
    exit()

# ==========================
# 📌 ID KÊNH
# ==========================
CHANNEL_PHU_ID = 1465291905368854570
CHANNEL_CHINH_ID = 1466801337361764506

CHANNEL_TOP_NONG_SAN = 1468562267267141877
CHANNEL_TOP_CONG_CU = 1468562389443280927
CHANNEL_TOP_THOI_TIET = 1468562439930118367

# ==========================
# 🌾 ROLE
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059

# ==========================
# 🖼️ BANNER
# ==========================
BANNER_MAIN_URL = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688569311826186/ChatGPT_Image_21_51_11_4_thg_2_2026.png?v=2"
BANNER_TOP_URL  = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688625360310576/ChatGPT_Image_21_37_31_4_thg_2_2026.png?v=2"

# ==========================
# 🌾 NÔNG SẢN
# ==========================
NONG_SAN = {
    "bí ngô": ("Bí Ngô", "<:bi_ngo:1468559344676110529>", "Yeongman"),
    "dưa hấu": ("Dưa Hấu", "<:dua_hau:1468559217316331624>", "Yeongman"),
    "dừa": ("Dừa", "<:dua:1468559538159357972>", "Yeongman"),
    "xoài": ("Xoài", "<:xoai:1468559607247933513>", "Yeongman"),
    "đậu thần": ("Đậu Thần", "<:dau_than:1468559814236962972>", "Yeongman"),
    "khế": ("Khế", "<:khe:1468559895602397343>", "Yeongman"),
    "táo đường": ("Táo Đường", "<:tao_duong:1468559984693612656>", "Yeongman"),
    "trái cổ đại": ("Trái Cổ Đại", "<:trai_co_dai:1468559690278502462>", "Yeongman"),
    "sung": ("Sung", "<:sung:1468838967297446149>", "Yeongman"),
    "mãng cầu": ("Mãng Cầu", "<:mang_cau:1468833219758657546>", "Yeongman"),
    "đu đủ": ("Đu Đủ", "<:du_du:1468836544532975708>", "Yeongman")
}

# ==========================
# 🛠️ CÔNG CỤ
# ==========================
CONG_CU = {
    "vòi đỏ": ("Vòi Đỏ", "<:voi_do:1468565773592301619>", "Lena"),
    "vòi xanh": ("Vòi Xanh", "<:voi_xanh:1468565853074362440>", "Lena")
}

# ==========================
# 🌦️ THỜI TIẾT
# ==========================
THOI_TIET = {
    "bão tuyết": ("Bão Tuyết", "<:bao_tuyet:1468560083465015443>", "Băng"),
    "tuyết": ("Tuyết", "<:tuyet:1468560669879308322>", "Khí Lạnh"),
    "mưa rào": ("Mưa Rào", "<:mua_rao:1468560753060741140>", "Ẩm Ướt"),
    "mưa bão": ("Mưa Bão", "<:mua_bao:1468560932325294205>", "Nhiễm Điện"),
    "sương mù": ("Sương Mù", "<:suong_mu:1468561014844035237>", "Ẩm Ướt"),
    "sương sớm": ("Sương Sớm", "<:suong_som:1468561105428152543>", "Sương"),
    "gió": ("Gió", "<:gio:1468561516872732703>", "Gió"),
    "gió cát": ("Gió Cát", "<:gio_cat:1468561637593190632>", "Cát"),
    "cực quang": ("Cực Quang", "<:cuc_quang:1468561214786371696>", "Cực Quang"),
    "ánh trăng": ("Ánh Trăng", "<:anh_trang:1468561408416546853>", "Ánh Trăng"),
    "nắng nóng": ("Nắng Nóng", "<:nang_nong:1468561712411316356>", "Khô")
}

ALL_KEYWORDS = {**NONG_SAN, **CONG_CU, **THOI_TIET}

# ==========================
# ⏳ RESET
# ==========================
RESET_TIME = {"nong_san": 300, "cong_cu": 1800, "thoi_tiet": 300}
da_bao = {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}

# ==========================
# 🏆 TOP FILE
# ==========================
TOP_FILE = "top_week.json"
LAST_TOP_FILE = "last_top.json"

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

top_data = load_json(TOP_FILE, {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}})
last_top = load_json(LAST_TOP_FILE, {"week": ""})

# ==========================
# 🤖 BOT
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def emoji_url(e):
    if e.startswith("<:"):
        return f"https://cdn.discordapp.com/emojis/{e.split(':')[2][:-1]}.png"
    return None

async def send_embed(channel, title, desc, emoji):
    embed = discord.Embed(title=title, description=desc, color=0x00ff99)
    embed.set_thumbnail(url=emoji_url(emoji))
    embed.set_image(url=BANNER_MAIN_URL)
    await channel.send(embed=embed)

async def xu_ly(message, loai, ten, emoji, npc=None, bien_the=None):
    now = time.time()
    if ten in da_bao[loai] and now - da_bao[loai][ten] < RESET_TIME[loai]:
        await message.reply("❌ Đã có người báo rồi!")
        return

    da_bao[loai][ten] = now
    uid = str(message.author.id)
    top_data[loai].setdefault(uid, {"count": 0})
    top_data[loai][uid]["count"] += 1
    save_json(TOP_FILE, top_data)

    channel = bot.get_channel(CHANNEL_CHINH_ID)
    if not channel:
        return

    await channel.send(f"<@&{ROLE_NONG_DAN_ID}> **{ten}**")

    if loai == "thoi_tiet":
        desc = f"{emoji} **{ten}**\n🌈 Biến thể: **[{bien_the}]**"
        title = "🔔 THÔNG BÁO THỜI TIẾT"
    else:
        time_txt = "5 phút" if loai == "nong_san" else "30 phút"
        icon = "🛒" if loai == "nong_san" else "🛠️"
        title = f"🔔 THÔNG BÁO {'NÔNG SẢN' if loai=='nong_san' else 'CÔNG CỤ'}"
        desc = f"{emoji} **{ten}**\n{icon} NPC: **[{npc}]**\n⏳ Reset: **{time_txt}**"

    await send_embed(channel, title, desc, emoji)

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != CHANNEL_PHU_ID:
        return

    text = message.content.lower().strip()

    if text in NONG_SAN:
        await xu_ly(message, "nong_san", *NONG_SAN[text])
    elif text in CONG_CU:
        await xu_ly(message, "cong_cu", *CONG_CU[text])
    elif text in THOI_TIET:
        ten, emoji, bt = THOI_TIET[text]
        await xu_ly(message, "thoi_tiet", ten, emoji, bien_the=bt)
    else:
        sug = difflib.get_close_matches(text, ALL_KEYWORDS.keys(), n=1)
        await message.reply(f"❌ Sai từ khóa. Bạn muốn `{sug[0]}`?" if sug else "❌ Không hợp lệ!")

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("✅ Bot Online!")

bot.run(TOKEN)
