import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CONFIG ===
BOT_TOKEN = "8361075699:AAGS2iW4eWAcoQ5f9fiL36h5dZ8-TqTVdtk"
ACCESS_PASSWORD = "67459"

# Group IDs
GROUP_IDS = {
    "Physics": -1003059225110,
    "Chemistry": -1003107619933,
    "Math": -1003054961866,
    "Biology": -1002839562079
}

# Track verified users
verified_users = set()

# === FUNCTIONS ===
def get_course_menu():
    keyboard = [
        [InlineKeyboardButton("Physics", callback_data="Physics"),
         InlineKeyboardButton("Chemistry", callback_data="Chemistry")],
        [InlineKeyboardButton("Math", callback_data="Math"),
         InlineKeyboardButton("Biology", callback_data="Biology")],
        [InlineKeyboardButton("Combo Pack", callback_data="Combo"),
         InlineKeyboardButton("Pay Status", callback_data="PayStatus")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in verified_users:
        await update.message.reply_text("Welcome back", reply_markup=get_course_menu())
    else:
        await update.message.reply_text("Enter your password.:")


async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == ACCESS_PASSWORD:
        verified_users.add(update.effective_user.id)
        await update.message.reply_text("Verified! Access granted.", reply_markup=get_course_menu())
    elif update.effective_user.id in verified_users:
        await update.message.reply_text("You’re already verified.", reply_markup=get_course_menu())
    else:
        await update.message.reply_text("Wrong password! Try again.")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in verified_users:
        await query.message.reply_text("Access denied. Please enter password first.")
        return

    course = query.data

    # Normal subjects
    if course in GROUP_IDS:
        group_id = GROUP_IDS[course]

        payment_text = f"""{course} all cycle ACS
কোর্সের দাম: 350 TK

সেন্ড মানি করুন:
বিকাশ পার্সোনাল: 01790768817

সেন্ড মানি করে স্ক্রিনশট দিন।
২৪ ঘন্টার ভিতরে গ্রুপে এড করা হবে।
"""
        await query.message.reply_text(payment_text)

        new_link = await context.bot.create_chat_invite_link(chat_id=group_id, member_limit=1)
        link_text = f"{course} One-Time Join Link:\n{new_link.invite_link}"
        await query.message.reply_text(link_text)

    # Combo Pack
    elif course == "Combo":
        msg1 = """ALL Subjects Combo (HCS + ACS)
কোর্সের দাম: 1000 TK

সেন্ড মানি করুন:
বিকাশ পার্সোনাল: 01790768817

সেন্ড মানি করে স্ক্রিনশট দিন।
২৪ ঘন্টার ভিতরে গ্রুপে এড করা হবে।
"""
        await query.message.reply_text(msg1)

        # create one-time links for all 4 subjects
        links = []
        for sub, gid in GROUP_IDS.items():
            new_link = await context.bot.create_chat_invite_link(chat_id=gid, member_limit=1)
            links.append(f"{sub}:\n{new_link.invite_link}\n")  # blank line between each

        msg2 = "Groups of your Combo Pack:\n\n" + "\n".join(links)
        await query.message.reply_text(msg2)

    # Pay Status
    elif course == "PayStatus":
        await query.message.reply_text("❎ পেমেন্ট নট রিসিভড")
        await query.message.reply_text("✅ পেমেন্ট রিসিভড")

    # Show menu again
    await query.message.reply_text("Choose another option:", reply_markup=get_course_menu())


# === MAIN ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))

    print("Bot is running... Press Ctrl + C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
