# coding: utf-8

#! /usr/bin/env python

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import beta
import random
# MKS units, constants
sec = 1
meter = 1
kg = 1
deg = np.pi/180.
km = 1.e3 * meter
day = 86400 * sec
year = 365.26*day
AU = 1.49e8 * km
c = 3e8 * meter/sec
G = 6.674e-11 *meter**3 / (kg*sec**2)
Msun = 2e30 * kg
Mjup = 1.9e27 * kg

#################
# Random class
#################
# class that can generate random numbers
class RandomDist:
    """A random number generator class"""

    # initialization method for Random class
    def __init__(self, seed = 5555):
        self.seed = seed
        self.m_v = np.uint64(4101842887655102017)
        self.m_w = np.uint64(1)
        self.m_u = np.uint64(1)
        
        self.m_u = np.uint64(self.seed) ^ self.m_v
        self.int64()
        self.m_v = self.m_u
        self.int64()
        self.m_w = self.m_v
        self.int64()
        '''
        - Msun: solar mass as center
        - planetary parameters e.g., [[m1,a1,e1],[m2,a2,e2],[m3,a3,e2],...)
        - all quantities are in MKS units; angles in radians
        '''
        self.c = 3e8
        self.G = 6.674e-11
        self.Msun = 1.99e30
        self.day = 86400
        self.year = 365.26*86400
        
    
    
    # function returns a random 64 bit integer
    def int64(self):
        with np.errstate(over='ignore'):
            self.m_u = np.uint64(self.m_u * np.uint64(2862933555777941757) + np.uint64(7046029254386353087))
        self.m_v ^= self.m_v >> np.uint64(17)
        self.m_v ^= self.m_v << np.uint64(31)
        self.m_v ^= self.m_v >> np.uint64(8)
        self.m_w = np.uint64(np.uint64(4294957665)*(self.m_w & np.uint64(0xffffffff))) + np.uint64((self.m_w >> np.uint64(32)))
        x = np.uint64(self.m_u ^ (self.m_u << np.uint64(21)))
        x ^= x >> np.uint64(35)
        x ^= x << np.uint64(4)
        with np.errstate(over='ignore'):
            return (x + self.m_v)^self.m_w
    

    # function returns a random floating point number between (0, 1) (uniform)
    def rand(self):
        return 5.42101086242752217E-20 * self.int64()
    
    
    # function returns a random integer (0 or 1) according to a Bernoulli distr.
    def Bernoulli(self, p):
        if p < 0. or p > 1.:
            return 1
        
        R = self.rand()

        if R < p:
            return 1
        else:
            return 0

    # function returns a random double (0 to infty) according to an exponential distribution
    def Exponential(self, beta=1.):
      # make sure beta is consistent with an exponential
      if beta <= 0.:
        beta = 1.

      R = self.rand()

      while R <= 0.:
        R = self.rand()

      X = -math.log(R)/beta

      return X

    # function returns a random integer using normal distribution (Box-muller)
    def normal(self, mu=2., sigma=0.5):
        if sigma <= 0.:
            sigma = 0.5
        
        R1 = self.rand();
        R2 = self.rand();
        
        y1 = np.sqrt(-2*np.log(R1))*np.cos(2*np.pi*R2)
        y2 = np.sqrt(-2*np.log(R1))*np.sin(2*np.pi*R2)
        
        X = y1*sigma+mu
        return X
        
        
    # implement beta distribution
    def Beta(self, a, b, n):
        import numpy as np
        import random
        # two shape parameters namely 𝛼 and 𝛽 both >0
        if a <= 0.:
            a = 0.5
            
        if b <= 0.:
            b = 0.5
        
        X = np.random.beta(a, b, n)
        
        return X
    
