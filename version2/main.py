import pygame as pg
import time as t
import os

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(256)

def readSequence(startBeat=0):
    text = None
    audioTracks = dict()
    speed = 0
    with open("./sequence.txt","r") as f:
        text = f.read().split("\n")
        for line in text:
            line = line.split("; ")
            if line[0] == 'bpm':
                speed = 60/int(line[1])
            if line[0] == 'at':
                notes = []
                for index,note in enumerate(line[2].split()):
                    if int(note) == 1:
                        notes.append(((index+startBeat)/4)*speed) 
                notes.append(float("inf"))
                audioTracks.update({line[1]:[pg.mixer.Sound("./samples/%s.wav" % line[1]),notes]})
        return speed, audioTracks
                
timeStamp = 0
speed,audioTracks = readSequence()
start = t.time()

while True:
    timeDelta = t.time() - start
    fileTime = os.stat("./sequence.txt").st_mtime
    finished = 0
    for audioTrack in audioTracks.values():
        if timeDelta >= audioTrack[1][0]:
            audioTrack[0].play()
            audioTrack[1].pop(0)
        if len(audioTrack[1]) == 1:
            finished+=1
    if finished == len(audioTracks) and timeDelta >= speed*4:
        speed,audioTracks = readSequence()
        start = t.time()
        