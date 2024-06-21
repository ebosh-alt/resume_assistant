import logging
import time

from openai import OpenAI
from openai.types.beta import CodeInterpreterToolParam
from openai.types.beta.threads.message_create_params import Attachment

from data.config import OPENAI_API_KEY, ASSISTANT

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self):
        self.client = OpenAI()
        self.client.api_key = OPENAI_API_KEY

    def _create_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def _retrieve_thread(self, thread_id):
        thread = self.client.beta.threads.retrieve(thread_id)
        return thread

    def _create_message(self, thread_id, content, file_id=None):
        if file_id:
            attachments = [Attachment(file_id=file_id, tools=[CodeInterpreterToolParam(type="code_interpreter")])]
        else:
            attachments = None
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
            attachments=attachments
        )
        logger.info(f"Created message: {message.id}")
        return message

    def _list_message(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id,
                                                          order="desc")
        logging.info("Listing messages")
        return messages

    def _retrieve_message(self, thread_id, message_id):
        message = self.client.beta.threads.messages.retrieve(
            message_id=thread_id,
            thread_id=message_id,
        )
        return message

    def _create_run(self, thread_id):
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT
        )
        logger.info(f"Created run: {run.id}")
        self._retrieve_run(run, thread_id)
        return run

    def _retrieve_run(self, run, thread_id):
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            logger.info(f"Retrieved run: {run.id}, run status: {run.status}")
            time.sleep(2)

        return run

    def _upload_file(self, file):
        file = self.client.files.create(
            file=file,
            purpose="assistants")
        logger.info(f"Uploaded file: {file.id}")
        return file

    def _list_file(self):
        files = self.client.files.list()
        return files

    def _delete_file(self, file_id):
        self.client.files.delete(file_id)

    @staticmethod
    def _get_text(messages, run_id):
        text = ""
        for message in messages:
            if message.run_id == run_id:
                text = message.content[0].text.value
        return text

    def _del_copy_file(self, file_path):
        list_files = self._list_file()
        file_name = file_path.name.split("/")[-1]
        for i in list_files:
            if i.filename == file_name:
                self._delete_file(i.id)
