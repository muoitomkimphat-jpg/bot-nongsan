import discord
from discord.ext import commands, tasks
import os, time, json
import datetime
import difflib

# ==========================
# 🔑 TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ Bạn chưa thêm TOKEN vào Variables!")
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
# 🌾 ROLE PING
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059

# ==========================
# 🖼️ BANNER
# ==========================
BANNER_MAIN_URL = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688569311826186/ChatGPT_Image_21_51_11_4_thg_2_2026.png?ex=6984ee51&is=69839cd1&hm=1edab68d84f0fc3e81855ccc55accca872aac973c41f5bcb688a6503cf3b2b8d&"
BANNER_TOP_URL = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688625360310576/ChatGPT_Image_21_37_31_4_thg_2_2026.png?ex=6984ee5f&is=69839cdf&hm=14a5a60764ca4e23fc278101f390cb622067f2a2449378278dced55d0847050e&"

# ==========================
# 🌾 NÔNG SẢN + NPC
# ==========================
NONG_SAN = {
    "bí ngô": ("Bí Ngô", "<:bi_ngo:1468559344676110529>", "Yeongman"),
    "dưa hấu": ("Dưa Hấu", "<:dua_hau:1468559217316331624>", "Yeongman"),
    "dừa": ("Dừa", "<:dua:1468559538159357972>", "Yeongman"),
    "xoài": ("Xoài", "<:xoai:1468559607247933513>", "Yeongman"),
    "đậu thần": ("Đậu Thần", "<:dau_than:1468559814236962972>", "Yeongman"),
    "khế": ("Khế", "<:khe:1468559895602397343>", "Yeongman"),
    "táo đường": ("Táo Đường", "<:tao_duong:1468559984693612656>", "Yeongman"),
    "trái cổ đại": ("Trái Cổ Đại", "<:trai_co_dai:1468559690278502462>", "Yeongman")
}

# ==========================
# 🛠️ CÔNG CỤ + NPC
# ==========================
CONG_CU = {
    "vòi đỏ": ("Vòi Đỏ", "<:voi_do:1468565773592301619>", "Lena"),
    "vòi xanh": ("Vòi Xanh", "<:voi_xanh:1468565853074362440>", "Lena")
}

# ==========================
# 🌦️ THỜI TIẾT + BIẾN THỂ
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
# ⏳ RESET TIME
# ==========================
RESET_TIME = {
    "nong_san": 300,
    "cong_cu": 1800,
    "thoi_tiet": 300
}

da_bao = {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}

# ==========================
# 🏆 FILE TOP
# ==========================
TOP_FILE = "top_week.json"
LAST_TOP_FILE = "last_top_sent.json"


def init_files():
    if not os.path.exists(TOP_FILE):
        with open(TOP_FILE, "w", encoding="utf-8") as f:
            json.dump({"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}, f)

    if not os.path.exists(LAST_TOP_FILE):
        with open(LAST_TOP_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_week": ""}, f)


def load_top():
    init_files()
    with open(TOP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_top(data):
    with open(TOP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_last_top():
    init_files()
    with open(LAST_TOP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last_top(data):
    with open(LAST_TOP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


top_data = load_top()
last_top_data = load_last_top()

# ==========================
# ✅ EMOJI URL
# ==========================
def get_emoji_url(emoji_text):
    if emoji_text.startswith("<:"):
        emoji_id = emoji_text.split(":")[2].replace(">", "")
        return f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    return None

# ==========================
# 🤖 BOT SETUP
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 📢 SEND EMBED
# ==========================
async def send_embed(channel, title, desc, emoji, banner):
    embed = discord.Embed(title=title, description=desc, color=0x00ff99)
    embed.set_thumbnail(url=get_emoji_url(emoji))
    embed.set_image(url=banner)
    await channel.send(embed=embed)

# ==========================
# 📌 XỬ LÝ BÁO
# ==========================
async def xu_ly_bao(message, loai, ten, emoji, npc=None, bien_the=None):
    now = time.time()

    if ten in da_bao[loai]:
        if now - da_bao[loai][ten] < RESET_TIME[loai]:
            await message.reply("❌ Đã có người báo rồi!")
            return

    da_bao[loai][ten] = now

    # cộng TOP tuần
    uid = str(message.author.id)
    top_data[loai].setdefault(uid, {"count": 0})
    top_data[loai][uid]["count"] += 1
    save_top(top_data)

    channel = bot.get_channel(CHANNEL_CHINH_ID)
    ping = f"<@&{ROLE_NONG_DAN_ID}> **{ten}**"

    if loai == "nong_san":
        title = "🔔 THÔNG BÁO NÔNG SẢN"
        desc = f"{emoji} **{ten}**\n🛒 NPC: **[{npc}]**\n⏳ Làm mới sau: **5 phút**"

    elif loai == "cong_cu":
        title = "🔔 THÔNG BÁO CÔNG CỤ"
        desc = f"{emoji} **{ten}**\n🛠️ NPC: **[{npc}]**\n⏳ Làm mới sau: **30 phút**"

    else:
        title = "🔔 THÔNG BÁO THỜI TIẾT"
        desc = f"{emoji} **{ten}**\n Biến thể: **[{bien_the}]**"

    await channel.send(content=ping)
    await send_embed(channel, title, desc, emoji, BANNER_MAIN_URL)

# ==========================
# 🏆 LỆNH !TOP
# ==========================
@bot.command()
async def top(ctx, loai=None):
    if loai not in ["nong_san", "cong_cu", "thoi_tiet"]:
        await ctx.send("❌ Dùng: `!top nong_san` / `!top cong_cu` / `!top thoi_tiet`")
        return

    data = top_data.get(loai, {})
    if not data:
        await ctx.send("❌ Chưa có ai báo tuần này!")
        return

    top_list = sorted(data.items(), key=lambda x: x[1]["count"], reverse=True)[:5]

    medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
    text = ""
    for i, (uid, info) in enumerate(top_list):
        text += f"{medals[i]} <@{uid}> : **{info['count']}** lần\n"

    embed = discord.Embed(
        title=f"🏆 TOP {loai.upper()} TUẦN",
        description=text,
        color=0x00ff99
    )
    embed.set_image(url=BANNER_TOP_URL)

    await ctx.send(embed=embed)

# ==========================
# 🏆 AUTO TOP TUẦN (KHÔNG MISS)
# ==========================
@tasks.loop(minutes=1)
async def auto_top_week():
    now = datetime.datetime.now()
    current_week = now.strftime("%Y-W%U")

    if now.weekday() != 0:
        return

    if now.hour != 0:
        return

    if last_top_data["last_week"] == current_week:
        return

    async def send_top(loai, channel_id, title):
        channel = bot.get_channel(channel_id)
        if channel is None:
            return

        data = top_data.get(loai, {})
        if not data:
            await channel.send("❌ Tuần này chưa có ai báo.")
            return

        top_list = sorted(data.items(), key=lambda x: x[1]["count"], reverse=True)[:5]

        medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
        text = ""

        for i, (uid, info) in enumerate(top_list):
            text += f"{medals[i]} <@{uid}> : **{info['count']}** lần\n"

        embed = discord.Embed(
            title=f"🏆 {title}",
            description=text,
            color=0x00ff99
        )
        embed.set_image(url=BANNER_TOP_URL)

        await channel.send(embed=embed)

        top_data[loai].clear()
        save_top(top_data)

    await send_top("nong_san", CHANNEL_TOP_NONG_SAN, "TOP TUẦN NÔNG SẢN")
    await send_top("cong_cu", CHANNEL_TOP_CONG_CU, "TOP TUẦN CÔNG CỤ")
    await send_top("thoi_tiet", CHANNEL_TOP_THOI_TIET, "TOP TUẦN THỜI TIẾT")

    last_top_data["last_week"] = current_week
    save_last_top(last_top_data)

# ==========================
# 📩 ON MESSAGE
# ==========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_PHU_ID:
        return

    text = message.content.lower().strip()

    if text in NONG_SAN:
        ten, emoji, npc = NONG_SAN[text]
        await xu_ly_bao(message, "nong_san", ten, emoji, npc=npc)

    elif text in CONG_CU:
        ten, emoji, npc = CONG_CU[text]
        await xu_ly_bao(message, "cong_cu", ten, emoji, npc=npc)

    elif text in THOI_TIET:
        ten, emoji, bien_the = THOI_TIET[text]
        await xu_ly_bao(message, "thoi_tiet", ten, emoji, bien_the=bien_the)

    else:
        sug = difflib.get_close_matches(text, ALL_KEYWORDS.keys(), n=1)
        if sug:
            await message.reply(f"❌ Sai từ khóa. Bạn muốn `{sug[0]}`?")
        else:
            await message.reply("❌ Không hợp lệ!")

    await bot.process_commands(message)

# ==========================
# ✅ READY
# ==========================
@bot.event
async def on_ready():
    print("✅ Bot Online!")
    auto_top_week.start()
    print("📌 Dùng: !top nong_san / cong_cu / thoi_tiet")

bot.run(TOKEN)
