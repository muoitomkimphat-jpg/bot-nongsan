import discord
from discord.ext import commands, tasks
import os, time, json, difflib, datetime

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

# ==========================
# 🌾 ROLE
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059

# ==========================
# 🖼️ BANNER
# ==========================
BANNER_MAIN_URL = "https://cdn.discordapp.com/attachments/1468688509979070565/1468688569311826186/ChatGPT_Image_21_51_11_4_thg_2_2026.png"

# ==========================
# 👤 NPC AVATAR
# ==========================
NPC_AVATAR = {
    "Yeongman": "https://i.imgur.com/yeongman.png",
    "Tiến Sĩ Brown": "https://i.imgur.com/brown.png",
    "Lena": "https://i.imgur.com/lena.png"
}

# ==========================
# 🌾 NÔNG SẢN
# ==========================
NONG_SAN = {
    "bí ngô": ("Bí Ngô", "<:bi_ngo:1468559344676110529>", "Yeongman"),
    "dưa hấu": ("Dưa Hấu", "<:dua_hau:1468559217316331624>", "Yeongman"),
    "dừa": ("Dừa", "<:dua:1468559538159357972>", "Yeongman"),
    "xoài": ("Xoài", "<:xoai:1468559607247933513>", "Yeongman"),
    "táo đường": ("Táo Đường", "<:tao_duong:1468559984693612656>", "Yeongman"),
    "khế": ("Khế", "<:khe:1468559895602397343>", "Yeongman"),
    "đậu thần": ("Đậu Thần", "<:dau_than:1468559814236962972>", "Yeongman"),
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
    "mưa": ("Mưa", "<:mua_rao:1468560753060741140>", "Ẩm Ướt", "Tiến Sĩ Brown"),
    "mưa bão": ("Mưa Bão", "<:mua_bao:1468560932325294205>", "Nhiễm Điện", "Tiến Sĩ Brown"),
    "sương mù": ("Sương Mù", "<:suong_mu:1468561014844035237>", "Ẩm Ướt", "Tiến Sĩ Brown"),
    "sương sớm": ("Sương Sớm", "<:suong_som:1468561105428152543>", "Sương", "Tiến Sĩ Brown"),
    "cực quang": ("Cực Quang", "<:cuc_quang:1468561214786371696>", "Cực Quang", "Tiến Sĩ Brown"),
    "ánh trăng": ("Ánh Trăng", "<:anh_trang:1468561408416546853>", "Ánh Trăng", "Tiến Sĩ Brown"),
    "gió": ("Gió", "<:gio:1468561516872732703>", "Gió", "Tiến Sĩ Brown"),
    "gió cát": ("Gió Cát", "<:gio_cat:1468561637593190632>", "Cát", "Tiến Sĩ Brown")
}

# ==========================
# 🧠 NPC LINE
# ==========================
NPC_LINES = {
    # ================= NÔNG SẢN =================
    "bí ngô": {
        "sáng": "Yeongman: Bí ngô buổi sáng rất tươi, mua sớm lời lắm đó!",
        "trưa": "Yeongman: Bí ngô trưa nay hàng đẹp, tranh thủ kẻo hết!",
        "chiều": "Yeongman: Chiều rồi, bí ngô này bán chạy lắm nha!",
        "tối": "Yeongman: Tối đến rồi, ai cần bí ngô thì ghé liền đi!"
    },
    "dưa hấu": {
        "sáng": "Yeongman: Dưa hấu sáng nay ngọt mát, giải nhiệt cực tốt!",
        "trưa": "Yeongman: Trưa nóng mà có dưa hấu là đúng bài luôn!",
        "chiều": "Yeongman: Dưa hấu chiều nay chất lượng lắm đó!",
        "tối": "Yeongman: Tối rồi, dưa hấu vẫn còn nè!"
    },
    "dừa": {
        "sáng": "Yeongman: Dừa sáng nay nước nhiều, rất đáng mua!",
        "trưa": "Yeongman: Dừa trưa nay uống là mát liền!",
        "chiều": "Yeongman: Chiều có dừa là hết sảy!",
        "tối": "Yeongman: Dừa tối nay vẫn còn trong shop đó!"
    },
    "xoài": {
        "sáng": "Yeongman: Xoài sáng nay chín vừa, thơm lắm!",
        "trưa": "Yeongman: Xoài trưa nay ngọt đậm vị luôn!",
        "chiều": "Yeongman: Chiều ăn xoài là hợp lý nhất!",
        "tối": "Yeongman: Xoài tối nay bán nốt đó!"
    },
    "táo đường": {
        "sáng": "Yeongman: Táo đường sáng nay rất hiếm đó nha!",
        "trưa": "Yeongman: Táo đường trưa nay ai nhanh thì có!",
        "chiều": "Yeongman: Chiều rồi, táo đường bán chạy lắm!",
        "tối": "Yeongman: Tối nay táo đường sắp hết hàng!"
    },
    "khế": {
        "sáng": "Yeongman: Khế sáng nay tươi roi rói luôn!",
        "trưa": "Yeongman: Khế trưa nay giá tốt lắm!",
        "chiều": "Yeongman: Khế chiều nay rất được ưa chuộng!",
        "tối": "Yeongman: Tối rồi, khế vẫn còn trong shop!"
    },
    "đậu thần": {
        "sáng": "Yeongman: Đậu thần sáng nay hiếm lắm đó!",
        "trưa": "Yeongman: Đậu thần trưa nay xuất hiện kìa!",
        "chiều": "Yeongman: Chiều gặp đậu thần là hên lắm!",
        "tối": "Yeongman: Đậu thần tối nay ai nhanh thì có!"
    },
    "sung": {
        "sáng": "Yeongman: Sung sáng nay chất lượng cao nha!",
        "trưa": "Yeongman: Sung trưa nay bán khá chạy đó!",
        "chiều": "Yeongman: Chiều nay nhiều người hỏi sung lắm!",
        "tối": "Yeongman: Sung tối nay vẫn còn đó!"
    },
    "mãng cầu": {
        "sáng": "Yeongman: Mãng cầu sáng nay rất thơm!",
        "trưa": "Yeongman: Mãng cầu trưa nay ngon lắm!",
        "chiều": "Yeongman: Chiều nay mãng cầu bán chạy ghê!",
        "tối": "Yeongman: Mãng cầu tối nay còn ít thôi!"
    },
    "đu đủ": {
        "sáng": "Yeongman: Đu đủ sáng nay chín đều lắm!",
        "trưa": "Yeongman: Đu đủ trưa nay rất đẹp!",
        "chiều": "Yeongman: Chiều ăn đu đủ là hợp lý nhất!",
        "tối": "Yeongman: Đu đủ tối nay vẫn còn nha!"
    },

    # ================= THỜI TIẾT =================
    "mưa": {
        "sáng": "Tiến Sĩ Brown: Mưa sáng làm không khí ẩm ướt hơn!",
        "trưa": "Tiến Sĩ Brown: Mưa trưa ảnh hưởng khá nhiều đó!",
        "chiều": "Tiến Sĩ Brown: Mưa chiều làm thời tiết thay đổi rõ rệt!",
        "tối": "Tiến Sĩ Brown: Mưa tối khiến môi trường rất ẩm!"
    },
    "mưa bão": {
        "sáng": "Tiến Sĩ Brown: Mưa bão sáng mang điện tích mạnh!",
        "trưa": "Tiến Sĩ Brown: Mưa bão trưa cực kỳ nguy hiểm!",
        "chiều": "Tiến Sĩ Brown: Mưa bão chiều cần chú ý an toàn!",
        "tối": "Tiến Sĩ Brown: Mưa bão tối ảnh hưởng lớn đến khu vực!"
    },
    "sương mù": {
        "sáng": "Tiến Sĩ Brown: Sương mù sáng gây ẩm ướt nhiều!",
        "trưa": "Tiến Sĩ Brown: Sương mù trưa vẫn chưa tan hết!",
        "chiều": "Tiến Sĩ Brown: Sương mù chiều ảnh hưởng tầm nhìn!",
        "tối": "Tiến Sĩ Brown: Sương mù tối rất dày đặc!"
    },
    "sương sớm": {
        "sáng": "Tiến Sĩ Brown: Sương sớm sáng rất rõ rệt!",
        "trưa": "Tiến Sĩ Brown: Sương sớm trưa đã tan bớt!",
        "chiều": "Tiến Sĩ Brown: Sương sớm chiều hiếm gặp!",
        "tối": "Tiến Sĩ Brown: Sương sớm tối xuất hiện nhẹ!"
    },
    "cực quang": {
        "sáng": "Tiến Sĩ Brown: Cực quang sáng là hiện tượng hiếm!",
        "trưa": "Tiến Sĩ Brown: Cực quang trưa rất đặc biệt!",
        "chiều": "Tiến Sĩ Brown: Cực quang chiều phát sáng rõ!",
        "tối": "Tiến Sĩ Brown: Cực quang tối là đẹp nhất!"
    },
    "ánh trăng": {
        "sáng": "Tiến Sĩ Brown: Ánh trăng sáng còn sót lại!",
        "trưa": "Tiến Sĩ Brown: Ánh trăng trưa khá yếu!",
        "chiều": "Tiến Sĩ Brown: Ánh trăng chiều dần xuất hiện!",
        "tối": "Tiến Sĩ Brown: Ánh trăng tối rất rõ!"
    },
    "gió": {
        "sáng": "Tiến Sĩ Brown: Gió sáng thổi nhẹ!",
        "trưa": "Tiến Sĩ Brown: Gió trưa khá mạnh!",
        "chiều": "Tiến Sĩ Brown: Gió chiều dễ chịu!",
        "tối": "Tiến Sĩ Brown: Gió tối mát lạnh!"
    },
    "gió cát": {
        "sáng": "Tiến Sĩ Brown: Gió cát sáng mang nhiều cát!",
        "trưa": "Tiến Sĩ Brown: Gió cát trưa rất khó chịu!",
        "chiều": "Tiến Sĩ Brown: Gió cát chiều ảnh hưởng lớn!",
        "tối": "Tiến Sĩ Brown: Gió cát tối vẫn còn mạnh!"
    },

    # ================= CÔNG CỤ =================
    "vòi đỏ": {
        "sáng": "Lena: Vòi đỏ sáng nay dùng rất hiệu quả!",
        "trưa": "Lena: Vòi đỏ trưa giúp tăng năng suất!",
        "chiều": "Lena: Vòi đỏ chiều nay nhiều người mua!",
        "tối": "Lena: Vòi đỏ tối sắp hết hàng!"
    },
    "vòi xanh": {
        "sáng": "Lena: Vòi xanh sáng nay rất ổn định!",
        "trưa": "Lena: Vòi xanh trưa dễ sử dụng!",
        "chiều": "Lena: Vòi xanh chiều bán khá chạy!",
        "tối": "Lena: Vòi xanh tối vẫn còn đó!"
    }
}  # 👈 DÁN NGUYÊN KHỐI BẠN ĐÃ GỬI

# ==========================
# ⏱️ RESET
# ==========================
RESET_TIME = {"nong_san": 300, "cong_cu": 1800, "thoi_tiet": 300}
last_report = {}

# ==========================
# 🏆 TOP TUẦN
# ==========================
TOP_FILE = "top_week.json"
if not os.path.exists(TOP_FILE):
    with open(TOP_FILE, "w") as f:
        json.dump({"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}, f)

def save_top(data):
    with open(TOP_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_top():
    with open(TOP_FILE) as f:
        return json.load(f)

# ==========================
# 🤖 BOT
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def emoji_url(e):
    return f"https://cdn.discordapp.com/emojis/{e.split(':')[2][:-1]}.png"

def get_time_slot():
    h = datetime.datetime.now().hour
    if 5 <= h < 11: return "sáng"
    if 11 <= h < 16: return "trưa"
    if 16 <= h < 19: return "chiều"
    return "tối"

def countdown(loai, key):
    now = time.time()
    t = RESET_TIME[loai] - int(now - last_report.get(key, 0))
    return max(0, t)

def npc_line(key):
    return NPC_LINES.get(key, {}).get(get_time_slot(), "...")

def make_embed(title, npc, emoji, content):
    e = discord.Embed(title=title, description=content, color=0x00ff99)
    e.set_thumbnail(url=emoji_url(emoji))
    e.set_author(name=npc, icon_url=NPC_AVATAR[npc])
    e.set_image(url=BANNER_MAIN_URL)
    return e

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != CHANNEL_PHU_ID:
        return

    text = message.content.lower().strip()
    now = time.time()
    channel = bot.get_channel(CHANNEL_CHINH_ID)
    top = load_top()

    def add_top(loai):
        uid = str(message.author.id)
        top[loai][uid] = top[loai].get(uid, 0) + 1
        save_top(top)

    if text in NONG_SAN:
        ten, emoji, npc = NONG_SAN[text]
        last_report[text] = now
        add_top("nong_san")
        t = countdown("nong_san", text)
        embed = make_embed(
            "🌾 NÔNG SẢN KAIA",
            npc,
            emoji,
            f"{emoji} **{ten}**\nđang bán tại cửa hàng\n\n💬 {npc_line(text)}\n⏳ Làm mới sau: **{t//60} phút : {t%60:02d} giây**"
        )

    elif text in CONG_CU:
        ten, emoji, npc = CONG_CU[text]
        last_report[text] = now
        add_top("cong_cu")
        t = countdown("cong_cu", text)
        embed = make_embed(
            "🛠️ CÔNG CỤ KAIA",
            npc,
            emoji,
            f"{emoji} **{ten}**\nđang bán tại cửa hàng\n\n💬 {npc_line(text)}\n⏳ Làm mới sau: **{t//60} phút : {t%60:02d} giây**"
        )

    elif text in THOI_TIET:
        ten, emoji, bt, npc = THOI_TIET[text]
        last_report[text] = now
        add_top("thoi_tiet")
        embed = make_embed(
            "🌦️ THỜI TIẾT KAIA",
            npc,
            emoji,
            f"{emoji} **{ten}**\nXuất hiện biến thể: **[{bt}]**\n\n💬 {npc_line(text)}"
        )
    else:
        return

    await channel.send(f"<@&{ROLE_NONG_DAN_ID}>")
    await channel.send(embed=embed)

@bot.command()
async def topweek(ctx):
    data = load_top()
    msg = ""
    for loai, npc in [("nong_san", "Yeongman"), ("thoi_tiet", "Tiến Sĩ Brown"), ("cong_cu", "Lena")]:
        top3 = sorted(data[loai].items(), key=lambda x: x[1], reverse=True)[:3]
        msg += f"\n**🏆 TOP TUẦN {loai.upper()}**\n"
        for i, (uid, c) in enumerate(top3, 1):
            user = await bot.fetch_user(int(uid))
            msg += f"{i}. {user.name} ({c} lần)\n"
    await ctx.send(msg)

@bot.event
async def on_ready():
    print("✅ BOT KAIA ONLINE")

bot.run(TOKEN)
