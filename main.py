#!D:\projects\python_projects\yandex_music_telegram\venv\Scripts\python.exe

import yandex_music
from config import token, api_id, api_hash
import time
import sys
from pyrogram import Client
import traceback

try:
    client = yandex_music.Client(token).init() # подключаемся к апи яндекс музыки
except:
    print("Произошла ошибка подключения к API, проверьте токен на валидность.")
    time.sleep(10)
    sys.exit(0)

exit = True

app = Client("telegram", api_id, api_hash) # подключаемся к телеге
app.start()

bio = app.get_chat("me") # получаем статус, для того чтобы потом его восстановить

def get_music():
    while True:
        queues = client.queues_list()

        last_queue = client.queue(queues[0].id)

        last_track_id = last_queue.get_current_track()
        last_track = last_track_id.fetch_track()

        artists = ', '.join(last_track.artists_name())
        title = last_track.title
        
        print(f"Сейчас играет: {artists} - {title} (Yandex.Music)")
        try:
            app.update_profile(bio=f"Сейчас играет: {artists} - {title} (Yandex.Music)") # меняем статус
        except:
            print("Произошла ошибка, возможно название было слишком длинным, название укорочено.")
            app.update_profile(bio=f"Сейчас играет: {artists} - {title}") # меняем статус

        time.sleep(10)

if __name__ == "__main__":
    try:
        while exit:
            get_music()
    except KeyboardInterrupt:
        if bio.bio == None:
            pass
        else:
            app.update_profile(bio=bio.bio)
        print("Работа остановлена, старый статус восстановлен")
        exit = False
    except Exception as ex:
        if bio.bio == None:
            pass
        else:
            app.update_profile(bio=bio.bio)
        print("Произошла ошибка, работа завершена, старый статус восстановлен: " + traceback.format_exc())
        exit = False