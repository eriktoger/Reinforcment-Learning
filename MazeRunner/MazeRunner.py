#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 15:06:27 2019

@author: erik
"""

# I had to install python 3.5 for pygame.
# And then spyder 3.2 otherwise some other spyder (2,7 or 3.6 opened and pygame didnt work there) 
import numpy as np
import random
from MazeGame import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, MazeGame
from DynamicProgramming import DP_Solution, GAMMA, LOWER_LIMIT
import time
# import the pygame module, so you can use it
import os
os.environ['PYGAME_FREETYPE'] = '1'
import pygame
import pygame.freetype
# define a main function

# I didnt get apples/bombs to work since it made it dymanic instead of static.
#if I add that if go back to visited square penalize it heavy, maybe it will work
# just save that problem for later.
#Or just basicly two games 1 to find way to apple and one from apple to end

class MazeRunner:
     
    def __init__(self,pygameIn):
    # initialize the pygame module
        self.pygame = pygameIn
        self.pygame.init()
        
        # load and set the logo
        
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        
        self.MAX_Y = 20*32
        self.MAX_X = 16*32
        self.INFO_X = 6*32
        self.INFO_Y = self.MAX_Y
       
        
        #print(self.START_X)
        #print(self.START_Y)
        # positions and borders
   
        self.stepSize = 32
        
        self.leftWall = 0
        
        self.upperWall = 0
        
        #screen and background
        logo = self.pygame.image.load("pictures/unicorn32.bmp")
       
        self.pygame.display.set_icon(logo)
        self.pygame.display.set_caption("Maze Runner")
        self.screen = self.pygame.display.set_mode((self.MAX_X + self.INFO_X ,self.MAX_Y))
    
        self.score = 0
        

        #border 16px of grey/white

        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        # main loop
        
        self.menuDict = {
                        'Play' : 1 ,
                        'DP' : 2 ,
                        'MC' : 3 ,
                        'Exit' : 4
                        }
        
        self.mazeDict = {
                'small' : 1,
                'medium' : 2,
                'large' : 3,
                'Exit' : 4
                }
        
        self.loadImages()
        
    def loadImages(self):
        self.unicornImage = self.pygame.image.load("pictures/unicorn32.bmp")
        self.rainbowImage = self.pygame.image.load("pictures/rainbow32.bmp")
        self.wallImage = self.pygame.image.load("pictures/brick32.bmp")
        self.hellImage = self.pygame.image.load("pictures/hell32.bmp")
        self.appleImage = self.pygame.image.load("pictures/apple32.bmp") 
        self.bombImage = self.pygame.image.load("pictures/bomb32.bmp")
    
    def drawBorder(self):
        
        FRAME = 8
        BORDER_FRAME = 8
        CORNER = 2
        color =(255,255,255)
       
        #top
        x1 = self.START_X - BORDER_FRAME - CORNER 
        y1 = self.START_Y - BORDER_FRAME
        
        x2 = self.START_X + self.MAZE_X + BORDER_FRAME +CORNER+2
        y2 = y1
        #y2 = self.START_Y + self.MAZE_X + FRAME
        self.pygame.draw.line(self.screen, color ,(x1,y1) ,(x2,y2 )  ,FRAME)
        
        #left
        x1 = self.START_X - BORDER_FRAME  
        y1 = self.START_Y - BORDER_FRAME - CORNER
        
        x2 = x1
        y2 = self.START_Y + self.MAZE_Y + BORDER_FRAME +CORNER +2
        self.pygame.draw.line(self.screen, color ,(x1,y1) ,(x2,y2 )  ,FRAME)
        
        #right
        x1 = self.START_X + self.MAZE_X +BORDER_FRAME
        y1 = self.START_Y - BORDER_FRAME - CORNER
        
        x2 = x1
        y2 = self.START_Y + self.MAZE_Y + BORDER_FRAME + CORNER
        self.pygame.draw.line(self.screen, color ,(x1,y1) ,(x2,y2 )  ,FRAME)
        
        #bottom
        x1 = self.START_X - BORDER_FRAME - CORNER
        y1 = self.START_Y + self.MAZE_Y + BORDER_FRAME
        
        x2 = self.START_X + self.MAZE_X + BORDER_FRAME + CORNER+2
        y2 = y1
        self.pygame.draw.line(self.screen, color ,(x1,y1) ,(x2,y2 )  ,FRAME)
        self.pygame.display.flip()
    
    def placeTokens(self):
        cols = self.theMazeGame.size[1]
        rows = self.theMazeGame.size[0]
        
        returnValue = self.theMazeGame.returnGridValue
        for i in range(rows):
            for j in range(cols):
                if self.theMazeGame.policyGrid[i][j] == -1:
                    x = self.START_X + j*32
                    y = self.START_Y + i*32
                    self.screen.blit(self.wallImage, (x,y) )
                if self.theMazeGame.policyGrid[i][j] == 9 and self.theMazeGame.returnGrid[i][j] > 0:
                    x = self.START_X + j*32
                    y = self.START_Y + i*32
                    self.screen.blit(self.rainbowImage, (x,y ))
                if self.theMazeGame.policyGrid[i][j] == 9 and self.theMazeGame.returnGrid[i][j] < 0:
                    x = self.START_X + j*32
                    y = self.START_Y + i*32
                    self.screen.blit(self.hellImage, (x,y) )
                if not self.theMazeGame.policyGrid[i][j] in [1,9] and self.theMazeGame.returnGrid[i][j] > returnValue:
                    x = self.START_X + j*32
                    y = self.START_Y + i*32
                    self.screen.blit(self.appleImage, (x,y) )
                if not self.theMazeGame.policyGrid[i][j] in [1,9] and self.theMazeGame.returnGrid[i][j] < returnValue:
                    x = self.START_X + j*32
                    y = self.START_Y + i*32
                    self.screen.blit(self.bombImage, (x,y) )    
                    
        
        self.screen.blit(self.unicornImage, self.smileyPos) 
        self.pygame.display.flip()
    
    def run(self):
         self.mainMenu()
         self.pygame.quit()
         
    def play(self):
        # event handling, gets all event from the event queue
        
        running = True
       
        while(running):
            self.pygame.time.delay(100)
            self.pygame.event.pump() 
            key = self.pygame.key.get_pressed()
            
            if key[self.pygame.K_LEFT]:
                self.move(self.LEFT)
                self.printScore()
            if key[self.pygame.K_UP]:
                self.move(self.UP)
                self.printScore()
            if key[self.pygame.K_RIGHT]:
                self.move(self.RIGHT)
                self.printScore()
            if key[self.pygame.K_DOWN]:
                self.move(self.DOWN)
                self.printScore()
                    
            if self.theMazeGame.gameOver():
                #self.pygame.quit()
                running = False
                break
            
            if key[self.pygame.K_q]:
                pass
                
            
            for event in self.pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == self.pygame.QUIT:
                    # maybe should go back to main menu or so
                    self.pygame.quit()
                    running = False
    
    def mazeMenu(self,menuType):
        self.clearScreen()

        self.menuItems = 0
        self.menuItemsPos = []
        self.menuItemIdx = 1
        self.printText('Choose Maze for '+ menuType )
        self.printText('Small Maze')
        self.printText('Medium')
        self.printText('Large')
        self.printText('Back')
  
        self.pygame.display.flip()
        
        self.pygame.time.delay(100)
        return self.chooseMaze(menuType)
        
        
        
    def chooseMaze(self, menuType):
        idx = 1
        cursor = self.menuItemsPos[idx] 
        self.screen.blit(self.unicornImage, cursor)
        
        
        while(True):
            self.pygame.time.delay(100)
           
            key = self.pygame.key.get_pressed()
            self.pygame.event.pump() 
       
            x1 = cursor[0]
            y1 = cursor[1]
            if key[self.pygame.K_UP] and idx > 1:
                self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32,32 ))
                idx -=1
                cursor = self.menuItemsPos[idx] 
                self.screen.blit(self.unicornImage, cursor)
                
            if key[self.pygame.K_DOWN] and idx < (self.menuItems-1):
                self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32,32 ))
                idx +=1
                cursor = self.menuItemsPos[idx] 
                self.screen.blit(self.unicornImage, cursor)
                
            if key[self.pygame.K_RETURN]:
                if idx == self.mazeDict['small']:
                    if menuType == 'Play':
                        self.createMaze('small')
                    if menuType == 'DP':
                        self.createMaze('small')
                    return True
                
                if idx == self.mazeDict['medium']:
                    if menuType == 'Play':
                        self.createMaze('medium')
                    return True
                if idx == self.mazeDict['large']:
                    if menuType == 'Play':
                        self.createMaze('large')
                    return True
                if idx == self.mazeDict['Exit']:
                    return False
                
            self.pygame.display.flip()
            if self.quitting():
                return False
            
    def createMaze(self,size):
        #should be MazeSmall()
       
        self.theMazeGame = MazeGame(size)
        cols = self.theMazeGame.size[1]
        rows = self.theMazeGame.size[0]
        self.MAZE_X = cols*32
        self.MAZE_Y = rows*32
        FRAME = 8
        self.START_X = (self.MAX_X - cols*32) / 2 + FRAME #what happens if its not 0 in %32
        self.START_Y = (self.MAX_Y - rows*32) / 2 + FRAME
        x = self.theMazeGame.currentSquare[1]*32
        y = self.theMazeGame.currentSquare[0]*32
        self.smileyPos = (self.START_X + x,self.START_Y + y)
            
    def dynamicProgramming(self):
        x = self.MAX_X +8
        y = 8
        self.printTextRightArea(16,"Dynamic programming" ,x,y)
        y += 32
        self.printTextRightArea(16,"dont play the game" ,x,y)
        y += 32
        self.printTextRightArea(16,"Instead it directly" ,x,y)
        y += 32
        self.printTextRightArea(16,"access the game states" ,x,y)
        y += 32
        self.printTextRightArea(16,"These states are" ,x,y)
        y += 32
        self.printTextRightArea(16,"Policy: the moves" ,x,y)
        y += 32
        self.printTextRightArea(16,"Return: each square" ,x,y)
        y += 32
        self.printTextRightArea(16,"is worth diffrent points" ,x,y)
        y += 32
        self.printTextRightArea(16,"Value: These return " ,x,y)
        y += 32
        self.printTextRightArea(16,"points makes the value " ,x,y)
        y += 32
        
        self.printTextRightArea(16,"Press C to continue" ,x,y)
        self.PressCtoContinue()
        
        self.clearRightArea()
        y = 8
        self.printTextRightArea(16,"Here we see the first Policy" ,x,y)
        #self.ShowPolicy(1)
        
        time.sleep(5)
        pass
    def PressCtoContinue(self):
        while True:
            self.pygame.time.delay(100)
            key = self.pygame.key.get_pressed()
            self.pygame.event.pump() 
            if key[self.pygame.K_c]:
                break
            if self.quitting():
                return
    def clearRightArea(self):
        self.pygame.draw.rect(self.screen, self.BLACK, (self.MAX_X+8,0,self.MAX_X + self.INFO_X,self.MAX_Y))
        
        pass
    def setupGame(self):
        self.clearScreen()       
        self.drawBorder()
        self.placeTokens()
        self.setupRightArea()
        self.theMazeGame.returnCount = 0
        #self.theMazeGame.currentSquare = (0,0)
        self.printScore()
    
    def setupGameDP(self):
        self.clearScreen()       
        self.drawBorder()
        self.placeTokens()
        self.setupRightAreaDP()
        
    def setupRightArea(self):
        FRAME = 4
        white = (255, 255, 255) 
        black = (0,0,0)
       
        x1 = self.MAX_X
        y1 = 0
        
        x2 = self.MAX_X
        y2 = self.MAX_Y
        #y2 = self.START_Y + self.MAZE_X + FRAME
        self.pygame.draw.line(self.screen, white ,(x1,y1) ,(x2,y2 ) ,FRAME)
        
        fontSize = 32
        fontScore = self.pygame.freetype.Font('freesansbold.ttf', fontSize)
        
        x1 = self.MAX_X + 64
        y1 = 64
        
        x2 = 0
        y2 = 0
        
        (textScore,textposScore) = fontScore.render("Score", white, black)
        textposScore = [x1,y1,x2,y2]
        self.screen.blit(textScore, textposScore)
        
        rainbowImage = pygame.image.load("pictures/rainbow32.bmp")
        wallImage = pygame.image.load("pictures/brick32.bmp")
        hellImage = pygame.image.load("pictures/hell32.bmp")
        appleImage = pygame.image.load("pictures/apple32.bmp") 
        bombImage = pygame.image.load("pictures/bomb32.bmp")
        
        
        fontSize = 24
        adjustY = 12
        #collect apples
        x1 = self.MAX_X + 8 
        y1 = 192
        
        lengthOfText = self.printTextRightArea(24,"Collect: ",x1,y1)
        self.screen.blit(appleImage, (x1 + lengthOfText,y1-adjustY) )
        
        
        
        #dont collect bombs
        x1 = self.MAX_X + 8 
        y1 = 256
        
        lengthOfText = self.printTextRightArea(24,"Avoid: ",x1,y1)
        self.screen.blit(bombImage, (x1 + lengthOfText,y1-adjustY) )

        
        #rainbow is good exit
        x1 = self.MAX_X + 8 
        y1 = 320
        
        lengthOfText = self.printTextRightArea(24,"Good Exit: ",x1,y1)
        self.screen.blit(rainbowImage, (x1 + lengthOfText,y1-adjustY) )
        
        #Flame is bad exit
        x1 = self.MAX_X + 8 
        y1 = 384
    
        
        lengthOfText = self.printTextRightArea(24,"Bad Exit: ",x1,y1)
        self.screen.blit(hellImage, (x1 + lengthOfText,y1-adjustY) )
        
        # its a wall
        x1 = self.MAX_X + 8 
        y1 = 448
        
        lengthOfText = self.printTextRightArea(24,"Just a wall: ",x1,y1)
        self.screen.blit(wallImage, (x1 + lengthOfText,y1-adjustY) )
        
        
        self.pygame.display.flip()
    def setupRightAreaDP(self):
        FRAME = 4
        white = (255, 255, 255) 
        #black = (0,0,0)
       
        x1 = self.MAX_X
        y1 = 0
        
        x2 = self.MAX_X
        y2 = self.MAX_Y
        #y2 = self.START_Y + self.MAZE_X + FRAME
        self.pygame.draw.line(self.screen, white ,(x1,y1) ,(x2,y2 ) ,FRAME)
        self.pygame.display.flip()
    def printTextRightArea(self,fontSize, text, x,y):
        
        fontToken = self.pygame.freetype.Font('freesansbold.ttf', fontSize)
        #collect apples
        x1 = x
        y1 = y
        
        x2 = 0
        y2 = 0
        
        (textCollect,textposCollect) = fontToken.render(text, self.WHITE, self.BLACK)
        lengthOfCollect = textposCollect[2] - textposCollect[0] 
        textposCollect = [x1,y1,x2,y2]
        self.screen.blit(textCollect, textposCollect)
        self.pygame.display.flip()
        return lengthOfCollect   
    
    def printScore(self):
        score = str(self.theMazeGame.returnCount)
        fontSize = 32
        
        #erase is it needed? think so
        x1 = self.MAX_X + self.INFO_X / 2
        y1 = 3*32
        self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32+32,32+32 ))
        
        
        fontScore = self.pygame.freetype.Font('freesansbold.ttf', fontSize)
        
        white = (255, 255, 255) 
        black = (0,0,0)
        (textScore,textposScore) = fontScore.render(score, white, black)
        textposScore = [x1,y1,0,0]
        self.screen.blit(textScore, textposScore)
        
        self.pygame.display.flip()
        
     
    def move(self,direction):
         oldSquare = self.theMazeGame.currentSquare
         x1 = oldSquare[1] * 32 + self.START_X
         y1 = oldSquare[0] * 32 + self.START_Y
         
         #print(oldSquare)
         self.theMazeGame.move(direction)
         
         newSquare = self.theMazeGame.currentSquare
         #print(newSquare)
         x2 = newSquare[1] * 32 + self.START_X
         y2 = newSquare[0] * 32 + self.START_Y
         
         
         self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32,32 ))
         self.screen.blit(self.unicornImage, (x2 ,y2)) 
         self.pygame.display.flip()
    
    def mainMenu(self):
        #https://www.programcreek.com/python/example/93421/pygame.freetype
        running =True
        while(running):
            
            self.clearScreen()
            
            self.menuItems = 0
            self.menuItemsPos = []
            self.menuItemIdx = 1
    
            self.printText('Main menu')
            self.printText('Play game')
            self.printText('Dynamic Programming')
            self.printText('Monte Carlo')
            self.printText('Exit')
      
            self.pygame.display.flip()
            
            self.pygame.time.delay(100)
            running = self.choseFromMenu()
                
    def printText(self, text):
        if self.menuItems == 0:
            fontSize = 48
            startY = 32
        else:
            fontSize = 24
            startY = 32 + self.menuItems*48
            
        
        fontMenu = self.pygame.freetype.Font('freesansbold.ttf', fontSize)
        white = (255, 255, 255) 
        black = (0,0,0)
        (textMenu,textposMenu) = fontMenu.render(text, white, black)
        lengthOfText = textposMenu[2] - textposMenu[0] 
        textposMenu[0] = (self.MAX_X + self.INFO_X - lengthOfText) / 2
        textposMenu[1] = startY
        textposMenu[2] = textposMenu[2] + lengthOfText
        textposMenu[3] = textposMenu[1]+32 
        
        self.menuItemsPos.append( (textposMenu[0]-32,startY) )
        
        
        self.screen.blit(textMenu, textposMenu)
        
        self.menuItems += 1
        #self.pygame.display.flip()
    def choseFromMenu(self):
        idx = 1
        cursor = self.menuItemsPos[idx] 
        self.screen.blit(self.unicornImage, cursor)
        
        
        while(True):
            self.pygame.time.delay(100)
           
            key = self.pygame.key.get_pressed()
            self.pygame.event.pump() 
           
            x1 = cursor[0]
            y1 = cursor[1]
            if key[self.pygame.K_UP] and idx > 1:
                self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32,32 ))
                idx -=1
                cursor = self.menuItemsPos[idx] 
                self.screen.blit(self.unicornImage, cursor)
                
            if key[self.pygame.K_DOWN] and idx < (self.menuItems-1):
                self.pygame.draw.rect(self.screen, self.BLACK, (x1,y1,32,32 ))
                idx +=1
                cursor = self.menuItemsPos[idx] 
                self.screen.blit(self.unicornImage, cursor)
                
            if key[self.pygame.K_RETURN]:
                if idx == self.menuDict['Play']:
                    if self.mazeMenu('Play'):
                        self.setupGame()
                        self.play()
                        self.endScreen()
                        return True
                    else:
                        return True
                if idx == self.menuDict['DP']:
                    if self.mazeMenu('DP'):
                        self.setupGameDP()
                        self.dynamicProgramming()
                    return True
                if idx == self.menuDict['Exit']:
                    return False
                
            self.pygame.display.flip()
            if self.quitting():
                return False
            
    def quitting(self):
        for event in self.pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == self.pygame.QUIT:
                    # maybe should go back to main menu or so
                    self.pygame.quit()
                    return True
        return False
    def clearScreen(self):
        self.pygame.draw.rect(self.screen, self.BLACK, (0,0,self.MAX_X + self.INFO_X,self.MAX_Y))
    
    def endScreen(self):
        #remove maze
        self.clearScreen()
        fontSize = 32
        fontScore = self.pygame.freetype.Font('freesansbold.ttf', fontSize)
        white = (255, 255, 255) 
        black = (0,0,0)
        
        
        
        (textScore,textposScore) = fontScore.render("your score is", white, black)
        lengthOfText = textposScore[2] - textposScore[0] 
        textposScore[0] = (self.MAX_X + self.INFO_X - lengthOfText) / 2
        textposScore[1] = 64
        textposScore[2] = 0
        textposScore[3] = 0 
        
        self.screen.blit(textScore, textposScore)
        
        
        score = str(self.theMazeGame.returnCount)
        
        (textScore,textposScore) = fontScore.render(score, white, black)
        lengthOfText = textposScore[2] - textposScore[0] 
        textposScore[0] = (self.MAX_X + self.INFO_X - lengthOfText) / 2
        textposScore[1] = 128
        textposScore[2] = 0
        textposScore[3] = 0 
        
        self.screen.blit(textScore, textposScore)
        
        (textScore,textposScore) = fontScore.render("Press Q to get back to menu", white, black)
        lengthOfText = textposScore[2] - textposScore[0] 
        textposScore[0] = (self.MAX_X + self.INFO_X - lengthOfText) / 2
        textposScore[1] = 192
        textposScore[2] = 0
        textposScore[3] = 0 
        
        self.screen.blit(textScore, textposScore)
        
        
        
        
        self.pygame.display.flip()
        #your score was
        #back to main menu?
        while(True):
            self.pygame.time.delay(100)
            self.pygame.event.pump() 
            key = self.pygame.key.get_pressed()
            if key[self.pygame.K_q]:
                break
            
        for event in self.pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == self.pygame.QUIT:
                    # maybe should go back to main menu or so
                    self.pygame.quit()
                    break
    
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    MR = MazeRunner(pygame)
    MR.run()
   
