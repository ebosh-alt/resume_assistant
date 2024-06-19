import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot, BASE_PATH_PDF
from entity.database import users
from pkg.Filters import ThereSubscription, AcceptableFileFormat, AllowedLenFile
from pkg.states import UserStates
from service.GetMessage import get_mes, get_text, rm_symbol_text
from service.OpenAI import ChatGPT

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "load_documents", ThereSubscription())
async def load_documents(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    user = await users.get(id)
    await users.update(user)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("load_documents"))
    await state.set_state(UserStates.communication)


@router.message(F.document, AcceptableFileFormat(), AllowedLenFile(), ThereSubscription(), UserStates.communication)
async def valid_file(message: Message):
    id = message.from_user.id
    user = await users.get(id)
    path_file = f"{BASE_PATH_PDF}{id}_{message.document.file_name}".replace(".doc", ".docx")
    with open(path_file, "rb") as file:
        if user.thread_id is None:
            response, thread_id, vector_store_id = await ChatGPT.get_answer(file=file,
                                                                            user_id=id,
                                                                            content=f"Проанализируй документ {message.document.file_name}")
        else:
            response, thread_id, vector_store_id = await ChatGPT.get_answer(file=file,
                                                                            user_id=id,
                                                                            thread_id=user.thread_id,
                                                                            content=f"Проанализируй документ {message.document.file_name}")
    user.thread_id = thread_id
    user.vector_store_id = vector_store_id
    text = get_text(response)
    logger.info(f"Get text: {text}")
    try:
        if len(text) > 4096:
            count_message = len(text) // 4096
            for i in range(count_message + 1):
                await bot.send_message(chat_id=id,
                                       text=text[i * 4096:(i + 1) * 4096],
                                       parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await bot.send_message(chat_id=id,
                                   text=text,
                                   parse_mode=ParseMode.MARKDOWN_V2)
    except TelegramBadRequest:
        text = rm_symbol_text(response)
        if len(text) > 4096:
            count_message = len(text) // 4096
            for i in range(count_message + 1):
                await bot.send_message(chat_id=id,
                                       text=text[i * 4096:(i + 1) * 4096])
        else:
            await bot.send_message(chat_id=id,
                                   text=text)
    user.count_request += 1
    await users.update(user)


@router.message(F.text, UserStates.communication, ThereSubscription())
async def ask_question(message: Message):
    id = message.from_user.id
    question = message.text
    user = await users.get(id)
    if user.thread_id is None or user.vector_store_id is None:
        return await bot.send_message(chat_id=id,
                                      text="Сначала необходимо загрузить документ")
    response, thread_id, vector_store_id = await ChatGPT.get_answer(content=question,
                                                                    user_id=id,
                                                                    thread_id=user.thread_id,
                                                                    vector_store_id=user.vector_store_id)
    text = get_text(response)
    logger.info(f"Get text: {text}")
    if len(text) > 4096:
        count_message = len(text) % 2
        for i in range(count_message):
            await bot.send_message(chat_id=id,
                                   text=text[i * 4096:(i + 1) * 4096],
                                   parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=id,
                               text=text,
                               parse_mode=ParseMode.MARKDOWN_V2)


load_documents_rt = router
