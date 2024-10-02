import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ваш токен Telegram бота
TELEGRAM_TOKEN = '8187053611:AAFPOUMsYqS0VEnFgL5HHt9jjdJdv_EaHe4'
# Ваш API ключ Steam
STEAM_API_KEY = '39D4FAC87A9084961BB167B76AE7E4DC'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Рестарт", callback_data='restart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Введите Steam ID пользователя, чтобы получить информацию о профиле.', reply_markup=reply_markup)

async def get_player_info(steam_id: str) -> dict:
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('response', {}).get('players', [{}])[0]
    else:
        return None

def escape_markdown(text: str) -> str:
    """Экранирование специальных символов для MarkdownV2."""
    return (
        text.replace('_', '\\_')
            .replace('*', '\\*')
            .replace('[', '\\[')
            .replace(']', '\\]')
            .replace('(', '\\(')
            .replace(')', '\\)')
            .replace('~', '\\~')
            .replace('>', '\\>')
            .replace('#', '\\#')
            .replace('+', '\\+')
            .replace('-', '\\-')
            .replace('=', '\\=')
            .replace('|', '\\|')
            .replace('{', '\\{')
            .replace('}', '\\}')
            .replace('.', '\\.')
            .replace('!', '\\!')
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    steam_id = update.message.text.strip()
    player_info = await get_player_info(steam_id)

    if player_info and 'steamid' in player_info:
        profile_info = (
            f"*Имя:* {escape_markdown(str(player_info.get('personaname', 'Не указано')))}\n"
            f"*Статус:* {escape_markdown(str(player_info.get('personastate', 'Не указано')))}\n"
            f"*Биография:* {escape_markdown(str(player_info.get('profileurl', 'Не указано')))}\n"
            f"*Местоположение:* {escape_markdown(str(player_info.get('loccountrycode', 'Не указано')))}\n"
            f"*Фото профиля:* {escape_markdown(str(player_info.get('avatarfull', 'Не указано')))}"
        )
        await update.message.reply_text(profile_info, parse_mode='MarkdownV2')
    else:
        await update.message.reply_text('Пользователь не найден. Пожалуйста, проверьте Steam ID.')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'restart':
        await query.edit_message_text(text="Бот перезапущен. Пожалуйста, подождите...")
        # Здесь вы можете добавить логику для реального перезапуска бота.
        # Например, если вы используете Docker или другой процесс-менеджер, вы можете отправить команду на перезапуск.

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
