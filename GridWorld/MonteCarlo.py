#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:11:40 2019

@author: erik
"""

import numpy as np
import random
from GridWorld import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, GridWorld

class MC_solution:
    def __init__(self):
        self.game = GridWorld( (5,5))
        self.squareCountGrid = self.game.createSquareCount()
    
    def playMCGame(self,startSquare, randomMove):
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
    
    def updateValueGrid(self):
        visitedSquares = set()
        
        for square, G in self.squares_and_values:
            #print(square)
            if not square in visitedSquares:
                visitedSquares.add(square)
                i = square[0]
                j = square[1]
                self.squareCountGrid[i][j] += 1
                self.game.valueGrid[i][j] = self.game.valueGrid[i][j] + (G - self.game.valueGrid[i][j] ) / self.squareCountGrid[i][j] 
                
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
        print(self.squareCountGrid)

MC_Game = MC_solution()

# seams to work with the correct hyper parameters
for i in range(20000):
    if i% 1000 == 0: 
        print(i)
        MC_Game.game.printPolicyGrid()
    MC_Game.playMCGame((0,0), i / (i*2.5 +1) + 0.5 )
    #print("update")
    MC_Game.updateValueGrid()
    converged = not MC_Game.updatePolicyGrid()
    if converged:
        print("converged at: " + str(i))
        break
    
MC_Game.printGrids()
