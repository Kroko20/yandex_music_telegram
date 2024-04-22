import yandex_music
from config import token
from threading import Thread
import time
import sys

try:
    client = yandex_music.Client(token).init()
except:
    print("Произошла ошибка подключения к API, проверьте токен на валидность.")
    sys.exit(0)

exit = True

def get_music():
    while True:
        queues = client.queues_list()

        last_queue = client.queue(queues[0].id)

        last_track_id = last_queue.get_current_track()
        last_track = last_track_id.fetch_track()

        artists = ', '.join(last_track.artists_name())
        title = last_track.title

        print(f"Сейчас играет: {artists} - {title} (Yandex.Music)")
        time.sleep(10)

if __name__ == "__main__":
    try:
        while True:
            get_music()
    except KeyboardInterrupt:
        print("Работа остановлена")
        true = False