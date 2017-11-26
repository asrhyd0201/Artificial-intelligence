#!/usr/bin/python3
import sys
import math

class GradientDescent:

    """ Parsing the command line arguments
    and extracitng input filename and 
    output filename from the arguments
    """
    def parseCommandLineArgs(self,args):

        if(len(args) < 2):
            print ('Usage: problem2_3.py <input.csv> <output.csv>')
            sys.exit(1)
        else:
            self.input   = args[0]
            self.output  = args[1]


    """ Features age and weight of each data point  
    are scaled by its population standard deviation 
    and set their means to zero. Formula for scaling,
    for each feature "x":
    X(scaled) = [x - mean(x)] / stdDev(x)
    """    
    def dataPreparationAndNormalization(self):

        fileObj = open(self.input, 'r')        
        numDataPoints = 0
        self.age    = []
        self.weight = []
        self.height = []
        ageSum = 0
        ageMean = 0
        weightSum = 0
        weightMean = 0      
        ageMeanDiff = 0
        weightMeanDiff = 0  
        ageStdDev = 0
        weightStdDev = 0

        for line in fileObj:

            numDataPoints = numDataPoints + 1
            line = line[:len(line)-1]
            lineDataElements = line.split(",")
            self.age.append(float(lineDataElements[0]))    
            self.weight.append(float(lineDataElements[1]))    
            self.height.append(float(lineDataElements[2]))    
            ageSum = ageSum + float(lineDataElements[0])
            weightSum = weightSum + float(lineDataElements[1])

        ageMean = ageSum / numDataPoints
        weightMean = weightSum / numDataPoints
        
        for index in range(0, len(self.age)):
            ageMeanDiff = ageMeanDiff + (self.age[index] - ageMean) * (self.age[index] - ageMean)
            
        for index in range(0, len(self.weight)):
            weightMeanDiff = weightMeanDiff + (self.weight[index] - weightMean) * (self.weight[index] - weightMean) 
        
        ageStdDev = math.sqrt(ageMeanDiff / numDataPoints)
        weightStdDev = math.sqrt(weightMeanDiff / numDataPoints)
       
        for index in range(0, len(self.age)):
            self.age[index] = (self.age[index] - ageMean) / ageStdDev
            
        for index in range(0, len(self.weight)):
            self.weight[index] = (self.weight[index] - weightMean) / weightStdDev
        fileObj.close()


    
    """ Running gradient descent algorithm using range
    of learning rates(alpha) for exactly 100 iterations
    to compare the convergence rate when learning rate 
    (alpha) is small versus large.
    """
    def runGradientDescent(self):

        numOfIterations = 101
        learningRate = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.003] 
        fileObj = open(self.output, 'w')        
        
        """ Running each learning rate (alpha) value 
        for 100 iterations to find beta values.
        """
        for lR in learningRate: 
            # Initialize betas to zeros
            beta0 = 0
            betaAge = 0
            betaWeight = 0
             
            for iter in range(1, numOfIterations):
                beta0, betaAge, betaWeight = self.stepGradient(beta0, betaAge, \
                        betaWeight, lR, self.age, self.weight, self.height)
            line = str(lR) + "," + str(iter) + "," + str(beta0) + "," + str(betaAge) + "," + str(betaWeight) + "\n"
            fileObj.write(line)

    """ Calculating beta values for one iteration
    """            
    def stepGradient(self, beta0, beta1, beta2, learningRate, x1, x2, y):   
        
        n = len(x1)
        b0_gradient = 0
        b1_gradient = 0
        b2_gradient = 0
        
        """ Updating beta values for each data point in the given dataset
        Formula for beta values is :-
        beta(i) = beta(i) - (alpha) * (1/n) * Summation from 0 -> n [ F(xi) - y(i) ] * x(i)
        F(xi) = beta0 + beta1 * feature1[i] + beta2 * feature2[i]
        For beta0, x(i) = 1
        """
        for i in range(0, n):
   
            Fx =  beta0 + beta1 * x1[i] + beta2 * x2[i]
            b0_gradient = b0_gradient + ( Fx - y[i])      
            b1_gradient = b1_gradient + ( Fx - y[i]) * x1[i]
            b2_gradient = b2_gradient + ( Fx - y[i]) * x2[i]

        beta0 = beta0 - learningRate * (1 / n) * b0_gradient
        beta1 = beta1 - learningRate * (1 / n) * b1_gradient
        beta2 = beta2 - learningRate * (1 / n) * b2_gradient
        
        return [beta0, beta1, beta2]


""" Main program
"""     
if __name__ == '__main__':
    
    gd = GradientDescent()
    gd.parseCommandLineArgs(sys.argv[1:])
    gd.dataPreparationAndNormalization()
    gd.runGradientDescent()

