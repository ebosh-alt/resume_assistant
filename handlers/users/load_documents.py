import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, File

from data.config import bot, BASE_PATH_PDF
from entity.database import users
from pkg.Filters import ThereSubscription, IsPdf
from pkg.states import UserStates
from service.GetMessage import get_mes
from service.OpenAI import ChatGPT

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "load_documents", ThereSubscription())
async def load_documents(msg: Message | CallbackQuery, state: FSMContext):
    id = msg.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=msg.message.message_id,
                                text=get_mes("load_documents"))
    await state.set_state(UserStates.communication)


def download_file(file: File):
    file_path = file.file_path
    destination = r'...data/pdf/'
    destination_file = bot.download_file(file_path, destination)
    logger.info(f"Downloading file -> {destination_file}")


@router.message(F.document, IsPdf(), UserStates.communication)
async def download_file(message: Message, state: FSMContext):
    id = message.from_user.id
    format_file = message.document.file_name.split('.')[-1]
    path_file = f"{BASE_PATH_PDF}{id}_{message.document.file_name}"
    user = await users.get(id)

    await bot.download(
        message.document,
        destination=path_file)

    await state.update_data(path_file=path_file)
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
    await users.update(user)
    try:
        await bot.send_message(chat_id=id,
                               text=response,
                               parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(chat_id=id,
                               text=response)


@router.message(F.text, UserStates.communication)
async def download_file(message: Message):
    id = message.from_user.id
    user = await users.get(id)
    question = message.text
    response, thread_id = await ChatGPT.get_answer(content=question, user_id=id, thread_id=user.thread_id)
    await bot.send_message(chat_id=id,
                           text=response)


@router.message(F.document, UserStates.communication)
async def download_file(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Файл не распознан. Попробуйте ещё раз")


load_documents_rt = router
