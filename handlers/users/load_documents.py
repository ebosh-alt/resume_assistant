import logging
import os
import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, File

from data.config import bot, BASE_PATH_PDF, offset, count_free_request
from entity.database import users
from handlers.users.payment import no_sbp
from pkg.Filters import ThereSubscription, IsPdf
from pkg.states import UserStates
from service.GetMessage import get_mes, get_text
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


def download_file(file: File):
    file_path = file.file_path
    destination = r'...data/pdf/'
    destination_file = bot.download_file(file_path, destination)
    logger.info(f"Downloading file -> {destination_file}")


@router.message(F.document, IsPdf(), UserStates.communication, ThereSubscription())
async def download_file(message: Message):
    id = message.from_user.id
    path_file = f"{BASE_PATH_PDF}{id}_{message.document.file_name}"
    user = await users.get(id)
    await bot.download(
        message.document,
        destination=path_file)
    logger.info("Downloaded file")
    with open(path_file, "rb") as file:
        if user.thread_id is None:
            response, thread_id = await ChatGPT.get_answer(file=file,
                                                           user_id=id,
                                                           content="Проанализируй документ")
            user.thread_id = thread_id
        else:
            response, thread_id = await ChatGPT.get_answer(file=file,
                                                           user_id=id,
                                                           thread_id=user.thread_id,
                                                           content="Проанализируй документ")

    text = get_text(response)
    await users.update(user)
    user.count_request += 1
    await users.update(user)
    await bot.send_message(chat_id=id,
                           text=text,
                           parse_mode=ParseMode.MARKDOWN_V2)
    logger.info("Get response: %s", response)

    # os.remove(path_file)


@router.message(F.text, UserStates.communication, ThereSubscription())
async def download_file(message: Message):
    id = message.from_user.id
    user = await users.get(id)
    user.count_request += 1
    await users.update(user)
    question = message.text
    response, thread_id = await ChatGPT.get_answer(content=question, user_id=id, thread_id=user.thread_id)
    text = get_text(response)
    await bot.send_message(chat_id=id,
                           text=text,
                           parse_mode=ParseMode.MARKDOWN_V2)


@router.message(F.document, UserStates.communication)
async def download_file(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Файл не распознан. Попробуйте ещё раз")


load_documents_rt = router
