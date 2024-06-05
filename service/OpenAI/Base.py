import logging
import time

import openai
from aiogram.enums import ChatAction
from openai.pagination import SyncCursorPage
from openai.types import FileObject
from openai.types.beta import Thread
from openai.types.beta.threads import Run, ThreadMessage

from data.config import OPENAI_API_KEY, ASSISTANT, bot

logger = logging.getLogger(__name__)


class BaseOpenAI:
    def __init__(self):
        self.client = openai
        self.client.api_key = OPENAI_API_KEY

    def _request(self, thread_id: str, content: str) -> Run:
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT,
        )
        return run

    @staticmethod
    def _get_text(messages, run_id) -> str:
        text = ""
        for message in messages:
            if message.assistant_id is None:
                continue
            if message.run_id == run_id:
                text = f"{message.content[0].text.value}"
        return text

    async def _wait_on_run(self, run, thread, user_id: int = None) -> Run:
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            if user_id:
                await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, request_timeout=1.5)
            time.sleep(1.5)
        return run

    def _get_response(self, thread) -> SyncCursorPage[ThreadMessage]:
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

    def _new_threads(self) -> Thread:
        thread = self.client.beta.threads.create()
        logger.info(f"Created new threads: {thread}")
        return thread

    def _load_file(self, file) -> FileObject:
        file = self.client.files.create(
            file=file,
            purpose="assistants")
        return file

    def _add_file(self, id) -> None:
        self.client.beta.assistants.update(
            ASSISTANT,
            tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
            file_ids=[id])
