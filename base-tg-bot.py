import logging
import re  # хуйня ты ебанная чтоб тебя медведь сьел
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
    await update.message.reply_text('Привет! Вам нужно ввести ссылку на профиль стим, а я пришлю вам статистику данного пользователя.',
                                    reply_markup=reply_markup)


def extract_steam_id(profile_url: str) -> str:
    """функция для извлечения Steam ID из полученной ссылки"""
    # проверка, содержит ли ссылка /profiles/ и извлечение ID
    match_profiles = re.search(r'steamcommunity\.com/profiles/(\d+)', profile_url)
    if match_profiles:
        return match_profiles.group(1)

    # проверка, на содержание в ссылке /id/ и извлечение кастом URL
    match_id = re.search(r'steamcommunity\.com/id/([\w\d]+)', profile_url)
    if match_id:
        return match_id.group(1)

    return None


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


async def resolve_vanity_url(vanity_url: str) -> str:
    """формат кастом URL в Steam ID с помощью API"""
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_url}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json().get('response', {})
        if result.get('success') == 1:
            return result.get('steamid')
        else:
            return None
    else:
        return None


def escape_markdown(text: str) -> str:
    """экранирование спец символов для MarkdownV2."""
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
    """Конвертация времени в формат 'часы-минуты'."""
    if minutes == 0:
        return "0 ч"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours > 0:
        return f"{hours} ч {remaining_minutes} мин"
    else:
        return f"{remaining_minutes} мин"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ПОлучение текста сообщения
    profile_url = update.message.text.strip()

    # Извлечения Steam ID или кастом URL
    extracted_id = extract_steam_id(profile_url)

    # КОнвертатор кастом URL в steam ID
    if extracted_id and not extracted_id.isdigit():
        steam_id = await resolve_vanity_url(extracted_id)
        if not steam_id:
            await update.message.reply_text('Не удалось найти Steam ID по вашей информации. Проверьте корректность и работоспособность ссылки.')
            return
    else:
        steam_id = extracted_id

    if steam_id:
        player_info = await get_player_info(steam_id)
        steam_level = await get_steam_level(steam_id)

        if player_info and 'steamid' in player_info:
            recently_played_games = await get_recently_played_games(steam_id)

            # Конвертация времени для каждой игры, всего отобразится 5
            games_list = "\n".join([f"• {escape_markdown(game['name'])} (Время: {convert_playtime(game['playtime_forever'])})" for game in recently_played_games]) or "Нет недавно запущенных игр."

            # Проверка на корректность URL аватарки
            avatar_url = player_info.get('avatarfull')
            if avatar_url and avatar_url.startswith(('http://', 'https://')):
                avatar_display = f'<a href="{avatar_url}">Полная аватарка</a>'
            else:
                avatar_display = "Пользователь не установил аватар профиля."

            # Все возможные статусы
            personastate = player_info.get('personastate', 0)
            status_map = {
                0: "Не в сети",
                1: "Онлайн",
                2: "Нет на месте",
                3: "Не беспокоить",
                4: "В игре"
            }
            status = status_map.get(personastate, "Текущий статус неизвестен")

            profile_info = (
                f"<b>Имя аккаунта:</b> {escape_markdown(player_info.get('personaname', 'Отсутствует'))}\n"
                f"<b>Уровень аккаунта:</b> {steam_level}\n"
                f"<b>Статус профиля:</b> {status}\n"
                f"<b>Фото профиля:</b> {avatar_display}\n"
                f"<b>Список недавно запущенных игр:</b>\n{games_list}"
            )

            await update.message.reply_text(profile_info, parse_mode=ParseMode.HTML)

        else:
            await update.message.reply_text('Не удалось получить данные по этой ссылке. Пожалуйста, проверьте ссылку.')
    else:
        await update.message.reply_text('Пожалуйста, предоставьте корректную ссылку на Steam профиль.')


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Я вас не понимаю. Укажите действующую ссылку на Steam профиль.')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()
