#IMPORT MODULES
import random



#CREATE A TURBINE
class Turbine():
    
    #Check proximity to other turbines
    def proximity(self, turbines):
        return (((self._x - turbines._x)**2) + ((self._y - turbines._y)**2))**0.5



    #Place the turbine in a random position
    def locate(self, turbines, min_dist, mce):
        
        #Select a random coordinate
        self._x = random.randint(2, 297)
        self._y = random.randint(2, 297)

        #Check if turbine is near to others
        for turbines in self.turbines:
            prox = self.proximity(turbines)
            
            #If too near, relocate
            if prox <= min_dist:
                self.locate(turbines, min_dist, mce)
        
        #Check if turbine is in an eligible location
        if self.mce != []:    
            if self.mce[self._y][self._x] != 1:
                
                #If not, relocate
                self.locate(turbines, min_dist, mce)



    #Initiating the turbine class
    def __init__ (self, mce = [], turbines = [], min_dist = 0):
        
        #Import variables and create empty variables
        self.turbines, self.min_dist, self.mce = turbines, min_dist, mce
        self._x, self._y = 0, 0
        
        #Begin the locating process
        self.locate(turbines, min_dist, mce)