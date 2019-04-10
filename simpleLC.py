import math as math
import numpy as np
import os as os
import sys as sys
import subprocess
import argparse
import pdb
import kali


class declareLC(kali.lc.lc):
    def read(self,name = 'LC1', band=r'V', path=None, **kwargs): 
        time = kwargs.get('x')
        y = kwargs.get('y')
        yerr = kwargs.get('yerr')
        
        #---------------------------------------------------------

        cadence = np.require(np.arange(0, len(time),1), requirements=['F', 'A', 'W', 'O', 'E'])
        mask = np.require(np.zeros(len(time)), requirements= ['F', 'A', 'W', 'O', 'E'])  
        mask[:] = int(1)
        
        #---------------------------------------------------------
        #these affect the fit
        self.startT = time[0] # first time index, start at t=0 
        self.T = time[-1]-time[0] #length of the lightcurve
        dt = np.absolute(np.min(time[1:]-time[:-1]))
        self._dt = dt # Increment between epochs.
        self.mindt = dt/10.0
        
        self._numCadences = len(time)
        self.numCadences = len(time)
        
        #---------------------------------------------------------
        #initialize arrays
        self.cadence = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        self.mask = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])  # Numpy array of mask values.
        self.t = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        #self.terr = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        self.x = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        self.y = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        self.yerr = np.require(np.zeros(self.numCadences), requirements=['F', 'A', 'W', 'O', 'E'])
        
        #---------------------------------------------------------
        #fill in arrays with data   
        self.cadence  = cadence
        self.mask = mask     
        self.t = time-time[0]
    	#self.terr = terr[w] 
        self.y = y[:]
        self.yerr = yerr[:]

        #---------------------------------------------------------
        #other LC attributes
        self.z = kwargs.get('z', 0.0)                
        self._name = str(name)  # The name of the light curve (usually the object's name).
        self._xunit = r'$t$~(MJD)'  # Unit in which time is measured (eg. s, sec, seconds etc...).
        self._yunit = r'$F$~($\mathrm{e^{-}}$)'  # Unit in which the flux is measured (eg Wm^{-2} etc...).
        self._band = band
    def write(self, name, path=None, **kwrags):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(r'-n', r'--name', type=str, default=r'LC1', help=r'Object name')
    parser.add_argument(r'-z', r'--z', type=float, default=0.2784, help=r'Object redshift')

    args = parser.parse_args()