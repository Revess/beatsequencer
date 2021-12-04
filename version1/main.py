import pygame as pg
import time as t

pg.mixer.init()
pg.init()

kick = pg.mixer.Sound("./samples/k.wav")
snare = pg.mixer.Sound("./samples/s.wav")
hat = pg.mixer.Sound("./samples/h.wav")

pg.mixer.set_num_channels(128)

def readSequence():
    kickScroll = []
    snareScroll = []
    hatScroll = []
    with open("./sequence.txt","r") as f:
        text = f.read().split("\n")
        speed = 60/int(text[0].split(";")[1].split()[0])
        for instrument in text[1:]:
            instrument = instrument.split(";")
            notes = []
            for index,note in enumerate(instrument[1].split()):
                if int(note) == 1:
                    notes.append((index/4)*speed)
            notes.append(float("inf"))
            if instrument[0] == "k":
                kickScroll = notes
            elif instrument[0] == "s":
                snareScroll = notes
            elif instrument[0] == "h":
                hatScroll = notes
    return kickScroll,snareScroll,hatScroll, speed*4

kickScroll,snareScroll,hatScroll,maxLength = readSequence()
start = t.time()

while True:
    currentTime = t.time()
    if currentTime - start >= kickScroll[0]:
        kickScroll.pop(0)
        kick.play()
    if currentTime - start >= snareScroll[0]:
        snareScroll.pop(0)
        snare.play()
    if currentTime - start >= hatScroll[0]:
        hatScroll.pop(0)
        hat.play()
    if len(snareScroll) == 1 and len(kickScroll) == 1 and len(hatScroll) == 1 and currentTime - start >= maxLength:
        kickScroll,snareScroll,hatScroll,maxLength = readSequence()
        start = t.time()