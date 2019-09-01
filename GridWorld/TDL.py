#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 08:16:28 2019

@author: erik
"""

import numpy as np
import random
from GridWorld import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, GridWorld



#I should use Q[s][a] but im just using valueGrid since all the actions
#leads to a new square.

class TDL_solution:
    def __init__(self):
        self.game = GridWorld( (5,5))
        self.squareCountGrid = self.game.createSquareCount()
        self.alpha = 0.1
        self.gamma = 0.9
    
    def playTDLGame(self,startSquare, randomMove):
        self.game.currentSquare = startSquare
        
        keepPlaying = not self.game.gameOver()
        squares_and_returns = [(self.game.currentSquare,0)]
     
        while keepPlaying:
            
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
        #self.squares_and_values.reverse()
    
    def playSarsa(self,startSquare, randomMove):
        self.game.currentSquare = startSquare
        keepPlaying = not self.game.gameOver()
        
        while keepPlaying:
            
            #policy
            i1 = self.game.currentSquare[0]
            j1 = self.game.currentSquare[1]
            move = self.game.policyGrid[i1][j1]
      
            if randomMove < np.random.rand():
                moves = self.game.possibleMoves((i1,j1))
                print( str(i1) + " " + str(j1) + " " + str(moves) + " " + str(move) )
                moves.remove(move)
                if len(moves) > 0:
                    idx = np.random.randint(0,len(moves))
                    move = moves[idx]
            #move
            self.game.move(move)
            i2 = self.game.currentSquare[0]
            j2 = self.game.currentSquare[1]
            theReturn = self.game.returnGrid[i2][j2]
            self.game.valueGrid[i1][j1] = self.game.valueGrid[i1][j1] + self.alpha*(theReturn + self.gamma*self.game.valueGrid[i2][j2]- self.game.valueGrid[i1][j1] )
            keepPlaying = not self.game.gameOver()
            
    def playQLearning(self,startSquare, randomMove):
        self.game.currentSquare = startSquare
        keepPlaying = not self.game.gameOver()
        
        while keepPlaying:
            
            #policy
            i1 = self.game.currentSquare[0]
            j1 = self.game.currentSquare[1]
            move = self.game.policyGrid[i1][j1]
            
            # we use the best move even if random runs over it
            i3 = self.game.currentSquare[0]
            j3 = self.game.currentSquare[1]
      
            if randomMove < np.random.rand():
                moves = self.game.possibleMoves((i1,j1))
                print( str(i1) + " " + str(j1) + " " + str(moves) + " " + str(move) )
                moves.remove(move)
                if len(moves) > 0:
                    idx = np.random.randint(0,len(moves))
                    move = moves[idx]
            #move
            self.game.move(move)
            i2 = self.game.currentSquare[0]
            j2 = self.game.currentSquare[1]
            theReturn = self.game.returnGrid[i2][j2]
            self.game.valueGrid[i1][j1] = self.game.valueGrid[i1][j1] + self.alpha*(theReturn + self.gamma*self.game.valueGrid[i3][j3]- self.game.valueGrid[i1][j1] )
            keepPlaying = not self.game.gameOver()
    
        
        
    def updateValueGrid(self):
        for t in range(len(self.squares_and_values) -1):
            
            square , _ = self.squares_and_values[t]
            nextSquare, value = self.squares_and_values[t+1]
            i1 = square[0]
            j1 = square[1]
            i2 = nextSquare[0]
            j2 = nextSquare[1]
            self.game.valueGrid[i1][j1] = self.game.valueGrid[i1][j1] + self.alpha*(value + self.gamma*self.game.valueGrid[i2][j2]- self.game.valueGrid[i1][j1] )  
    
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


TDL_Game = TDL_solution()
# seams to work with the correct hyper parameters
for i in range(200):
    if i% 100 == 0: 
        print(i)
    TDL_Game.playQLearning((0,0), ( i/ (i*2.5+1) ) + 0.5 )
    #print("update")
    #TDL_Game.updateValueGrid()
    TDL_Game.updatePolicyGrid()
    
    
TDL_Game.printGrids()
