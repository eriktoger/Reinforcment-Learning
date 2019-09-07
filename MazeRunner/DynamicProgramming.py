#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:34:00 2019

@author: erik
"""
import numpy as np
import random
from MazeGame import POSSIBLE_MOVES,NR_POSSIBLE_MOVES, MazeGame


GAMMA = 0.9
LOWER_LIMIT = 0.0001


class DP_Solution:
    def __init__(self, size,gamma, lower_limit):
        self.game = MazeGame( size)
        self.size = size
        self.gamma = gamma
        self.lower_limit = lower_limit
    
    def updateValueGrid(self):
        rows = self.game.size[0]
        cols = self.game.size[1]
        for i in range(rows):
            for j in range(cols):
                move = self.game.policyGrid[i][j]
                #print(str(i)+" " + str(j) +" " +str(move))
                if move in [0,1,2,3]:    
                    if move == 0:
                        theReturn = self.game.returnGrid[i-1][j]
                        self.game.valueGrid[i][j] = self.gamma *(theReturn +self.game.valueGrid[i-1][j])
                       
                    if move == 1:
                        theReturn = self.game.returnGrid[i][j+1]
                        self.game.valueGrid[i][j] =self.gamma *(theReturn + self.game.valueGrid[i][j+1])
                     
                    if move == 2:
                        theReturn = self.game.returnGrid[i+1][j]
                        self.game.valueGrid[i][j] = self.gamma *(theReturn + self.game.valueGrid[i+1][j])
                        
                    if move == 3:
                        theReturn = self.game.returnGrid[i][j-1]
                        self.game.valueGrid[i][j] =self.gamma *(theReturn + self.game.valueGrid[i][j-1])
                      
                        
    def updateValueGridWindy(self, sucessRate= 0.75):
        rows = self.game.size[0]
        cols = self.game.size[1]
       
        for i in range(rows):
            for j in range(cols):
                possibleMoves = self.game.possibleMoves( (i,j) )
                nrOfWrongMoves = len(possibleMoves) -1
                chosenMove = self.game.policyGrid[i][j]
                if not self.game.policyGrid[i][j] in [-1,9]:
                    self.game.valueGrid[i][j] = 0
                    for move in possibleMoves:
                        if move == chosenMove:
                            p = sucessRate
                        else:
                            if nrOfWrongMoves != 0:
                                p = (1 - sucessRate) / nrOfWrongMoves
                            else:
                                p = 0 # shouldnt happen   
                        if move == 0:
                            theReturn = self.game.returnGrid[i-1][j]
                            self.game.valueGrid[i][j] += p*self.gamma *(theReturn +self.game.valueGrid[i-1][j])
                        if move == 1:
                            theReturn = self.game.returnGrid[i][j+1]
                            self.game.valueGrid[i][j] += p*self.gamma *(theReturn + self.game.valueGrid[i][j+1])
                        if move == 2:
                            theReturn = self.game.returnGrid[i+1][j]
                            self.game.valueGrid[i][j] += p*self.gamma *(theReturn + self.game.valueGrid[i+1][j])
                        if move == 3:
                            theReturn = self.game.returnGrid[i][j-1]
                            self.game.valueGrid[i][j] += p*self.gamma *(theReturn + self.game.valueGrid[i][j-1])
                            
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
    
    def updatePolicyGridWindy(self):
        
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
    
    def updateUntilConvergence(self,save):
        change = True
        count =0
        
        while change:
            change = self.updatePolicyGrid()
            self.updateValueGrid()
            count += 1
            if save:
                self.saveToFile(count)
            print(count)
    
            DP_Game.printGrids()
            if count %1000 == 0:
                print("count: "+ str(count))
                DP_Game.printGrids()
            if count >10000:
                print("didnt converge")
                break
    
    def printGrids(self):
        pass
        self.game.printPolicyGrid()
        self.game.printReturnGrid()
        self.game.printValueGrid()
    
    def openFiles(self):
        prefix = "DP"
        self.policyGridFile = open(prefix + self.size + "policyGrid.txt","w+")
        self.returnGridFile = open(prefix + self.size + "returnGrid.txt","w+")
        self.valueGridFile = open(prefix + self.size + "valueGrid.txt", "w+")
    def saveToFile(self,i):
        self.policyGridFile.write("Round" + str(i) + "\n")
        self.returnGridFile.write("Round" + str(i) + "\n")
        self.valueGridFile.write("Round" + str(i) + "\n")
        for i in range(self.game.size[0]):
            for j in range(self.game.size[1]):
                self.policyGridFile.write(str(self.game.policyGrid[i][j]) + " " )
                self.returnGridFile.write(str(self.game.returnGrid[i][j]) + " " )
                self.valueGridFile.write(str( round(self.game.valueGrid[i][j], 3 ) ) + " " )
            self.policyGridFile.write("\n")
            self.returnGridFile.write("\n")
            self.valueGridFile.write("\n")
    def closeFiles(self):    
        self.policyGridFile.close()
        self.returnGridFile.close()
        self.valueGridFile.close()
    
if __name__=="__main__":
    DP_Game = DP_Solution('small',GAMMA, LOWER_LIMIT)
    save = False
    
    if save:
        DP_Game.openFiles()
    DP_Game.updateUntilConvergence(save)
    if save:
        DP_Game.openFiles()
    DP_Game.printGrids()
