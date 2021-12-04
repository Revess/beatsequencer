import pygame as pg
import time as t
import curses

# screen = curses.initscr()
# screenSize = screen.getmaxyx()
# bpmScreen = curses.newwin(3,round(screenSize[1]/4),0,0)
# sequencerScreen = curses.newwin(screenSize[0]-3,screenSize[1],3,0)
# curses.noecho()
# curses.curs_set(0) 
# curses.cbreak()
# curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
# screen.keypad(True) 
# sequencerScreen.keypad(True) 
# bpmScreen.keypad(True) 
# bpmScreen.nodelay(True)
# sequencerScreen.nodelay(True)
# screen.nodelay(True)

# ##screen loop
# bpmInput = "BPM: "
# event = ""
# while True:
#     ##Clear all##
#     bpmScreen.clear()
#     sequencerScreen.clear()

#     bpmEvent = bpmScreen.getch(1,1)
#     screenEvent = screen.getch()
#     if bpmEvent != -1:
#         event = str(screenEvent == curses.KEY_MOUSE)
#         bpmEvent = chr(bpmEvent)
#         if bpmEvent == 'q':
#             break
#         elif bpmEvent == "\n":
#             bpmInput = "BPM: "
#         elif bpmEvent == "\b":
#             bpmInput = bpmInput[:-1]
#         else:
#             bpmInput+=bpmEvent

#     bpmScreen.addstr(1,1,bpmInput)
#     sequencerScreen.addstr(1,1,str(curses.getmouse()))
#     sequencerScreen.addstr(2,1,event)

#     ##Refresh all##
#     sequencerScreen.box()
#     sequencerScreen.refresh()
#     bpmScreen.box()
#     bpmScreen.refresh()
#     t.sleep(0.01)

# curses.endwin()

def main(screen):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    curses.mousemask(True)
    
    screenSize = screen.getmaxyx()
    bpmScreen = curses.newwin(3,int(screenSize[1]/3),0,0)
    sequencerScreen = curses.newwin(screenSize[0]-3,screenSize[1],3,0)
   
    coordinates = {
        "BPM": [(0,0),bpmScreen.getmaxyx()],
        "SEQ": [(3,0),sequencerScreen.getmaxyx()]
    }
    
    headerNumbers = [10+(int((sequencerScreen.getmaxyx()[1]-10)/16)*index) for index in range(16)]
    tracks = {
        "kick": [[0]*16,[[5,x]for x in headerNumbers]],
        "hat": [[0]*16,[[7,x]for x in headerNumbers]],
        "snare": [[0]*16,[[9,x]for x in headerNumbers]],
        }

    screen.nodelay(True)

    bpmText = "BPM: "
    selectedBox = "BPM"

    bpm = 60
    speed = 60/bpm
    tickIndex = 0
    start = t.time()

    ##the loop##
    while True:
        ##Time based things
        currentTime = t.time() - start

        if currentTime >= (speed/4)*tickIndex:
            tickIndex += 1

        if tickIndex%17 == 0:
            tickIndex = 0
            start = t.time()

        ##Event Handler
        event = screen.getch()
        if event != -1:
            if event == curses.KEY_MOUSE:
                _,x,y,_,_ = curses.getmouse()
                for key,value in coordinates.items():
                    if x >= value[0][1] and x <= value[1][1] and y >= value[0][0] and y <= value[1][0]:
                        selectedBox = key
                if selectedBox == "SEQ":
                    for trackname,track in tracks.items():
                        for coordinate in track[1]:
                            if x >= coordinate[1]+coordinates[selectedBox][0][1]  and x <= coordinate[1]+coordinates[selectedBox][1][1] and x >= coordinate[0]+coordinates[selectedBox][0][0]  and x <= coordinate[0]+coordinates[selectedBox][0][0]:
                                print(trackname)
                                break

            elif event == "\n":
                bpmText = "BPM: "
            elif event == "\b":
                bpmText = bpmText[:-1]
            elif event == 27:
                break

        #Place BPM Elements
        bpmScreen.addstr(1,1,bpmText+str(bpm))

        #Place Sequencer Elements
        sequencerScreen.clear()
            #Trackfeedback
        if tickIndex == 0:
            sequencerScreen.addstr(2,10,"*")
        else:
            sequencerScreen.addstr(2,headerNumbers[tickIndex-1],"*")

            #Print the headers
        for index, x in enumerate(headerNumbers):
            if index%4 == 0:
                sequencerScreen.addstr(3,x,str(int((index)/4)+1))
            else:
                sequencerScreen.addstr(3,x,"|")

            #Print the tracks
        for index, track in enumerate(tracks.items()):
            sequencerScreen.addstr((index*2)+5,1,track[0])
            for number, x in enumerate(headerNumbers):
                sequencerScreen.addstr((index*2)+5,x,str(track[1][0][number]))


        ##Finish the loop
        bpmScreen.box()
        sequencerScreen.box()

        bpmScreen.refresh()
        sequencerScreen.refresh()
        screen.refresh()

curses.wrapper(main)