import asyncio
import secrets

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from tinydb import TinyDB, Query

from settings import settings



db = TinyDB(settings.PATH_TO_TYNIDB)
User = Query()

bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

@dp.message(Command('start', 'help'))
async def _(m: Message):
    user = db.search(User.user_id == m.from_user.id)
    if user:
        text = user[0]['text']
    else:
        db.insert({'user_id': m.from_user.id, 'text': (text := secrets.token_hex(3))})
    link = f'https://t.me/{settings.TARGET_USERNAME}?text=@{settings.BOT_USERNAME}%20{text}'
    await m.answer(f'Your link is:\n<a href="{link}">{link}</a>', disable_web_page_preview=True)
    
@dp.inline_query()
async def _(q: InlineQuery):
    text = q.query.strip()
    user = db.search(User.text == text)
    if user:
        props = [
            ('User ID: {x}', q.from_user.id),
            ('Username: @{x}', q.from_user.username),
            ('First name: {x}', q.from_user.first_name),
            ('Last name: {x}', q.from_user.last_name),
            ('Language code: {x}', q.from_user.language_code),
            ('Is bot: {x}', q.from_user.is_bot),
            ('Is premium: {x}', q.from_user.is_premium)
        ]
        text = '\n'.join(f.format(x=value) for f, value in filter(lambda x: x[1], props))
        await bot.send_message(user[0]['user_id'], text)

    article = InlineQueryResultArticle(
            id=secrets.token_hex(10),
            title=f'Your ID: {q.from_user.id}',
            input_message_content=InputTextMessageContent(message_text=f'Your ID: {q.from_user.id}')
        )
    await q.answer(article)
    


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
