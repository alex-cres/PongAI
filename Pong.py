import turtle # similar to pygame
from playsound import playsound
import os 
import threading
import random

#sound threading for async sound
def soundPlayer(soundFile):
    threading.Thread(target=playsound, args=(soundFile,), daemon=True).start()
#defining global variables
dir_path = os.path.dirname(os.path.realpath(__file__))
soundFile = dir_path+'\\bounce.wav'
width = 800
height = 600
width_perimeter=width/2-10
height_perimeter=height/2-10
score_base_height=(height/2)-40
randList = [-1,1]
width_limits=[-width_perimeter,width_perimeter]
height_limits=[score_base_height-10,-height_perimeter]
        
color="black"
#defining a screen, title, backgound color, size
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor(color)
wn.setup(width=width,height=height)
#stopping the window from updating immediately
wn.tracer(0)

#Paddle class
class Paddle:
    def __init__(self,controls,starting_width,stretch_wid,stretch_len):
        self.paddle_turtle = turtle.Turtle()
        self.paddle_turtle.st()
        self.paddle_turtle.speed(0) #Animation speed
        self.paddle_turtle.shape("square") # defult 20x20
        self.paddle_turtle.color("white")
        self.paddle_turtle.shapesize(stretch_wid=stretch_wid,stretch_len=stretch_len) # modify the size x times
        self.paddle_turtle.penup()
        self.paddle_turtle.goto(starting_width,0)
        self.starting_width = starting_width
        self.stretch_wid = stretch_wid
        self.stretch_len = stretch_len
        self.controls = controls
    def paddle(self,control):
        y = self.paddle_turtle.ycor()
        #if y + (self.stretch_wid*10) <= width/2 and y - (self.stretch_wid*10) >= -width/2:
        y += 20 if self.controls[0]==control else -20
        self.paddle_turtle.sety(y)
    def key_bind(self):  
        wn.onkeypress(lambda:self.paddle(self.controls[0]),self.controls[0])
        wn.onkeypress(lambda:self.paddle(self.controls[1]),self.controls[1])
    def xcor(self):
        return self.paddle_turtle.xcor()
    def ycor(self):
        return self.paddle_turtle.ycor()
    def collisionYDetection(self,turtle_object):
        return turtle_object.ycor() < self.paddle_turtle.ycor()+((self.stretch_wid)*10) and turtle_object.ycor() > self.paddle_turtle.ycor()-((self.stretch_wid)*10)
    def collisionXDetection(self,turtle_object):
        if self.starting_width <0:
            return turtle_object.xcor() < (self.starting_width+10) and turtle_object.xcor()  > self.starting_width
        else:
            return turtle_object.xcor() > (self.starting_width-10) and turtle_object.xcor()  < self.starting_width
    def afterCollisionXPosition(self):
        if self.starting_width <0:
            return (self.starting_width+10)
        else:
            return (self.starting_width-10)
    def clear(self):
        self.paddle_turtle.ht()

#Score class   
class Score:
    def __init__(self):
        self.pen=turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0,score_base_height)
        self.__score = [0,0]
        self.reWrite()
    def reWrite(self):
        self.pen.clear()
        self.pen.write("Player A: {} Player B: {}".format(self.__score[0],self.__score[1]),align="center",font=("Courier",24,"normal"))
    def scoreUp(self,index):
        self.__score[index]+=1
        return self
    def clear(self):
        self.pen.clear()

#Line 
class Line:
    def __init__(self,base_width,base_height,pen_size=3):
        self.line = turtle.Turtle()
        self.line.setheading(270)
        self.line.hideturtle()
        self.line.speed(0)
        self.line.penup()
        self.line.pensize(pen_size)
        self.line.color("white")
        self.line.goto(base_width,base_height)
        
    def HorizontalToRight(self):
        self.line.setheading(0)
        return self
    def HorizontalToLeft(self):
        self.line.setheading(180)
        return self
    def VerticalToUp(self):
        self.line.setheading(90)
        return self    
    def VerticalToDown(self):
        self.line.setheading(270)
        return self
    def writeDashed(self,size,scalar=1,rep=9):
        for i in range(rep):
            self.line.pendown()
            self.line.forward(size/scalar)
            self.line.penup()
            self.line.forward(size/scalar)
            i=i
        return self
    def writeNormal(self,size):
        self.line.pendown()
        self.line.forward(size)
        self.line.penup()
        return self
    def clear(self):
        self.line.clear()
        
           
     
class Ball:
    def __init__(self,height_perimeter,width_perimeter,soundFile,randList):
        #Ball
        self.ball = turtle.Turtle()
        self.ball.st()
        self.ball.speed(0) #Animation speed
        self.ball.shape("square") # defult 20x20
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0,0)
        self.height_perimeter=height_perimeter
        self.width_perimeter=width_perimeter
        self.soundFile=soundFile
        #move by x pixels every update
        self.ball.dx = 0.1*random.choice(randList)
        self.ball.dy = 0.1*random.choice(randList)
    def setx(self,x):
        self.ball.setx(x)
    def sety(self,y):
        self.ball.sety(y)
    def xcor(self):
        self.ball.xcor()
    def ycor(self):
        self.ball.ycor()
    def moveBall(self):
        self.ball.setx(self.ball.xcor()+self.ball.dx)
        self.ball.sety(self.ball.ycor()+self.ball.dy)
    def checkCollision(self,turtle_object):
        if turtle_object.collisionXDetection(self.ball) and turtle_object.collisionYDetection(self.ball):
            self.ball.setx(turtle_object.afterCollisionXPosition())
            self.ball.dx *=-1
            soundPlayer(self.soundFile)
    def checkWalls(self,score):
        if self.ball.ycor() > self.height_perimeter[1]:
            self.ball.sety(self.height_perimeter[1])
            self.ball.dy *= -1
            soundPlayer(self.soundFile)
        
        if self.ball.ycor() < self.height_perimeter[0]:
            self.ball.sety(self.height_perimeter[0])
            self.ball.dy *= -1
            soundPlayer(self.soundFile)

        if self.ball.xcor() > self.width_perimeter[1]:
            self.ball.goto(0,0)
            self.ball.dx*=-1
            self.ball.dy *= random.choice(randList)
            score.scoreUp(0).reWrite()
            soundPlayer(self.soundFile)

        if self.ball.xcor() < self.width_perimeter[0]:
            self.ball.goto(0,0)
            self.ball.dx*=-1
            self.ball.dy *= random.choice(randList)
            score.scoreUp(1).reWrite() 
            soundPlayer(self.soundFile)
    def clear(self):
        self.ball.ht()


class Game:
    def __init__(self):
        self.isInMenu=True
        self.isInGame=False
        self.menu={}
        self.menu["objects"]=[]
        self.game={}
        self.game["objects"]=[]
    def main(self):
        while self.isInMenu:
            self.startMenu()
            while self.isInGame:
                self.startGame()
        wn.bye()
    def drawMenuTitle(self):
        pen=turtle.Turtle()
        pen.speed(0)
        pen.color("white")
        pen.penup()
        pen.hideturtle()
        pen.goto(0,score_base_height)
        pen.write("Menu",align="center",font=("Courier",24,"normal"))
        return pen
    def drawMenuItem(self,text,height):
        pen=turtle.Turtle()
        pen.speed(0)
        pen.color("white")
        pen.penup()
        pen.hideturtle()
        pen.goto(0,height)
        pen.write(text,align="center",font=("Courier",24,"normal"))
        return pen
    def startMenu(self):
        self.isInMenu=True
        self.menu["objects"].append(self.drawMenuTitle())
        self.menu["objects"].append(Line(width_perimeter,score_base_height-10).writeDashed(height,40,18))
        self.menu["objects"].append(Line(-width_perimeter,score_base_height-10).writeDashed(height,40,18))
        self.menu["objects"].append(Line(-width_perimeter,score_base_height-10,1).HorizontalToRight().writeDashed(width,40,20))
        self.menu["objects"].append(Line(-width_perimeter,-height_perimeter,1).HorizontalToRight().writeDashed(width,40,20))
        self.menu["objects"].append(self.drawMenuItem("   1. Enter Game",score_base_height-score_base_height*5/10))
        self.menu["objects"].append(self.drawMenuItem("Esc. Exit Game",score_base_height-score_base_height*7/10))
        wn.listen()
        wn.onkeypress(lambda:self.exitMenu(),"Escape")
        wn.onkeypress(lambda:self.enterGame(),"1")
        while self.isInMenu:
            wn.update() #updates the screen
    def enterGame(self):
        self.exitMenu()
        self.isInGame=True
    def exitMenu(self):
        self.isInMenu=False
        for i in self.menu["objects"]:
            i.clear()

    def startGame(self):
        #--------------------------#-----------------------------------#
        wn.bgcolor(color)
        wn.setup(width=width,height=height)
        width_perimeter=width/2-10
        height_perimeter=height/2-10
        score_base_height=(height/2)-40
        starting_width_paddles= width/2 -width/16
        width_limits=[-width_perimeter,width_perimeter]
        height_limits=[-height_perimeter,score_base_height-10]
        #--------------------------#-----------------------------------#
        #Init Lines
        self.game["objects"].append(Line(0,score_base_height-10).writeDashed(height,20))
        self.game["objects"].append(Line(width_perimeter,score_base_height-10).writeDashed(height,40,18))
        self.game["objects"].append(Line(-width_perimeter,score_base_height-10).writeDashed(height,40,18))
        self.game["objects"].append(Line(-width_perimeter,score_base_height-10,1).HorizontalToRight().writeDashed(width,40,20))
        self.game["objects"].append(Line(-width_perimeter,-height_perimeter,1).HorizontalToRight().writeDashed(width,40,20))
        
        #Init Paddles
        paddle_a = Paddle(["w","s"],-starting_width_paddles,5,1)
        paddle_b = Paddle(["Up","Down"],+starting_width_paddles,5,1)
        self.game["objects"].append(paddle_a)
        self.game["objects"].append(paddle_b)
        #Init Score 
        score = Score()
        self.game["objects"].append(score)
        #InitBall
        ball = Ball(height_limits,width_limits,soundFile,randList)
        self.game["objects"].append(ball)
        #Keyboard binding
        wn.listen()
        paddle_a.key_bind()
        paddle_b.key_bind()
        wn.onkeypress(lambda:self.exitGame(),"Escape")
        #Main game loop
        while self.isInGame:
            wn.update() #updates the screen
            #Move ball
            ball.moveBall()
            #Border checking
            ball.checkWalls(score)
            #Collision Between ball and the paddles
            ball.checkCollision(paddle_b)
            ball.checkCollision(paddle_a)

    def exitGame(self):
        self.isInGame=False
        self.isInMenu=True
        for i in self.game["objects"]:
            i.clear()




game = Game()
game.main()
    
    
    
