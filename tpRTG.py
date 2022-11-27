from cmu_112_graphics import *
import time, tpRTGMain, tpLeaderboard, random, math


appWidth = 1200
appHeight = 900
unit = 1200 / 100 # appWidth / 100
seconds = time.time()
state = False

def stateChange():
    runApp(width = 900, height = 675)

# collision detection algorithm
# rectangle intersection detection algorithm
def rangeIntersect(min0, max0, min1, max1):
    return (max(min0, max0) >= min(min1, max1) and
            min(min0, max0) <= max(min1, max1))
    
def rectIntersect(r0, r1):
    return (rangeIntersect(r0.x, r0.x + r0.width, r1.x, r1.x + r1.width) and
            rangeIntersect(r0.y, r0.y + r0.height, r1.y, r1.y + r1.height))

class Rect():
    def __init__(self, x, y, width, height, color = "white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def appStarted(app):
    app.vy = 0
    app.vx = 0
    # gravitational acceleration
    app.a = -6
    app.state = 0
    # jumping state
    app.jumping = False
    # game state
    app.isGameOver = False
    # app.r0 is floor(lava)
    app.r0 = Rect(0, appHeight * 4 / 5, appWidth * 2, appHeight, "red")
    # app.r1 is initial block
    app.r1 = Rect(unit, unit * random.randint(10, 30), appWidth / 65, appHeight / 100, "green")
    # character rectangle
    app.rChar = Rect(0, app.r1.y - 30, 30, 30, "white")
    
    # low tiles
    app.r2 = Rect(unit * 4, app.r1.y + unit * random.randint(-1, 3), appWidth / 65, appHeight / 65, "green")
    app.r3 = Rect(unit * 10, app.r2.y + unit * random.randint(2, 5), appWidth / 65, appHeight / 100, "green")
    app.r4 = Rect(unit * 16, app.r3.y + unit * random.randint(0, 5), appWidth / 65, appHeight / 100, "green")
    app.r5 = Rect(unit * 20, app.r4.y + unit * random.randint(-2, 10), appWidth / 65, appHeight / 100, "green")
    app.r6 = Rect(unit * 24, app.r5.y + unit * random.randint(-1, 10), appWidth / 10, appHeight / 100, "green")
    app.r7 = Rect(unit * 35, random.randint(app.r6.y, app.r0.y - 10), appWidth / 65, appHeight / 100, "green")
    app.r8 = Rect(unit * 42, random.randint(app.r7.y, app.r0.y - 5), appWidth / 20, appHeight / 100, "black")

    # high tiles
    app.r15 = Rect(unit * 47, app.r8.y - random.randint(40, 100), appWidth / 40, appHeight / 100, "green")
    app.r16 = Rect(unit * 51, app.r15.y - random.randint(70, 200), appWidth / 45, appHeight / 100, "green")
    app.r17 = Rect(unit * 55, app.r16.y - random.randint(70, 100), appWidth / 43, appHeight / 100, "green")
    app.r18 = Rect(unit * 60, app.r16.y - random.randint(-50, 100), appWidth / 70, appHeight / 100, "green")
    app.r19 = Rect(unit * 64, unit * 15, appWidth / 43, appHeight / 100, "red")
    app.r20 = Rect(unit * 70, app.r19.y - random.randint(-20, 20), appWidth / 43, appHeight / 100, "green")
    app.r21 = Rect(unit * 74, app.r20.y + random.randint(0, 30), appWidth / 40, appHeight / 100, "green")
    app.r22 = Rect(unit * 79, app.r21.y + random.randint(0, 30), appWidth / 38, appHeight / 100, "green")
    app.r23 = Rect(unit * 82, app.r22.y + random.randint(0, 30), appWidth / 20, appHeight / 100, "green")

    app.rect = [app.r0, app.r1, app.r2, app.r3, app.r4, app.r5, app.r6, app.r7, app.r8,
                app.r15, app.r16, app.r17, app.r18,
                app.r19, app.r20, app.r21, app.r22, app.r23]
    # app.startTime = time.time()
    # app.finalTime = 0
    app.winState = False
    app.currentTime = "00:00"
    # sidescrolling 
    if app.rChar.y > 250:    
        app.scrollY = app.rChar.y - 250
    else:
        app.scrollY = 30
    if app.rChar.x > 400:    
        app.scrollX = app.rChar.x - 400
    else:
        app.scrollX = 0

def anyRectIntersect(app):
    if (app.rChar.x < 0):
        return True
    if (app.rChar.x < 0 or app.rChar.x + app.rChar.width > appWidth or
        app.rChar.y < 0 or app.rChar.y + app.rChar.height > appHeight):
        return True
    for rect in app.rect:
        if rectIntersect(app.rChar, rect):
            return True
    return False
            
def timerFired(app):
    if (app.isGameOver or app.winState) == True:
        return 0
    app.finalTime = time.time()
    
    totalSeconds = int(app.finalTime)
    # extracting minutes
    minutes = totalSeconds // 60
    if minutes < 10:
        mString = f"0{int(minutes)}"
    else:
        mString = f"{int(minutes)}"
    # extracting seconds
    seconds = totalSeconds % 60
    if seconds < 10:
        sString = f"0{int(seconds)}"
    else:
        sString = f"{int(seconds)}"
    app.currentTime = mString + ":" + sString
    
        # game over if character touches lava or ceiling
    if (app.rChar.y + app.rChar.height == app.r0.y - 1) or app.rChar.y == 0:
        app.isGameOver = True
    # wins if character touches the moon
    if ((app.rChar.x + app.rChar.width // 2 - int(unit * 90 + 30))**2 + 
        (app.rChar.y + app.rChar.height // 2 - int(unit * 5 + 30))**2
        <= 30**2):
        record = f"{app.currentTime},user"
        writeFile("leaderboard.txt", record)
        app.winState = True
        
    if app.state == 1:
        motionY(app)
        motionX(app)

    if app.rChar.y > 250:    
        app.scrollY = app.rChar.y - 250
    else:
        app.scrollY = 0
    if app.rChar.x > 400:    
        app.scrollX = app.rChar.x - 400
    else:
        app.scrollX = 0
 
# for debugging purposes: winState testing
def mousePressed(app, event):
    if ((event.x - int(unit * 90 + 30))**2 + (event.y - int(unit * 5 + 30))**2
        <= 30**2):
        app.winState = True
        record = f"{app.currentTime},user"
        currentRec = readFile("leaderboard.txt")
        writeFile("leaderboard.txt", currentRec + record + "\n")
    #     print("win")
    # else:
    #     print((event.x - int(unit * 90) + 30)**2 + (event.y - unit * 5 + 30)**2)
    #     print(event.x - int(unit * 90 + 30), event.y - int(unit * 5 + 30))

# Character's x component of motion
def motionX(app):
    for i in range(abs(app.vx)):
        app.rChar.x += app.vx / abs(app.vx)
        if anyRectIntersect(app):
            app.rChar.x -= app.vx / abs(app.vx)

# Character's y component of motion
def motionY(app):
    if app.vy >= 0:
        for i in range (app.vy):
            app.rChar.y -= 1
            # when hits the ground
            if anyRectIntersect(app):
                app.rChar.y += 1
                app.vx = 0
                app.vy = 0
                # jumping state
                app.jumping = False
                break
    else:
        for i in range (-app.vy):
            app.rChar.y += 1
            # when hits the ground
            if anyRectIntersect(app):
                app.rChar.y -= 1
                app.vx = 0
                app.vy = 0
                # jumping state
                app.jumping = False
                break
    app.vy += app.a

def keyPressed(app, event):
    if (event.key == "Up"):
        # app.scrollY -= 1
        if not (app.isGameOver or app.winState):
            if app.jumping == False:
                # app.jumping = True
                # app.state = 1
                # app.vy = 15
                # motionY(app)
                if app.a <= 0:
                    app.jumping = True
                    app.state = 1
                    app.vy = 15
                    motionY(app)
                if app.a > 0:
                    app.jumping = True
                    app.state = 1
                    app.vy = -15
                    motionY(app)
        
    if (event.key == "Left"):
        # app.scrollX -= 1
        if not (app.isGameOver or app.winState):
            app.vx = -10
            # app.a = 10
            motionX(app)
        
    if (event.key == "Right"):
        # app.scrollX += 1
        if not (app.isGameOver or app.winState):
            app.vx = 10
            motionX(app)
            
    if (event.key == "r"):
        appStarted(app)
        
    if (event.key == "g"):
        if not (app.isGameOver or app.winState):
            app.a *= -1
            motionY(app)
            
    if (event.key == "b"):
        print("importing main")
        tpMain.stateChange()  
        
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "lightgrey")
    for r in app.rect:
        drawRect(app, canvas, r)
    if not app.winState:
        drawRect(app, canvas, app.rChar)
    drawMoon(app, canvas, unit*90, unit*5, 60)
    drawTime(app, canvas)
    drawInstruction(app, canvas)
    drawPhysics(app, canvas)
    if app.isGameOver:
        drawGameOver(app, canvas)
    if app.winState:
        drawWin(app, canvas)
    
    
def drawTime(app, canvas):
    canvas.create_text(app.width / 2, app.height / 7, text = app.currentTime, 
                       fill = "black", font = f"Arial {int(unit * 2)} bold")

def drawMoon(app, canvas, x, y, d):
    canvas.create_oval(x - app.scrollX, y - app.scrollY + app.r1.y - 30, x + d - app.scrollX, y - app.scrollY + d + app.r1.y - 30, fill = "gray", outline = "black",
                       width = 3)
    
def drawRect(app, canvas, r):
    canvas.create_rectangle(r.x - app.scrollX, r.y - app.scrollY + app.r1.y - 30, 
                            r.x - app.scrollX + r.width, r.y - app.scrollY + r.height + app.r1.y - 30, 
                            fill = r.color, outline = "black")
    
def drawGameOver(app, canvas):
    canvas.create_rectangle(app.width / 3, app.height / 3, app.width * 2 / 3,
                            app.height * 2 / 3, fill = "black", outline="red")
    canvas.create_rectangle(app.width/3 + 5, app.height/3 + 5, 
                            app.width * 2/3 - 5, app.height * 2 / 3 - 5,
                            fill = "black", outline="red", width = 5)
    canvas.create_text(app.width / 2, app.height / 2 - unit * 2, text = "GAME OVER :(", 
                       font = f"Times {int(unit*3)} bold", fill = "gold")
    canvas.create_text(app.width / 2, app.height / 2 + unit * 6, text = 
                       "press r to restart", 
                       font = f"Times {int(unit*2)} bold", fill = "gold")

# def drawLeaderboard(app, canvas):
#     canvas.create_rectangle(app.width/3, app.height / 7, app.width * 2 / 3,
#                             app.height * 6 / 7, fill = "white", outline = 
#                             "black")
    
def drawInstruction(app, canvas):
    canvas.create_rectangle(0, 0, unit * 17, unit * 15, outline = "black")
    canvas.create_text(unit * 5, unit * 6, text = 
                       """
                       press "up" to jump
                       press "left" to go left
                       press "right" to go right
                       press "g" to inverse gravity
                       press "r" to restart
                       press "b" to return to main
                       """, 
                       font = f"Arial {int(unit * 5 / 4)} ", fill = "black")

def drawWin(app, canvas):
    canvas.create_rectangle(app.width / 3, app.height / 6, app.width * 2 / 3,
                            app.height * 6 / 7, fill = "gray", outline = 
                            "black")
    canvas.create_rectangle(app.width / 3 + unit, app.height / 6 + unit, 
                            app.width * 2 / 3 - unit, app.height * 6 / 7 - unit, 
                            fill = "black", outline = "gray")
    canvas.create_text(app.width / 2, app.height / 4, text = "YOU ARRIVED!", 
                       font = f"Times {int(unit*4)} bold", fill = "gold")
    canvas.create_text(app.width / 2, app.height / 3, text = f"{app.currentTime}", 
                       font = f"Times {int(unit*2)}", fill = "gold")
    canvas.create_rectangle(app.width / 3 + unit * 2, app.height / 6 + unit * 15, 
                        app.width * 2 / 3 - unit * 2, app.height * 6 / 7 - unit * 2, 
                        fill = "black", outline = "gold")
    canvas.create_text(app.width / 2, app.height / 3 + unit * 4, text = "Leaderboard", 
                       font = f"Times {int(unit*2)}", fill = "gold")
    canvas.create_text(app.width / 2, app.height * 4 / 5, text = "press r to replay", 
                       font = f"Times {int(unit*2)} bold", fill = "gold")
    # canvas.create_rectangle(app.width / 2 - unit * 3, app.height * 5/7 + unit * 5,
    #                         app.width / 2 + unit * 3, app.height * 5/7 + unit * 8,
    #                         fill = "black", outline = "gold")
    canvas.create_text(app.width / 2 - unit * 8, app.height / 3 - unit * 3 + unit * 10, text =
                       tpLeaderboard.boardReturn(), 
                       font = f"Times {int(unit*2)}", fill = "gold", anchor = "nw")
    

def drawPhysics(app, canvas):
    if not app.jumping:
        canvas.create_text(app.width / 2 - unit*3, unit * 13, text = 
                       f"""
                       v={app.vx}i + {0}j
                       g={app.a}
                       """, anchor = "c", fill = "black")
    
    else: 
        canvas.create_text(app.width / 2 - unit*3, unit * 13, text = 
                       f"""
                       v={app.vx}i + {app.vy}j
                       g={app.a}
                       """, anchor = "c", fill = "black")    

if state:
    runApp(width = appWidth, height = appHeight)