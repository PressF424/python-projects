import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = '8187053611:AAFPOUMsYqS0VEnFgL5HHt9jjdJdv_EaHe4'
STEAM_API_KEY = '39D4FAC87A9084961BB167B76AE7E4DC'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Рестарт", callback_data='restart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Введите Steam ID пользователя, чтобы получить информацию о профиле.',
                                    reply_markup=reply_markup)


async def get_player_info(steam_id: str) -> dict:
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(url)

    if response.status_code == 200:
        players = response.json().get('response', {}).get('players', [])
        if players:
            return players[0]
        else:
            return None
    else:
        return None


async def get_recently_played_games(steam_id: str) -> list:
    url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&count=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('response', {}).get('games', [])
    else:
        return []
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

async def get_steam_level(steam_id: str) -> int:
    url = f"http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_API_KEY}&steamid={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('response', {}).get('player_level', 0)
    else:
        return 0

def convert_playtime(minutes: int) -> str:
    if minutes == 0:
        return "0 ч"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours > 0:
        return f"{hours} ч {remaining_minutes} мин"
    else:
        return f"{remaining_minutes} мин"


def convert_playtime(minutes: int) -> str:
    """Конвертация времени из минут в формат 'часы минуты'."""
    if minutes == 0:
        return "0 ч"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours > 0:
        return f"{hours} ч {remaining_minutes} мин"
    else:
        return f"{remaining_minutes} мин"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    steam_id = update.message.text.strip()
    player_info = await get_player_info(steam_id)
    steam_level = await get_steam_level(steam_id)

    if player_info and 'steamid' in player_info:
        recently_played_games = await get_recently_played_games(steam_id)

        # конвертация времени для каждой игры
        games_list = "\n".join([f"• {escape_markdown(game['name'])} (Время: {convert_playtime(game['playtime_forever'])})" for game in recently_played_games]) or "Нет недавно запущенных игр."

        # исправленная проверка на корректность URL аватара
        avatar_url = player_info.get('avatarfull')
        if avatar_url and avatar_url.startswith(('http://', 'https://')):
            avatar_display = f'<a href="{avatar_url}">Ссылка на аватар</a>'
        else:
            avatar_display = "Нет доступного аватара."

        # все возможные статусы
        personastate = player_info.get('personastate', 0)
        status_map = {
            0: "Не в сети",
            1: "Онлайн",
            2: "Нет на месте",
            3: "Не беспокоить",
            4: "В игре"
        }
        status = status_map.get(personastate, "Неизвестно")

        profile_info = (
            f"<b>Имя:</b> {escape_markdown(player_info.get('personaname', 'Не указано'))}\n"
            f"<b>Уровень аккаунта:</b> {steam_level}\n"
            f"<b>Статус:</b> {status}\n"
            f"<b>Местоположение:</b> {escape_markdown(str(player_info.get('loccountrycode', 'Не указано')))}\n"
            f"<b>Фото профиля:</b> {avatar_display}\n"
            f"<b>Недавно запущенные игры:</b>\n{games_list}"
        )

        await update.message.reply_text(profile_info, parse_mode=ParseMode.HTML)

    else:
        await update.message.reply_text('Возможно вы ошибились. Пожалуйста, проверьте Steam ID.')




async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Я вас не понимаю. Укажите свой действующий ID.')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()