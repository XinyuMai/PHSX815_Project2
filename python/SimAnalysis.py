
# coding: utf-8

# In[144]:


#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
# import our Random class from python/Random.py file
sys.path.append(".")
from python.MySort import MySort
from python.Random import RandomDist

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
    
    # default alpha, beta for hypothesis 0
    a0 = 0.5
    b0 = 0.5
    
    # default alpha, beta for hypothesis 1
    a1 = 2.
    b1 = 2.
    
    # default alpha value
    alpha = 0.05
    
    haveH0 = True
    haveH1 = True
    
    if '-a0' in sys.argv:
        p = sys.argv.index('-a0')
        a0 = float(sys.argv[p+1])
        
    if '-b0' in sys.argv:
        p = sys.argv.index('-b0')
        b0 = float(sys.argv[p+1])
        
    if '-a1' in sys.argv:
        p = sys.argv.index('-a1')
        a1 = float(sys.argv[p+1])
    
    if '-b1' in sys.argv:
        p = sys.argv.index('-b1')
        b1 = float(sys.argv[p+1])
        
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
        print ("   -a0 [number]  alpha value for H0 (characteristic value for beta distribution)")
        print ("   -b0 [number]  beta  value for H0 (characteristic value for beta distribution")
        
        print ("   -a1 [number]  alpha value for H1 (characteristic value for beta distribution")
        print ("   -b1 [number]  beta  valuee for H1 (characteristic value for beta distribution")
        print ("   -input0 [filename]  name of file for H0 data")
        print ("   -input1 [filename]  name of file for H1 data")
        print ("   -alpha [number]      alpha value for H0 [significance of test]")
        print
        sys.exit(1)
    
   
   
    # read Inputfile0 and Inputfile1 for each hypotheses and get possibility
    data0 = np.loadtxt(InputFile0)
    p0 = get_prob(InputFile0)
    p0 = np.mean(p0)
    
    data1 = np.loadtxt(InputFile1)
    p1 = get_prob(InputFile1)
    p1 = np.mean(p1)
    
    Nms = 1
    Npass0 = []
    LogLikeRatio0 = []
    Npass1 = []
    LogLikeRatio1 = []

    Npass_min = 1e8
    Npass_max = -1e8
    LLR_min = 1e8
    LLR_max = -1e8
        
    with open(InputFile0) as ifile:
        for line in ifile:
            lineVals = line.split()
            Nms = len(lineVals)
            Npass = 0
            LLR = 0
            for v in lineVals:
                Npass += float(v)
                # adding LLR for this toss
                if float(v) >= 1:
                    LLR += math.log( p1/p0 )
                else:
                    LLR += math.log( (1.-p1)/(1.-p0) )
                    
            if Npass < Npass_min:
                Npass_min = Npass
            if Npass > Npass_max:
                Npass_max = Npass
            if LLR < LLR_min:
                LLR_min = LLR
            if LLR > LLR_max:
                LLR_max = LLR
            Npass0.append(Npass)
            LogLikeRatio0.append(LLR)

    if haveH1:
        with open(InputFile1) as ifile:
            for line in ifile:
                lineVals = line.split()
                Nms = len(lineVals)
                Npass = 0
                LLR = 0
                for v in lineVals:
                    Npass += float(v);
                    # adding LLR for this toss
                    if float(v) >= 1:
                        LLR += math.log( p1/p0 )
                    else:
                        LLR += math.log( (1.-p1)/(1.-p0) )

                if Npass < Npass_min:
                    Npass_min = Npass
                if Npass > Npass_max:
                    Npass_max = Npass
                if LLR < LLR_min:
                    LLR_min = LLR
                if LLR > LLR_max:
                    LLR_max = LLR
                Npass1.append(Npass)
                LogLikeRatio1.append(LLR)

    
    # Now we obtained Loglikelihood ratio for each hypothesis
    # Let's sort the data using default Python sort
    sorter = MySort()
    LLR0 = np.array(sorter.DefaultSort(LogLikeRatio0))
    LLR1 = np.array(sorter.DefaultSort(LogLikeRatio1))
    
    # determine critical value of lambda and power of test beta 
    lambda_c = LLR0[min(int((1-alpha)*len(LLR0)), len(LLR0)-1)]
    
    beta = (np.where(LLR1 > lambda_c)[0][0]) /len(LLR1)
    
    
    
    title = str(Nms) +  " Measurements / experiment with different $\\alpha$ , $\\beta$ in Beta distribution"
    # make LLR figure
    plt.figure(figsize=[12,7])
    plt.hist(LogLikeRatio0, Nms+1, density=True, facecolor='b', alpha=0.5, label="assuming $\\mathbb{H}_0$ $\\alpha$ = %.2f, $\\beta$=%.2f " % (a0,b0))
    plt.hist(LogLikeRatio1, Nms+1, density=True, facecolor='g', alpha=0.7, label="assuming $\\mathbb{H}_1$ $\\alpha$ = %.2f, $\\beta$=%.2f " % (a1,b1))
    plt.plot([], '', label='$\\alpha = %.3f$' % (alpha))
    plt.plot([], '', label='$\\beta = %.3f$' %(beta))
    plt.plot([], '', color='k', label='$\lambda_{crit} = $' + '$%.3f$' % (lambda_c))
    plt.axvline(lambda_c, color='k')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.xlabel('$\\lambda = \\log({\\cal L}_{\\mathbb{H}_{1}}/{\\cal L}_{\\mathbb{H}_{0}})$')
    plt.ylabel('Probability')
    plt.title(title)
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('LLR_hypotheses_H0_%s_%s_H1_%s_%s.png' % (a0,b0,a1,b1))
    plt.show()

