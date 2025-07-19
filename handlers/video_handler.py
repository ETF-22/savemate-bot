
import re, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def get_lang(update: Update):
    user_lang = update.effective_user.language_code
    return "ar" if user_lang.startswith("ar") else "en"

def get_tiktok_video(url):
    headers = { "User-Agent": "Mozilla/5.0" }
    api_url = f"https://ssstik.io/abc?url={url}"
    res = requests.get(api_url, headers=headers)
    matches = re.findall(r'https://[^\"]+?mp4', res.text)
    return matches[0] if matches else None

def get_instagram_video(url):
    try:
        api_url = f"https://igram.io/api/ajaxSearch"
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = f"url={url}"
        res = requests.post(api_url, headers=headers, data=data)
        matches = re.findall(r'https://[^\"]+?mp4', res.text)
        return matches[0] if matches else None
    except:
        return None

def get_twitter_video(url):
    try:
        res = requests.get(url)
        matches = re.findall(r'https://video.twimg.com/[^\"]+?mp4', res.text)
        return matches[0] if matches else None
    except:
        return None

def get_facebook_video(url):
    try:
        headers = { "User-Agent": "Mozilla/5.0" }
        res = requests.get(url, headers=headers)
        matches = re.findall(r'https://[^\"]+?fbcdn[^\"]+?mp4', res.text)
        return matches[0] if matches else None
    except:
        return None

async def handle_video_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    lang = get_lang(update)
    video_url, platform = None, "Unknown"

    if "tiktok.com" in url:
        platform = "TikTok"
        video_url = get_tiktok_video(url)
    elif "instagram.com" in url:
        platform = "Instagram"
        video_url = get_instagram_video(url)
    elif "twitter.com" in url or "x.com" in url:
        platform = "Twitter"
        video_url = get_twitter_video(url)
    elif "facebook.com" in url:
        platform = "Facebook"
        video_url = get_facebook_video(url)

    if video_url:
        button = [[InlineKeyboardButton("📥 Download" if lang == "en" else "📥 تحميل", url=video_url)]]
        reply_markup = InlineKeyboardMarkup(button)
        text = f"✅ {platform} Video Ready!" if lang == "en" else f"✅ فيديو {platform} جاهز!"
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        err = "❌ Failed to download video. Check the link." if lang == "en" else "❌ لم أتمكن من تحميل الفيديو. تأكد من الرابط."
        await update.message.reply_text(err)
