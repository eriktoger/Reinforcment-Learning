#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 13:20:50 2019

@author: erik
"""
import numpy as np

POSSIBLE_MOVES = ['U','R','D','L'] # C = closed
NR_POSSIBLE_MOVES = len(POSSIBLE_MOVES)
import random
import time
#random.seed(time.clock())

class GridWorld:
    
    def __init__(self, size):
        self.size = size
        
        self.policyGrid = self.createPolicyGrid()
        self.returnGridValue = -0.5
        self.returnGrid = self.createReturnGrid(self.returnGridValue)
        self.valueGrid = self.createValueGrid()
        
      
        self.createObstacle((0,2))
        self.createObstacle((1,2))
        self.createObstacle((2,2))
        
        self.createRandomPolicy()
        
        self.createGoal( (0,4), 10 )
        self.createGoal( (4,4), -10 )
        
        self.currentSquare = (0,0)
        self.returnCount = 0
        
        self.gamma = 0.9
        
        # works to add image of apple/bomb, but needs to be reset after stepping
        # self.returnGrid[2][1] = -5
        
    def createPolicyGrid(self):
        policyGrid = np.zeros(self.size)
        return policyGrid
    
    def createValueGrid(self):
        valueGrid = np.zeros(self.size)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.policyGrid[i][j] == -1:
                    valueGrid[i][j] = np.random.randn(1,1)
                else:
                    valueGrid[i][j] = None
        return valueGrid
    
    def createRandomPolicy(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.policyGrid[i][j] == -1:
                    self.policyGrid[i][j] = self.randomAdjecentValidSquare((i,j))
    
    def randomAdjecentValidSquare(self,square):
       if square[0] >= self.size[0] or square[0] < 0 or square[1] >= self.size[1] or square[1] < 0 :
           return None # we are out of bound
       
       actionIdx = random.randint(0,NR_POSSIBLE_MOVES-1)
       firstActionIdx = actionIdx
       
       step = (0,0) # no step
       while(True):
         
           
           if actionIdx == 0:
               step = (-1,0) # step up
           if actionIdx == 1:
               step = (0,1) # step right
           if actionIdx == 2:
               step = (1,0) # step down
           if actionIdx == 3:
               step = (0,-1) # step left
     
           newSquare = (square[0]+step[0] , square[1]+step[1])
           if 0 <= newSquare[0] < self.size[0] and 0 <= newSquare[1] < self.size[1]:
               if not self.policyGrid[newSquare[0]][newSquare[1]] == -1:
                   break
           
           actionIdx += 1
           actionIdx = actionIdx % NR_POSSIBLE_MOVES
        
           if actionIdx == firstActionIdx:
               return None
    
       return actionIdx
    
    def bestMove(self):
        
        bestValue = -999999
        bestMove = None
        for step in [(-1,0),(0,1),(1,0),(0,-1)]: # u r d l
            square = self.currentSquare
            newSquare = (square[0]+step[0] , square[1]+step[1])
            if 0 <= newSquare[0] < self.size[0] and 0 <= newSquare[1] < self.size[1]:
               if not self.policyGrid[newSquare[0]][newSquare[1]] == -1:
                   # took me like 1 hour to find that i missed return here. Should it be gamma aswell?
                   currentValue = self.valueGrid[newSquare[0]][newSquare[1]] + self.returnGrid[newSquare[0]][newSquare[1]]
                   if bestValue < currentValue: 
                       bestMove = step
                       bestValue = currentValue
        
        if bestMove == (-1,0):
            return 0
        if bestMove == (0,1):
            return 1
        if bestMove == (1,0):
            return 2
        if bestMove == (0,-1):
            return 3
        return None
    
    def possibleMoves(self, square):
        moves = []
        for step in [(-1,0),(0,1),(1,0),(0,-1)]: # u r d l
            newSquare = (square[0]+step[0] , square[1]+step[1])
            if 0 <= newSquare[0] < self.size[0] and 0 <= newSquare[1] < self.size[1]:
                if not self.policyGrid[newSquare[0]][newSquare[1]] == -1:
                     if step == (-1,0):
                         moves.append(0)
                     if step == (0,1):
                         moves.append(1)
                     if step == (1,0):
                         moves.append(2)
                     if step == (0,-1):
                         moves.append(3)
        return moves
        
    def move(self,actionIdx):
        
        step = (0,0) # no step
        if actionIdx == 0:
               step = (-1,0) # step up
        if actionIdx == 1:
               step = (0,1) # step right
        if actionIdx == 2:
               step = (1,0) # step down
        if actionIdx == 3:
               step = (0,-1) # step left
               
        newSquare = (self.currentSquare[0]+step[0] , self.currentSquare[1]+step[1])
        if 0 <= newSquare[0] < self.size[0] and 0 <= newSquare[1] < self.size[1]:
            if not self.policyGrid[newSquare[0]][newSquare[1]] == -1:
               self.currentSquare = newSquare
               self.returnCount += self.returnGrid[newSquare[0]][newSquare[1]]
                    
    
    def playMCGame(self,startSquare, randomMove):
        self.currentSquare = startSquare
        
        keepPlaying = self.gameOver()
        squares_and_returns = [(self.currentSquare,0)]
        
        while keepPlaying:
            
            #policy
            i = self.currentSquare[0]
            j = self.currentSquare[1]
            move = self.policyGrid[i][j]
            if randomMove < np.random.rand():
                moves =self.possibleMoves()
                moves.remove(move)
                if len(moves) > 0:
                    idx = np.random.randint(0,len(moves))
                    move = moves[idx]
            #move
            self.move(move)
            i = self.currentSquare[0]
            j = self.currentSquare[1]
            theReturn = self.returnGrid[i][j]
            squares_and_returns.appen (self.currentSquare,theReturn)
            keepPlaying = self.gameOver()
        
        G = 0
        self.squares_and_values = []
        for square , theReturn in reversed(squares_and_returns):
            self.squares_and_values.append( (square,theReturn) )
            G = theReturn + self.gamma*G
            
        self.squares_and_values.reverse()
    

    
    def gameOver(self):
        i = self.currentSquare[0]
        j = self.currentSquare[1]
        if self.policyGrid[i][j] == 9:
            return True
        return False
    
    def createObstacle(self,square):
        self.policyGrid[square[0]][square[1]] = -1
        self.returnGrid[square[0]][square[1]] = None
        self.valueGrid[square[0]][square[1]] = None
        
    def createGoal(self,square,value):
        self.policyGrid[square[0]][square[1]] = 9
        self.returnGrid[square[0]][square[1]] = value
        self.valueGrid[square[0]][square[1]] = 0
        
    def printPolicyGrid(self):
        print("Policy Grid")
        for i in range(self.size[0]):
            print()
            for j in range(self.size[1]):
                if self.policyGrid[i][j] == 0:
                   print(' U ', end = '')
                if self.policyGrid[i][j] == 1:
                   print(' R ', end = '')
                if self.policyGrid[i][j] == 2:
                   print(' D ', end = '')
                if self.policyGrid[i][j] == 3:
                   print(' L ', end = '')
                if self.policyGrid[i][j] == -1:
                   print(' C ', end = '')
                if self.policyGrid[i][j] == 9:
                   print(' G ', end = '')
        print()
        print()
    
    def createReturnGrid(self,value):
        returnGrid = np.zeros(self.size)
        returnGrid[:] = value
        return returnGrid
    
    def createSquareCount(self):
        squareCount = np.zeros(self.size)
        return squareCount
    
    def printReturnGrid(self):
        print("Return Grid")
        for i in range(self.size[0]):
            print()
            for j in range(self.size[1]):
                print(" " + str(self.returnGrid[i][j]) +" ",end ='')
        print()
        print()
        
    def printValueGrid(self):
        print("Value Grid")
        for i in range(self.size[0]):
            print()
            for j in range(self.size[1]):
                print(" " + str(round(self.valueGrid[i][j],1)) +" ",end ='')
        print()
        print()
        
#game = GridWorld((5,5))
#game.printPolicyGrid()
#game.printReturnGrid()
#game.printValueGrid()