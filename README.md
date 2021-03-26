# PHSX815_Project2: Orbit Stability Simulation of Planetary systems

## Project Description
In this project, we will simulate an idealized planetary system with the Sun at the center, corresponding to orbital parameters samples from Beta distribution. We implement the Hill stability Criterion \cite{Chambers:1996} \cite{Gladman:1993} to calculate fractional orbital separation for examination of stability of two bodies system. We perform an analysis of the output to evaluate how well these different scenarios can be distinguished from each other.

We closely examime two hypotheses:

* Hypothesis H0: probability of stable systems assuming model parameters alpha_{0} = 0.5, beta_{0}=0.5
* Hypothesis H1: probability of stable systems assuming model parameters alpha_{1} = 3.0, beta_{1}= 3.0

Note: alpha and beta are two shape parameters of beta distribution.

## This repository contains several types of programs:
* python/ `Random.py`, `OrbitSim.py`, `SimAnalysis.py`, `MySort.py`
* `data/` contains output data
* `plots/` contains output plots
	
## Code Usage 
* Options can be called from the command line with the -h 

* `python3.8 python/OrbitSim.py -a 0.5 -b 0.5 -Nsystem 100 -Nexp 10000 -output H0.txt `
* `python3.8 python/OrbitSim.py -a 3.0 -b 3.0 -Nsystem 100 -Nexp 10000 -output H1.txt `
	* `-a alpha value`
	
	* `-b beta value`
	* `-output [filename]  name of file for hypothesis`

* `python3.8 python/SimAnalysis.py -a0 0.5 -b0 0.5 -a1 3.0 -b1 3.0 -input0 H0.txt -input1 H1.txt`

	* `-a0 [number]  alpha value for H0 (characteristic value for beta distribution)`
	
	* `-b0 [number]  beta  value for H0 (characteristic value for beta distribution)`
        
	* `-a1 [number]  alpha value for H1 (characteristic value for beta distribution)`

	* `-b1 [number]  beta  valuee for H1 (characteristic value for beta distribution)`
	
	* `-input0 [filename]  name of file for H0 data`
	
	* `-input1 [filename]  name of file for H1 data`
	
	* `-alpha [number]      alpha value for H0 [significance of test]`


