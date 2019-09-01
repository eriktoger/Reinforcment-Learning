#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:47:50 2019

@author: erik
"""

import numpy as np
import random
from GridWorld import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, GridWorld

# this one dosnt work )=
# but it seams that he only uses it to check if hes premade policy works
# I guess it only tries to approximate the final policy, not training it on the way

class MC_Aprox_Solution:
    def __init__(self):
        self.game = GridWorld( (5,5))
        self.learning_rate = 0.001
        self.theta = np.random.randn(4) / 2
    
    def s2x(self,square):
        return np.array( [square[0]-1 , square[1] - 1.5, square[0]*square[1] - 3, 1] )
    
    def playMCGame(self,startSquare, randomMove):
        self.game.currentSquare = startSquare
        
        keepPlaying = not self.game.gameOver()
        squares_and_returns = [(self.game.currentSquare,0)]
        counter = 0
        while keepPlaying:
            
            counter += 1
            if counter > 2000:
                return False
            
            #policy
            i = self.game.currentSquare[0]
            j = self.game.currentSquare[1]
            move = self.game.policyGrid[i][j]
      
            if randomMove < np.random.rand():
                moves = self.game.possibleMoves((i,j))
               
                moves.remove(move)
                if len(moves) > 0:
                    idx = np.random.randint(0,len(moves))
                    move = moves[idx]
            #move
            self.game.move(move)
            i = self.game.currentSquare[0]
            j = self.game.currentSquare[1]
            theReturn = self.game.returnGrid[i][j]
            squares_and_returns.append( (self.game.currentSquare,theReturn) )
            keepPlaying = not self.game.gameOver()
        
        G = 0
        self.squares_and_values = []
        for square , theReturn in reversed(squares_and_returns):
            self.squares_and_values.append( (square,G) )
            G = theReturn + self.game.gamma*G
            
        return True
    
    def updateValueGrid(self, t):
        visitedSquares = set()
        
        alpha = self.learning_rate / (t+1)
        for square, G in self.squares_and_values:
            #print(square)
            if not square in visitedSquares:
                visitedSquares.add(square)
                
                old_theta = self.theta.copy()
                x = self.s2x(square)
                V_hat = theta.dot(x)
            
                self.theta += alpha*(G-V_hat)*x
                
        rows = self.game.size[0]
        cols = self.game.size[1]
        for i in range(rows):
            for j in range(cols):
                if self.game.policyGrid[i][j] in [0,1,2,3]:
                    self.game.valueGrid[i][j] = self.theta.dot(self.s2x( (i,j) ) )
                    
    def updatePolicyGrid(self):
        
        #check if policy change
        #hasChanged = False
        #if bestMove is new set to true.
        rows = self.game.size[0]
        cols = self.game.size[1]
        change = False
        for i in range(rows):
            for j in range(cols):
                if self.game.policyGrid[i][j] in [0,1,2,3]: 
                    self.game.currentSquare = (i,j)
                    oldMove = self.game.policyGrid[i][j]
                    self.game.policyGrid[i][j] = self.game.bestMove()
                    if oldMove != self.game.policyGrid[i][j]:
                        change = True
        return change
    
    
    def printGrids(self):
        self.game.printPolicyGrid()
        self.game.printReturnGrid()
        self.game.printValueGrid()

MC_Game = MC_Aprox_Solution()

# seams to work with the correct hyper parameters
counter =0


rows = MC_Game.game.size[0]
cols = MC_Game.game.size[1]
policy = MC_Game.game.policyGrid
print(policy)
randomStart = []
for i in range(rows):
    for j in range(cols):
        if policy[i][j] in [0,1,2,3]:
            randomStart.append ( (i,j) )

print(randomStart)
nrOfStarts = len(randomStart)
for i in range(10000): 
    #print(i)
    if i %1000 ==0 and i >0:
        MC_Game.game.printPolicyGrid()
    square = randomStart[i%nrOfStarts]
    finish = MC_Game.playMCGame(square, i / (i*2.5 +1) + 0.5 )
    if finish:
        MC_Game.updateValueGrid( i/100 )
        MC_Game.updatePolicyGrid()
    else:
        counter +=1
MC_Game.printGrids()
print( counter)