import asyncio
import logging
import time

from openai import OpenAI
from aiogram.enums import ChatAction
from openai.pagination import SyncCursorPage
from openai.types.beta import Thread
from openai.types.beta.threads import Run, Message

from data.config import OPENAI_API_KEY, ASSISTANT, bot

logger = logging.getLogger(__name__)


class BaseOpenAI:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def _request(self, thread_id: str, content: str) -> Run:
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=ASSISTANT,
        )
        return run

    @staticmethod
    def _get_text(messages: SyncCursorPage[Message], run_id) -> str:
        text = ""
        for message in messages:
            if message.assistant_id is None:
                continue
            if message.run_id == run_id:
                text = f"{message.content[0].text.value}"
        return text

    async def _wait_on_run(self, run, thread, user_id: int = None) -> Run:
        print(user_id)
        # while run.status != "complete":
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            if user_id is not None:
                logger.info(user_id)
                await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, request_timeout=3)
            time.sleep(3)
        return run

    def _create_vector_store(self, user_id: int):
        vector_store = self.client.beta.vector_stores.create(name=str(user_id))
        return vector_store.id

    def _get_response(self, thread) -> SyncCursorPage[Message]:
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

    def _new_threads(self) -> Thread:
        thread = self.client.beta.threads.create()
        logger.info(f"Created new threads: {thread}")
        return thread

    def _load_file(self, file_streams, vector_store_id: str):
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=[file_streams]
        )
        logger.info(f"Upload {file_streams}. Status: {file_batch.status}")

    def _add_file(self, vector_store_id) -> None:
        self.client.beta.assistants.update(
            ASSISTANT,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )

    def new_load_file(self, file):
        message_file = self.client.files.create(
            file=file, purpose="assistants"
        )
        return message_file.id
