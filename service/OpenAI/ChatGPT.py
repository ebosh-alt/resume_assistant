from service.OpenAI.Base import BaseClient


class Client(BaseClient):
    def analysis(self, file_path, thread_id=None):
        if not thread_id:
            thread = self._create_thread()
            thread_id = thread.id
        with open(file_path, "rb") as f:
            file = self._upload_file(f)
            self._create_message(thread_id=thread_id,
                                 content=f"Проанализируй документ. В начале пиши название файла",
                                 file_id=file.id)
        return self.__answer(thread_id), thread_id

    def question(self, content, thread_id=None):
        if not thread_id:
            thread = self._create_thread()
            thread_id = thread.id
        self._create_message(thread_id=thread_id,
                             content=content)
        return self.__answer(thread_id), thread_id

    def __answer(self, thread_id):
        run = self._create_run(thread_id)
        messages = self._list_message(thread_id)
        text = self._get_text(messages, run.id)

        return text
