import asyncio
import logging
import time
from contextlib import suppress

import openai
from aiogram.enums import ChatAction
from openai.pagination import SyncCursorPage
from openai.types import FileObject
from openai.types.beta import Thread
import threading
from data.config import OPENAI_API_KEY, ASSISTANT, bot


async def main():
    task = asyncio.create_task(start())
    await task


def get_text(text: str) -> str:
    text = text.replace("_", r"_")
    text = text.replace("{", r"{")
    text = text.replace("}", r"\}")
    text = text.replace("[", r"\[")
    text = text.replace("]", r"\]")
    text = text.replace("<", r"\<")
    text = text.replace(">", r"\>")
    text = text.replace("(", r"\(")
    text = text.replace(")", r"\)")
    text = text.replace("#", "")
    text = text.replace("+", r"\+")
    text = text.replace("-", r"\-")
    text = text.replace(".", r"\.")
    text = text.replace("!", r"\!")
    text = text.replace("|", r"\|")
    text = text.replace("**", "*")
    return text


class BaseOpenAI:
    def __init__(self):
        self.client = openai
        self.client.api_key = OPENAI_API_KEY

    def _request(self, thread_id: str, content: str):
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

    def _wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(1)
        return run

    def _get_response(self, thread):
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

    def new_threads(self) -> Thread:
        thread = self.client.beta.threads.create()
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


class ClientOpenAI(BaseOpenAI):
    def get_answer(self, content: str, file=None, thread_id=None):
        # await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        if thread_id is None:
            thread = self.new_threads()
        else:
            thread = self.client.beta.threads.retrieve(thread_id=thread_id)
        if file is not None:
            file_load = self._load_file(file)
            self._add_file(file_load.id)
        run = self._request(thread_id=thread.id, content=content)
        self._wait_on_run(run, thread)
        return self._get_text(self._get_response(thread), run.id)


def test(path_file, thread_id, count):
    ev.wait()
    now_2 = time.time()

    # thread_id = "thread_GvqLtvLdKAEMTB4MzuvRj0qC"
    with open(path_file, "rb") as file:
        response = ClientOpenAI().get_answer(file=file,
                                             thread_id=thread_id,
                                             content="Проанализируй документ")
        text = get_text(response)
        print(f"Выполнено {count + 1} запросов. Время выполнения {time.time() - now_2}")

        logger.info(text)


ev = threading.Event()


async def start():
    paths = ["/projects/resume_assistant/data/pdf/primer8.pdf",
             "/projects/resume_assistant/data/pdf/primer9.pdf",
             "/projects/resume_assistant/data/pdf/Долгих Станислав Андреевич.pdf"]
    threads_ai = ['thread_NjdntzZlMQ62CttYvRdxQppF', 'thread_vAEeE3dDWYAsHFbhMXmx3s1U',
                  'thread_OvCMJhRbAWmR0yJli1ZXi98x', 'thread_5dzvvWDU8EP0hB7lcI2v29WZ',
                  'thread_hVgj0xn6bK8GMrD2DHWsLQKW', 'thread_tZPRZ7jgCOsD83fiHDG6HoAP',
                  'thread_Jx2hovDAfR74ws9DH6kIuzKD', 'thread_m4Et56YULAZ4QSUlUXHRVue8',
                  'thread_xl03GltGPfyS2F0vjhiKG8yL', 'thread_9BMxKeVteRj17c7R8hOPExyS',
                  'thread_wqooCpv4T8nI4dxhuwvwI173', 'thread_x0zoj2SFFSDyzOpfy6yJMLN9',
                  'thread_fiyr8IepSqxVDpIqOwkbWDPT', 'thread_XZSuNegWU3v6bHnI67ju3lHk',
                  'thread_QMGMQNqYhLAuZcmdktMCvXgb', 'thread_MZ9LHWB7OkRME91KeuioJBVC',
                  'thread_TQIsuZsZVUm6Unu872oPeqJs', 'thread_mWf024pPnhYiaMeWrzDOcxX1',
                  'thread_Y0XQaTcBFkCKYUj5QKFoZn7s', 'thread_A1ecqRhlBeLNL5lqq1eCIPzi',
                  'thread_QDHkjQ3OaXk05kkclHCgXFsb', 'thread_8PpIMdq66Y2qXL8FvBN9laD0',
                  'thread_LGjq5Px5Q4PeIZWfwZE61FWo', 'thread_gr1Dsmz6TOFFW0t5LC0evyYf',
                  'thread_AwrfFD6OUWysnuOORcNBWu6e', 'thread_Uh4eMM4Wi4fxdYnqrbswZVzR',
                  'thread_gqoeCMZBIyXtx0QC6XoowDud', 'thread_v1JDgEh6bBA5iThj5jSj561P',
                  'thread_u3mFunQNkWr4z5n6XxvvPSDk', 'thread_by70IK4BccMvXcRgNsiMHmXs',
                  'thread_p9CLVrbkMmr7cDyFausB9JBy', 'thread_ZqZT94pjD6ckdYEgdRoPSmSp',
                  'thread_umpGmXMHvoQyBEb9POaQqFpW', 'thread_ZtTOu03ZesJ6otn1qBcmsrtb',
                  'thread_n1oEKrk8fhcacI13enCs5D2e', 'thread_fT8xS5DJ9KkAZaT5HKLrLkjz',
                  'thread_dHILCbR1YYFrlkDDBERYZVE7', 'thread_TLMJydosEgVghLmlqyBK1bMW',
                  'thread_Xjf5BYU5tvNccOd8Zq9hZ9Ir', 'thread_N9HpAySQ5X0ernOR5AQr24iV',
                  'thread_JLE6pSMfWDnobYKGihHPTeq0', 'thread_rvp4fAww2TrUP4YC4fURltek',
                  'thread_T8HrKOU5ozwQUjJAqPZL5r2S', 'thread_f37Zo6EIkUHF8Kr30mIzqBE1',
                  'thread_DTIydlJwnPVoJwYJVDeufBrb', 'thread_wK7w073eMrbLmGjp1lg7sIaj',
                  'thread_YVvvNzmLnhlOdMUz5muYQN0j', 'thread_OmgEUP1XSIrnEGhTgF5GpEHd',
                  'thread_JvjdCWxDuaVZX4BA2U6BS3Qv', 'thread_uanJ6eW1T8PDa9doDhUO5Qug',
                  'thread_uTBNGbJhvphmQ2mLDoAtQUbS', 'thread_fJAUlNKPg2Jr8sJEWdkS2Q6e',
                  'thread_GMCD5RWgEZfndwenR8alRgeA', 'thread_hoKub3IdTMzxvJzElzWWveeg',
                  'thread_lNb00kR1x92AayhFG9sKhw85', 'thread_m6eVzqprNipba6Vh8SMIp407',
                  'thread_VkLWu17W1sQycJqXPWvGWOr4', 'thread_eknmGP35YaJu6bXoDF3urMsA',
                  'thread_VDoWMNkofJ0fKKuteOnhwXye', 'thread_azfS4kmvM7DEJ4UCCfV0TVCz',
                  'thread_ijkc5FNhVi8mYaO9zOAsbpFm', 'thread_0uIfFY0pOw2gBPJ5IdizPwv4',
                  'thread_jAD3uEtF1VbbLeAjW9UN5xgR', 'thread_p0phQ06yVnQ8DQ9UVlPVvGH0',
                  'thread_Xkm5jvOOgIT1Wi2QNnrbURxj', 'thread_p85Hrqb6nwZzNJ8CbS48ziMg',
                  'thread_vJagBX2pw0ffrXidmvK8scnv', 'thread_7pWgLCkYSozjjdcQMYL5b2W5',
                  'thread_11tQwkpdOXMJTuMwu9IFkc2S', 'thread_cq9BWIVSvW7utmMEs1nLz341',
                  'thread_51hM5BFFBvVgOPLOQbIAh9wR', 'thread_PDdxSuGAyzLLSRJGc1q8n05e',
                  'thread_FPbvF7Nv7jZxSYQYoUtVRVlk', 'thread_LHS6LDbaHytzKGUbBurxlu4j',
                  'thread_ckft2JIuSPLpqJvD23h3FYdN', 'thread_Wpvr1OCS5mNxSr4Q8r8ZnUed',
                  'thread_cE12TnjpgNr5hbeZdpwBNroy', 'thread_486YLTOvEqzqNZeV47Bm8Lrr',
                  'thread_EqVoUm9rZoesDxl2Ap7s4QSa', 'thread_AJILlFHKYFH96V6v3vj7ZpIC',
                  'thread_yQqYMlL7u0o8uuIky5JNcY6Y', 'thread_rMRC6YC1CCyhzhNiKfu7bF2k',
                  'thread_C0hyBMT7DemVrWYs1JRO3iU5', 'thread_ShEVfQgWorqxphvub6SWQlI6',
                  'thread_KiBRZpqMJEQGawBCedQEgGkv', 'thread_4wGTrQTmeWqjDE5gKuUVOIUd',
                  'thread_nBDD9BvpkLBYi6o0sQEeH0ME', 'thread_KQ9CqLN6HAiqPrla8GlNBHrV',
                  'thread_q2mT9oN2krs5OBMUspSuGDgM', 'thread_cA3nZMN48dYgKCXMkYx1atqr',
                  'thread_YyKYEcXCnpooH4sj0Zdu8Fc7', 'thread_wPXZaXjLSCGdo9tr4tR5zNRr',
                  'thread_h2nKa6D1SUOgGIor5kicknYF', 'thread_ZGK9BHOckRLw0QYTx7L39UV3',
                  'thread_axffcD63YsYrQ58u4IoXVqMm', 'thread_Vozlwag2V6qO4UstPnrjPH2P',
                  'thread_o83W0jURNozRdExuEjA39JYI', 'thread_90PuvszwvqQyyyDODAmzeVqq',
                  'thread_iS80vg2XvBbcpZov0hjk0yXs', 'thread_NZK95pUzXE6kgPkZzTfaN7JH']

    count = 0
    now = time.time()
    data = []
    for i in range(0, 100):
        data.append(
            threading.Thread(target=test, kwargs={"path_file": paths[count], "thread_id": threads_ai[i], "count": i}))
        count += 1
        if count == 3:
            count = 2
    count = 1
    for thread in data:
        ev.clear()
        thread.start()
        time.sleep(5)
        ev.set()
        count += 1

    print(time.time() - now)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="stress.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
"""
100 запросов с промежутком запуска в 10 секунд прошли успешно, время выполнения: 1000.098965883255
100 запросов с промежутком запуска в 5 секунд прошли успешно, время выполнения: 500.0737955570221
Время ответа в обоих случаях схожи, вальируется от 9 до 57 секунд
Такой разброс происходит из-за загрузки процессора потокоми(для теста я использовал threading), в боте же ответ будет калибаться от 9 до 30 секунд
Иногда выдавал пустой ответ, но сами запросы все обрабатывал
"""
