# PHSX815_Project2: Orbit Stability Simulation of Planetary systems

## Project Description
In this project, we will simulate an idealized planetary system with the Sun at the center, corresponding to orbital parameters samples from their marginal distribution using Monte Carlo Markov Chain method. We implement the Hill stability Criterion \cite{Chambers:1996} \cite{Gladman:1993} in orbit element space to calculate fractional orbital separation for examination of stability of two bodies system.

## This repository contains several types of programs:
* `random.py` 
* `OrbitCounter.py` 
* `OrbitAnalysis.py`
* `MySort.py` 

## General info
The simple experiment simulated will have at least one configurable parameter that can take different values, which are also sampled from an appropriate
probability distribution with at least one configurable parameter. We will study the posterior probability distribution of a parameter of interest and/or can simulate at least two different scenarios (different models/probability distributions or values of parameters associated with hypotheses) and perform an analysis of the output to evaluate how well these different scenarios can be distinguished from each other.
	
## Timeline 
Project is created with:
* ProjectPeerInput version: March 15 
* ProjectResponse version: TBD
* Final Project version: TBD
	
## Code Usage 

```
$ cd ../python
$ python/OrbitCounter.py and python/OrbitAnalysis.py can be called from the command line with the -h 
```
