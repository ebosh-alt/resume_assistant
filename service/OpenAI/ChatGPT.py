import logging

from service.OpenAI.Base import BaseClient

logger = logging.getLogger(__name__)


class Client(BaseClient):
    async def analysis(self, path_file, vector_store_id, thread_id, user_id=None):
        with open(path_file, "rb") as f:
            self._del_copy_file(path_file=path_file, vector_store_id=vector_store_id)
            file = self._upload_file(f)
            # files = self._list_files()
            self._create_vector_store_file(vector_store_id=vector_store_id,
                                           file_id=file.id)
            self._create_message(thread_id=thread_id,
                                 content=f"Проанализируй документ."
                                         f"Ответь на файл {file.filename} и id {file.id}, это очень важно иначе работособность проекта сильно понизиться.",
                                 file_id=file.id)
        return await self.__answer(thread_id, user_id)

    async def question(self, content, thread_id=None, user_id=None):
        self._create_message(thread_id=thread_id,
                             content=content + ". В начале пиши id файла")
        return await self.__answer(thread_id, user_id)

    async def __answer(self, thread_id, user_id):
        run = await self._create_run(thread_id, user_id)
        if type(run) is str:
            return run
        messages = self._list_message(thread_id)
        text = self._get_text(messages, run.id)
        return text

    def create_vector_store(self, user_id):
        return self._create_vector_store(user_id)

    def create_thread(self):
        return self._create_thread()

    def test(self):
        vector_stores = self.client.beta.vector_stores.list()
        count = 0
        # for vector_store in vector_stores:
        #     count += 1
        # print(count)
        count = 0
        # print(self._list_files())
        for vector_store in vector_stores:
            self.client.beta.vector_stores.delete(
                vector_store_id=vector_store.id
            )


if __name__ == '__main__':
    client = Client()
    client.test()
