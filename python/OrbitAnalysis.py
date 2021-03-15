
#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
# import our Random class from python/Random.py file
sys.path.append(".")
from python.MySort import MySort
from python.Random import RandomOrbit


#  calculate probability of being stable [1] for each hypotheses outfile0 and outfile1
def get_prob(InputFile):
    # read input file
    with open(InputFile) as ifile:
        ct=[]
        for line in ifile:
            lineVals = line.split()
            Nsys = len(lineVals)
            count = 0
            i = 0
            while i in range(Nsys):
                #print(dataset[i])
                #print(lineVals[i])
                if lineVals[i] == '1':
                    count = count +1
                i = i +1
            ct.append(count)
        prob = []
        for c in ct:
            p = c /(len(lineVals))
            prob.append(p)
        # count how much stable outcome in each experiment and return probability of being stable/ per experiment
        return prob


# main function for our Orbit stability Python code
if __name__ == "__main__":
    
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print
        sys.exit(1)
    
    seed = 5555
        
    # default hill criterion for hypothesis 0
    c0 = 1
    
    # default hill criterion for hypothesis 1
    c1 = 3
    
    # default alpha value
    alpha = 0.05
    
    haveH0 = False
    haveH1 = True
   
    
    if '-c0' in sys.argv:
        p = sys.argv.index('-c0')
        c0 = float(sys.argv[p+1])
        
    if '-c1' in sys.argv:
        p = sys.argv.index('-c1')
        c1 = float(sys.argv[p+1])
    
    if '-alpha' in sys.argv:
        p = sys.argv.index('-alpha')
        ptemp = float(sys.argv[p+1])
        if (ptemp > 0 and ptemp<1) :
            alpha = ptemp
            
    if '-input0' in sys.argv:
        p = sys.argv.index('-input0')
        InputFile0 = sys.argv[p+1]
        haveH0 = True
        
    if '-input1' in sys.argv:
        p = sys.argv.index('-input1')
        InputFile1 = sys.argv[p+1]
        haveH1 = True
    
    if '-h' in sys.argv or '--help' in sys.argv or not haveH1:
        print ("Usage: %s [options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -input0 [filename]  name of file for H0 data")
        print ("   -input1 [filename]  name of file for H1 data")
        print ("   -c0 [number]  Hill criterion value for H0")
        print ("   -c1 [number]  Hill criterion value for H1")
        print ("   -alpha [number]      alpha value for H0 [significance of test]")
        print
        sys.exit(1)
    
   
   
    # read Inputfile0 and Inputfile1 for each hypotheses and get possibility
    
    p0 = get_prob(InputFile0)
    #print(p0) # when c = 1, probability of having stable orbit per experiment
    
    p1 = get_prob(InputFile1)
    #print(p1) # when c = 3, probability of having stable orbit per experiment
    
    Nsystem = 1
    LogLikeRatio0 = []
    LogLikeRatio1 = []
    LLR_min = 1e8
    LLR_max = -1e8
    
    with open(InputFile0) as ifile:
        for line in ifile:
            lineVals = line.split()
            Nsystem = len(lineVals)
            LLR = 0
            v = 0
            while v in range(Nsystem):
                # adding LLR for this system
                if float(lineVals[v]) >= 1:
                    #print(v)
                    for i,j in zip(p0,p1):
                        LLR += math.log( float(j)/float(i) )
           
                else:
                    LLR += math.log( (1.-float(j))/(1. -float(i)) )
                
                v +=1
                    
            if LLR < LLR_min:
                LLR_min = LLR
            if LLR > LLR_max:
                LLR_max = LLR
            LogLikeRatio0.append(LLR)
            
    
    #print(LogLikeRatio0)
    
    if haveH1:
        
        with open(InputFile1) as ifile:
            for line in ifile:
                lineVals = line.split()
                Nsystem = len(lineVals)
                #print(lineVals)
                LLR = 0
                v = 0
                while v in range(Nsystem):
                    # adding LLR for this system
                    if float(lineVals[v]) >= 1:
                        #print(v)
                        for i,j in zip(p0,p1):
                            LLR += math.log( float(j)/float(i) )
           
                    else:
                        LLR += math.log( (1.-float(j))/(1. -float(i)) )
                
                    v +=1
                
                if LLR < LLR_min:
                    LLR_min = LLR
                if LLR > LLR_max:
                    LLR_max = LLR
                LogLikeRatio1.append(LLR)
                
       # print(LogLikeRatio1)

     # Now we obtained Loglikelihood ratio for each hypothesis
     # Let's sort the data using default Python sort
    sorter = MySort()
    LLR0 = np.array(sorter.DefaultSort(LogLikeRatio0))
    LLR1 = np.array(sorter.DefaultSort(LogLikeRatio1))
    
    # determine critical value of lambda and power of test beta 
    lambda_c = LLR0[min(int((1-alpha)*len(LLR0)), len(LLR0)-1)]
    beta = (np.where(LLR1 > lambda_c)[0][0]) /len(LLR1)
    # plot LLR figure
    
    title = "%s measurements / experiment with H0 = %.1f, H1 = %.1f as Hill criterion value" % (Nsystem, c0, c1)
    
    plt.figure(figsize=[12,7])
    plt.hist(LLR0, 50, density=True, facecolor='b', alpha=0.75, label="H0 = %.1f" % c0 )
    plt.hist(LLR1, 50, density=True, facecolor='g', alpha=0.75, label="H1 = %.1f" % c1 )
    plt.plot([],[], '', label='$\\alpha = %.3f$' % (alpha))
    plt.plot([],[], '', label='$\\beta = %.3f$' %(beta))
    plt.plot([],[], '', color='k', label='$\lambda_{crit} = $' + '$%.3f$' % (lambda_c))
    plt.axvline(lambda_c, color='k')
    plt.text(lambda_c, 0.002, '$\\alpha = {:.3f}$'.format(alpha))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.yscale('log')
    plt.xlabel('$\lambda = \log [ \mathcal{L}(H1) / \mathcal{L}(H0) ]$')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(True)
    plt.title(title)
    plt.savefig('LLR_hypotheses.png')
    plt.show()
