import logging

from aiogram.enums import ChatAction

from data.config import bot
from entity.database import users
from service.OpenAI.Base import BaseOpenAI

logger = logging.getLogger(__name__)


### векторное хранилище нужно создавать под каждый файл

class ClientOpenAI(BaseOpenAI):
    async def get_answer(self, user_id, content: str, file=None, thread_id=None) -> tuple[
                                                                                                        str, str, str]:
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        if thread_id is None:
            thread = self._new_threads()
            vector_store_id = self._create_vector_store(user_id)
        else:
            thread = self.client.beta.threads.retrieve(thread_id=thread_id)
            vector_store_id = self._create_vector_store(user_id)
            logger.info(f"Getting threads: {thread}")
        if file is not None:
            self._load_file(file, vector_store_id)
            self._add_file(vector_store_id)

        run = self._request(thread_id=thread.id, content=content)
        await self._wait_on_run(run, thread, user_id)
        return self._get_text(self._get_response(thread), run.id), thread.id, vector_store_id
