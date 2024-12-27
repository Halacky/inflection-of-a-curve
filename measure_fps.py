import gi
import time
import threading
import sqlite3
from datetime import datetime

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
from gi.repository import Gst, GObject

# Инициализация GStreamer
Gst.init(None)

# Глобальные переменные
frame_count = [0, 0, 0]  # Счетчики кадров для трех камер
lock = threading.Lock()  # Для синхронизации между потоками

# Функция для подсчета кадров
def frame_counter_probe(pad, info, camera_id):
    global frame_count
    with lock:
        frame_count[camera_id] += 1
    return Gst.PadProbeReturn.OK

# Таймер для сбора данных каждые 5 секунд
def calculate_average():
    global frame_count
    while True:
        time.sleep(5)
        with lock:
            avg_frames = frame_count[:]
            frame_count = [0, 0, 0]

        # Запись в файл
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("frame_counts.csv", "a") as file:
            file.write(f"{timestamp}, {avg_frames[0]}, {avg_frames[1]}, {avg_frames[2]}\n")

        # Запись в базу данных
        conn = sqlite3.connect('frame_counts.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO frame_data (timestamp, camera1, camera2, camera3) VALUES (?, ?, ?, ?)",
            (timestamp, avg_frames[0], avg_frames[1], avg_frames[2])
        )
        conn.commit()
        conn.close()

# Настройка пайплайна DeepStream
def create_pipeline():
    pipeline = Gst.Pipeline.new("frame-count-pipeline")

    # Источники RTSP
    uris = [
        "rtsp://camera1/stream",
        "rtsp://camera2/stream",
        "rtsp://camera3/stream"
    ]

    # Создаем элементы
    source_bins = []
    for i, uri in enumerate(uris):
        source = Gst.ElementFactory.make("uridecodebin", f"source-{i}")
        source.set_property("uri", uri)
        source.connect("pad-added", on_pad_added)
        source_bins.append(source)
        pipeline.add(source)

    # Мультиплексор
    streammux = Gst.ElementFactory.make("nvstreammux", "stream-muxer")
    streammux.set_property("width", 1920)
    streammux.set_property("height", 1080)
    streammux.set_property("batch-size", len(uris))
    streammux.set_property("batched-push-timeout", 40000)
    pipeline.add(streammux)

    # Плагин преобразования
    nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "nvvideo-converter")
    pipeline.add(nvvidconv)

    # Подключение выходов
    sink = Gst.ElementFactory.make("fakesink", "sink")
    pipeline.add(sink)

    # Связываем элементы
    for i, source in enumerate(source_bins):
        sink_pad = streammux.get_request_pad(f"sink_{i}")
        src_pad = source.get_static_pad("src")
        src_pad.link(sink_pad)

    streammux.link(nvvidconv)
    nvvidconv.link(sink)

    # Установка обработчиков
    for i in range(len(uris)):
        pad = streammux.get_request_pad(f"sink_{i}")
        pad.add_probe(Gst.PadProbeType.BUFFER, frame_counter_probe, i)

    return pipeline

# Callback для подключения источников
def on_pad_added(src, pad):
    caps = pad.get_current_caps()
    if caps.is_fixed():
        pad.link(src.get_static_pad("sink"))

# Главная функция
def main():
    # Создаем пайплайн
    pipeline = create_pipeline()

    # Настройка базы данных
    conn = sqlite3.connect('frame_counts.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frame_data (
            timestamp TEXT,
            camera1 INTEGER,
            camera2 INTEGER,
            camera3 INTEGER
        )
    """)
    conn.commit()
    conn.close()

    # Запускаем таймер
    threading.Thread(target=calculate_average, daemon=True).start()

    # Запускаем пайплайн
    pipeline.set_state(Gst.State.PLAYING)

    try:
        loop = GObject.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    main()
