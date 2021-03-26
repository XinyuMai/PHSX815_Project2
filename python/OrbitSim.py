
# coding: utf-8

# In[37]:


# coding: utf-8
#! /usr/bin/env python
# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

sys.path.append(".")
from python.Random import RandomDist

# Calculate Delta critical value, which is the fraction of the orbital separation and planets’ mutual Hill radius RH
def Delta_cr(a, b, N):
    '''
        Hill parameter calculation with two or more orbiting planets orbit our sun.
        Seperate Hill calculation into two portions - A as semi-major axis fraction sampled from beta distribution
        Mass fraction is a fixed unitless value in our simution. 
        returns Delta_cr (fraction of the orbital separation and planets’ mutual Hill radius RH)
        (e..g. Chambers et al. 1996): > 2*sqr(3) => stable
    '''
    # call from random class samples A from beta distribution
    A = random.Beta(a,b, N)
    # calculate delta_cr
    delta_cr = 2*A*M
    
    return delta_cr


#  calculate probability of being stable [1] for each samples
def get_prob(a,b,N):
    # read input file
        
    delta_cr = Delta_cr(a, b, N)
    cr = 2*np.sqrt(3)
    
    Nsystem = len(delta_cr)
    count = 0
    i = 0
    while i in range(Nsystem):
        if delta_cr[i] > cr:
            count = count +1
        i = i+1
        
    # return probability of being stable given delta_cr    
    prob = count/ Nsystem
    return prob

# plot histogram frequency of delta_cr when output file is delta_cr
def plotHist_dc():
    data = Delta_cr(a, b, Nsystem)
    cr = 2*np.sqrt(3)
    # create histogram of our data
    plt.figure(figsize=[10,8])
    n, bins, patches = plt.hist(data, 25, density=True, facecolor='c', alpha=1)

    # plot formating options
    plt.axvline(cr, color='k')
    plt.xlabel('$\Delta_{crit}$')
    plt.ylabel('Frequency')
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title('Histogram of probability $\Delta_{crit}$ given different $\\alpha$ =%s and $\\beta$ =%s ' %(a,b))
    plt.grid(True)
    plt.savefig('delta_cr_%s_%s.pdf' %(a,b))

# main function for our Orbit stability Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print
        sys.exit(1)

    # default seed
    seed = 5555

    # default alpha and beta for beta distribution
    a = 0.5
    
    b = 0.5
    
    # Mass fraction in the calculation of Delta_cr, fixed.
    M = 10

    # default number of system testing (per experiment)
    Nsystem = 10

    # default number of experiments
    Nexp = 100

    # output file defaults (fixed)
    doOutputFile = True

    
    # read the user-provided seed from the command line (if there)
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-a' in sys.argv:
        p = sys.argv.index('-a')
        a = float(sys.argv[p+1])
        
    if '-b' in sys.argv:
        p = sys.argv.index('-b')
        b = float(sys.argv[p+1])
    
    if '-M' in sys.argv:
        p = sys.argv.index('-M')
        M = float(sys.argv[p+1])
        
    if '-Nsystem' in sys.argv:
        p = sys.argv.index('-Nsystem')
        Ns = int(sys.argv[p+1])
        if Ns > 0:
            Nsystem = Ns
            
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne

    
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True
        
    # class instance of our Random class using seed
    random = RandomDist(seed)
    
    
    if doOutputFile:
        outfile = open(OutputFileName, 'w')
        #probs=[]
        p = get_prob(a,b, Nsystem)
        p = np.mean(p)
        for n in range(Nexp):
            for s in range(Nsystem):
                
                outfile.write(str(random.Bernoulli(p))+" ")
                #probs.append(p)
            outfile.write(" \n")
        outfile.close()
       
    else:
        p = get_prob(a,b, Nsystem)
        p = np.mean(p)
        for e in range(Nexp):
            for t in range(Nsystem):
                
                print(random.Bernoulli(p), end=' ')
            print("  ")

plotHist_dc()
