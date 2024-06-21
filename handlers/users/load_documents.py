import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot, BASE_PATH_PDF
from entity.database import users
from pkg.Filters import ThereSubscription, AcceptableFileFormat, AllowedLenFile
from pkg.states import UserStates
from service.GetMessage import get_mes, send_mes
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
    path_file = f"{BASE_PATH_PDF}{id}_{message.document.file_name}"
    format_file = message.document.file_name.split('.')[-1]
    if format_file == "doc":
        path_file = f"{BASE_PATH_PDF}{id}_{message.document.file_name}".replace(".doc", ".docx")

    answer, thread_id = await ChatGPT.analysis(path_file=path_file,
                                               user_id=id,
                                               thread_id=user.thread_id)
    user.thread_id = thread_id
    logger.info(f"Get answer: {answer}")
    await send_mes(id, answer)
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
    answer, thread_id = await ChatGPT.question(content=question,
                                               user_id=id,
                                               thread_id=user.thread_id)
    logger.info(f"Get answer: {answer}")
    await send_mes(id, answer)


load_documents_rt = router
