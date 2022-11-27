from cmu_112_graphics import *
import time
import tpGame

appWidth = 1200
appHeight = 900
unit = appWidth / 100
seconds = time.time()

def stateChange():
    runApp(width = appWidth, height = appHeight)

def appStarted(app):
    app.counter = 0
    
def redrawAll(app, canvas):
    drawMain(app, canvas)        
        
def drawMain(app, canvas):
    canvas.create_text(app.width / 2, app.height / 5, text = "JUMPING",
                       fill = "black", font = f"Times {int(unit*17)} bold") 
    canvas.create_text(app.width / 2, app.height * 2 / 5, text = "to the",
                       fill = "black", font = f"Times {int(unit*5)} bold")        
    canvas.create_oval(app.width / 2 - unit * 3, app.height * 3 / 5 - unit * 3, 
                       app.width / 2 + unit * 3, app.height * 3 / 5 + unit * 3,
                       fill = "gray", outline = "black",
                       width = int(unit / 2))
    canvas.create_text(app.width / 2, app.height * 4 / 5, text = "(click on the Moon to start)",
                       fill = "black", font = f"Times {int(unit*2)}") 
    

def timerFired(app):
    pass
    
def mousePressed(app, event):
    if ((event.x - app.width / 2)**2 + (event.y - app.height * 3 / 5)**2
        <= (unit * 3)**2):
        # import tpGame 
        tpGame.stateChange()
    
def keyPressed(app, event):
    pass

runApp(width = appWidth, height = appHeight)