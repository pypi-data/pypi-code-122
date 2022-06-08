from multiprocessing import Queue

from neuralspace.transcription.stream import NSStreamer

q = Queue()
streamer = NSStreamer(q)
streamer.start_stream("en", "medical", 23)
while True:
    try:
        print("output :: ", q.get())
    except KeyboardInterrupt:
        exit()
