import asyncio
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# 🔹 ضع التوكن الصحيح هنا
TOKEN = "8142260456:AAEIpfAujCW6-TJHwc3OCvJO-OY9P-SxAqU"

# ✅ دالة تلخيص المقالات
def summarize_text(text, sentences_count=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        return f"❌ حدث خطأ أثناء التلخيص: {str(e)}"

# ✅ أمر /start
async def start(update: Update, context):
    await update.message.reply_text("👋 مرحبًا! أرسل لي مقالًا وسألخصه لك.")

# ✅ أمر /help
async def help_command(update: Update, context):
    await update.message.reply_text("📌 أرسل نصًا وسألخصه لك.")

# ✅ استقبال النصوص وتلخيصها
async def handle_message(update: Update, context):
    text = update.message.text
    if len(text.split()) < 20:  # التحقق من عدد الكلمات وليس الأحرف
        await update.message.reply_text("⚠️ النص قصير جدًا، أرسل مقالًا أطول.")
    else:
        summary = summarize_text(text)
        await update.message.reply_text(f"📌 التلخيص:\n{summary}")

# ✅ تشغيل البوت
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 البوت يعمل...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
