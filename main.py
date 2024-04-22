import yandex_music
from config import token, api_id, api_hash
from threading import Thread
import time
import sys
from pyrogram import Client

try:
    client = yandex_music.Client(token).init()
except:
    print("Произошла ошибка подключения к API, проверьте токен на валидность.")
    time.sleep(10)
    sys.exit(0)

exit = True

app = Client("telegram", api_id, api_hash)
app.start()

bio = app.get_chat("me")

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
            app.update_profile(bio=f"Сейчас играет: {artists} - {title} (Yandex.Music)")
        except socket.error as e:
            pass
        time.sleep(10)

if __name__ == "__main__":
    try:
        while True:
            get_music()
    except KeyboardInterrupt:
        if bio.bio == None:
            pass
        else:
            app.update_profile(bio=bio.bio)
        print("Работа остановлена, старый статус восстановлен")
        true = False