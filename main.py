import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI 
from cfg import Settings


bot = Bot(token=Settings.TOKEN)
dp = Dispatcher()

client = OpenAI(
    api_key=Settings.API_KEY_AI,
    base_url=Settings.BASE_URL,
    )


async def get_ai_response(prompt: str) -> str:
    try:
        full_prompt = f"""
        Ты - русскоязычный ассистент. Всегда отвечай на русском даже если вопрос задан на другом языке. Если вопрос не на русском, переведи его на русский перед ответом
        Вопрос: {prompt}
        """
        response = await asyncio.to_thread(
            client.chat.completions.create,
            messages=[
                {"role": "system", "content": "Ты - ИИ помошник по любому вопросу"},
                {"role": "user", "content": full_prompt}
            ],
            model=Settings.MODEL,
            max_tokens=5000,
            temperature=0.7
        )

        return response.choices[0].message.content
    
    except Exception as e:
        logging.error(f'error{e}')
        return "Извините, не можем обраюотать ваш запрос"


@dp.message(Command("start"))
async def start_bot(msg: Message):
    await msg.answer("Hello")


@dp.message(Command("image"))
async def handle_image(msg: Message):
    prompt = msg.text[len("/image "):].strip()
    if not prompt:
        await msg.answer("Напишите описание картинки после команды. Например:/image кот в космосе")
        return 
        
     await msg.answer("⏳ Генерирую изображение, подождите...")
    image_path = await generate_image(prompt)

    if image_path:
        await msg.answer_photo(FSInputFile(image_path))
        os.remove(image_path)  
    else:
        await msg.answer("Не удалось сгенерировать изображение.")


@dp.message(Command('help'))
async def help_info(msg: Message):
    await msg.answer("Я вижу что ты просишь у меня помощь ну и раз так давай расскажу. Я русский Chat-GPT готов помочь тебе ответить почти на все твои вопросы , а также развлечь тебя")
    


@dp.message()
async def  handler_msg(msg: Message):
    user_msg = msg.text
    if not user_msg:
        await msg.answer('Пожалуйста пришлите текстовое сообщение...')
        return
    try:
        ai_response = await get_ai_response(user_msg)
        await msg.answer(ai_response)
    except Exception as e:
        logging.error(f"Error in message handling: {e}")
        await msg.answer("Произошла ошибка при обработке вашего запроса")
    
    

async def main ():
    logging.basicConfig(level=logging.INFO)
    logging.info("Start Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())