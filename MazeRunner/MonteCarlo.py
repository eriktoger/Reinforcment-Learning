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
    def __init__(self,size,saveToFiles):
        self.game = MazeGame( size)
        self.squareCountGrid = self.game.createSquareCount()
        self.prefix = "MC"
        self.saveToFiles = saveToFiles
        self.size = size
        if self.saveToFiles:
            self.openFiles()
            self.saveReturnToFiles()
            
            
    
    def playMCGame(self,startSquare, idx,maxIdx):
        randomMove = idx / (maxIdx*2 +1) + 0.5
        self.game.currentSquare = startSquare
        
        keepPlaying = not self.game.gameOver()
        squares_and_returns = [(self.game.currentSquare,0)]
        finished = True
        steps = 0
        while keepPlaying:
            
            #policy
            i = self.game.currentSquare[0]
            j = self.game.currentSquare[1]
            move = self.game.policyGrid[i][j]
      
            if randomMove < np.random.rand():
                moves = self.game.possibleMoves((i,j))
                #print(moves)
                #print(move)
                moves.remove(move)
                if len(moves) > 0:
                    index = np.random.randint(0,len(moves))
                    move = moves[index]
            #move
            self.game.move(move)
            i = self.game.currentSquare[0]
            j = self.game.currentSquare[1]
            theReturn = self.game.returnGrid[i][j]
            squares_and_returns.append( (self.game.currentSquare,theReturn) )
            keepPlaying = not self.game.gameOver()
            steps += 1
            if steps > (100 + 900*idx/maxIdx):
                #print("break")
                finished = False
                break;
        G = 0
        self.squares_and_values = []
        #if idx % 20 == 0:
        
        for s_r in squares_and_returns:
            square = s_r[0]
            if self.saveToFiles and idx in self.saveThis:
                self.squareFile.write( str(square) + " " )
        if self.saveToFiles and idx in self.saveThis:
            self.squareFile.write( "|" )
    
        for square , theReturn in reversed(squares_and_returns):
            self.squares_and_values.append( (square,G) )
            G = theReturn + self.game.gamma*G
        return finished
        #self.squares_and_values.reverse()
    def possibleStartSquare(self):
        #create possibleStartSquares
        rows = self.game.size[0]
        cols = self.game.size[1]
        self.possibleStartSquares = []
        for i in range(rows):
            for j in range(cols):
                if self.game.policyGrid[i][j] in [1,2,3,4]:
                    self.possibleStartSquares.append((i,j))
        
    def randomStartSquare(self):
        return random.choice(self.possibleStartSquares)
        
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
           
    def openFiles(self):
        if self.saveToFiles:
            self.policyGridFile = open("saveFiles/MC/MC"+ str(self.size)  + "policyGrid.txt","w+")
            self.returnGridFile = open("saveFiles/MC/MC" + str(self.size)+ "returnGrid.txt","w+")
            self.valueGridFile = open("saveFiles/MC/MC" + str(self.size)+ "valueGrid.txt", "w+")
            
            self.squareFile = open("saveFiles/MC/MC" + self.size+ "Steps.txt","w+")
    def whatTosave(self, maxIdx):
        
        saveThis =[0,maxIdx-1] # first and last one.
        intervall = maxIdx / 8 # and 8 more.
        for i in range(1,8):
            saveThis.append( int(i*intervall) )
        saveThis.sort()
        print(saveThis)
        self.saveThis = saveThis
        
    def closeFiles(self):
        if self.saveToFiles:
            self.policyGridFile.close()
            self.returnGridFile.close()
            self.valueGridFile.close()
            
            self.squareFile.close()
    
    def saveReturnToFiles(self):
         if self.saveToFiles:
            self.returnGridFile.write("Round" + str(1) + "\n")
            for i in range(self.game.size[0]):
                for j in range(self.game.size[1]):
                    self.returnGridFile.write(str(self.game.returnGrid[i][j]) + " " )
                self.returnGridFile.write("\n")
    
    def savePolicyValueToFile(self,idx):
        #policyGrid
        if self.saveToFiles:
            self.policyGridFile.write("Round" + str(idx) + "\n")
            self.valueGridFile.write("Round" + str(idx) + "\n")
            for i in range(self.game.size[0]):
                for j in range(self.game.size[1]):
                    self.policyGridFile.write(str(self.game.policyGrid[i][j]) + " " )
                    #self.returnGridFile.write(str(self.game.returnGrid[i][j]) + " " )
                    self.valueGridFile.write(str( round(self.game.valueGrid[i][j], 3 ) ) + " " )
                self.policyGridFile.write("\n")
                #self.returnGridFile.write("\n")
                self.valueGridFile.write("\n")
        
    

if __name__=="__main__":
    saveToFiles = False
    MC_Game = MC_solution('small',saveToFiles)
    
    # seams to work with the correct hyper parameters
    maxIdx = 100
    MC_Game.whatTosave(maxIdx)
  
    
    MC_Game.possibleStartSquare()
    randomStarts = True
    startSquare = MC_Game.game.currentSquare
    orgStartSquare = MC_Game.game.currentSquare
    for i in range(maxIdx):
        if i% 1000 == 0: 
            print(i)
            #MC_Game.game.printReturnGrid()    
        if randomStarts:
            startSquare = MC_Game.randomStartSquare()
        #lastTime from
        if i == (maxIdx -1):
            startSquare = orgStartSquare
        if MC_Game.playMCGame(startSquare, i,maxIdx ) :
            MC_Game.updateValueGrid()
        if i in MC_Game.saveThis:
            MC_Game.savePolicyValueToFile(i)
        
        converged = not MC_Game.updatePolicyGrid()
        if converged:
            pass
            #print("converged at: " + str(i))
            #break
        
    MC_Game.printGrids()
    MC_Game.closeFiles()