#!/usr/bin/python3
import sys
import math 

class PerceptronLearningAlgorithm:

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

    """ Running perceptron algorithm for the given dataset
    and finding the weights w0, w1,....wn for the dataset
    """
    def runPerceptronAlgo(self):

        numDataPoints = 0
        feature1 = []
        feature2 = []
        label = []
        fileObj = open(self.input, 'r')        
  
        for line in fileObj:
            numDataPoints = numDataPoints + 1
            line = line[:len(line)-1]
            lineDataElements = line.split(",")
            feature1.append(float(lineDataElements[0]))
            feature2.append(float(lineDataElements[1]))
            label.append(float(lineDataElements[2]))
            
        """ Initialize weights to zero
        """    
        prev_bias = 0  #intercept 
        prev_w1   = 0
        prev_w2   = 0
        updated_bias = 0
        updated_w1   = 0
        updated_w2   = 0
        fileOut = open(self.output, 'w') 
        
        """ Repeat the perceptron algorithm 
        until it converges
        """
        while True:
            prev_bias = updated_bias 
            prev_w1   = updated_w1
            prev_w2   = updated_w2
            
            """ For each data point check whether the current model is 
            classifying (or) misclassifying
            """
            for i in range(0, numDataPoints):
                
                """ Calculating the function value for the current data point
                """
                fX = prev_bias + prev_w1 * feature1[i] + prev_w2 * feature2[i]

                """ If the product of the true label and calculated function label is <= 0.
                Then we have two labels with different polarity which means we are getting 
                error. The current hyperplane does not classify the current data point 
                properly. So we need to adjust weights i.e, Fix the hyperplane.
                """
                if(label[i] * fX <= 0):
                   
                    """ Adjusting weights
                    """ 
                    updated_bias = prev_bias + label[i]
                    updated_w1 = prev_w1 + label[i] * feature1[i]
                    updated_w2 = prev_w2 + label[i] * feature2[i]

            line = str(updated_w1) + ", " + str(updated_w2) + ", " + str(updated_bias) + "\n"
            fileOut.write(line)

            """ Check whether the algorihm is converging or not
            """
            if self.isConverged(prev_bias, prev_w1, prev_w2, updated_bias, updated_w1, updated_w2):
                break

    """ Function to check whether previous weights and 
    updated weights are equal or not. If equal return 
    True indicating that algorithm has converged
    """
    def isConverged(self, prev_bias, prev_w1, prev_w2, updated_bias, updated_w1, updated_w2):
        
        if abs(updated_bias - prev_bias) == 0 and abs(updated_w1 - prev_w1) == 0 and abs(updated_w2 - prev_w2) == 0:
            return True
        return False

""" Main Program
"""
if __name__ == '__main__':
    
    pla = PerceptronLearningAlgorithm()
    pla.parseCommandLineArgs(sys.argv[1:])
    pla.runPerceptronAlgo()

