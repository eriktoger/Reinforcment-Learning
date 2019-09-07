#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:11:40 2019

@author: erik
"""

import numpy as np
import random
from MazeGame import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, MazeGame

class MC_solution:
    def __init__(self,size):
        self.game = MazeGame( size)
        self.squareCountGrid = self.game.createSquareCount()
        self.prefix = "MC"
        self.squareFile = open(self.prefix + size+ "square.txt","w+")
    
    def playMCGame(self,startSquare, idx,maxIdx):
        randomMove = idx / (maxIdx*2.5 +1) + 0.5
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
                print(moves)
                print(move)
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
        if idx % 20 == 0:
            for s_r in squares_and_returns:
                square = s_r[0]
                self.squareFile.write( str(square) + " " )
            self.squareFile.write( "|" )
        
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
        
    def saveToFile(self):
        #policyGrid
        policyGridFile = open(self.prefix + "policyGrid.txt","w+")
        returnGridFile = open(self.prefix + "returnGrid.txt","w+")
        valueGridFile = open(self.prefix + "valueGrid.txt", "w+")
        for i in range(self.game.size[0]):
            for j in range(self.game.size[1]):
                policyGridFile.write(str(self.game.policyGrid[i][j]) + " " )
                returnGridFile.write(str(self.game.returnGrid[i][j]) + " " )
                valueGridFile.write(str( round(self.game.valueGrid[i][j], 3 ) ) + " " )
            policyGridFile.write("\n")
            returnGridFile.write("\n")
            valueGridFile.write("\n")
        policyGridFile.close()
        returnGridFile.close()
        valueGridFile.close()


MC_Game = MC_solution('small')

# seams to work with the correct hyper parameters
maxIdx = 100
for i in range(maxIdx):
    if i% 5 == 0: 
        print(i)
        MC_Game.game.printPolicyGrid()    
    MC_Game.playMCGame((0,0), i,maxIdx )
    #print("update")
    MC_Game.updateValueGrid()
    converged = not MC_Game.updatePolicyGrid()
    if converged:
        pass
        #print("converged at: " + str(i))
        #break
    
MC_Game.printGrids()
