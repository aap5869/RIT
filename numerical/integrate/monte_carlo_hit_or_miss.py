import inspect
import random
import time
from math import sqrt

def monte_carlo_hit_or_miss(function, lowerLimit, upperLimit, acceptableError,\
                        maximumIterations=100000, numberSamples=1000):

    """
    title::
        monte_carlo_hit_or_miss

    description::
        This method will perform an integration using the Monte Carlo "Hit or
        Miss" method. The method will iterate until it obtains the area under 
        the curve to within a specified acceptable error. If the function
        attribute is a list or tuple it is assumed it is a 2 x M list or tuple.
        The 0th row of the function are assumed to be the x-values of the 
        function and the 1st row is assumed to be the y-values of the function.

    attributes::
        function
            (function, list or tuple) Function for which the area will be found
            under. If it is a list or tuple, it is assumed it is a 2 x M list
            or tuple. The 0th row of the function attribute is assumed to be
            the x-values of the function and the 1st row of the is assumed to
            be the y-values of the function.

        lowerLimit
            (int or float) The lower (left-hand) boundary of the region beneath
            the function for which the area is to be found. Necessary but
            ignored if the function attribute is a list or tuple

        upperLimit
            (int or float) The upper (right-hand) boundary of the region
            beneath. Necessary but ignored if the function attribute is a list
            or tuple

        acceptableError
            (float) The acceptable error for the approximation of the area.
            Necessary but ignored if the function attribute is a list or tuple

        maximumIterations
            (int [optional]) The maximum allowable number of iterations that 
            the method may execute before raising a RuntimeError. Default
            value of 100000.

        numberSamples
            (int [optional]) The of samples at which to initially define the
            function. 

    returns::
        area
            (float) The area under the curve to within a specified acceptable
            error.

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0

    """
    
    # Check if function attribute is a list or tuple
    if isinstance(function, list) or isinstance(function, tuple):
        
        hits = 0
        randomY = []
        maxY = max(function[1])
        
        for i in range(len(function[1])):
            for j in range(numberSamples):
                randomY.append(random.uniform(0, maxY))
                if randomY[j] <= function[1][i]:
                    hits += 1
                    ratio = hits/len(randomY)
                    area = ratio*(max(function[0]) - min(function[0]))*maxY
                    print('Area: {0}'.format(area),end='\r')

        epsilon = (2.0/3.0)*(max(function[0]) - min(function[0]))*maxY*\
                  sqrt((ratio*(1 - ratio))/len(randomY))
            
    # Check if function attribute is a function    
    elif inspect.isfunction(function):

        # Create small table for display purposes on command line.
        # Comment out if unnecessary.
        print('\nArea\t\tEpsilon\t\tIterations')

        # Define variables and empty lists. Epsilon is set to infinity in order
        # to begin while loop.
        maxY = 0
        hits = 0
        iterations = 0
        epsilon = float('inf')
        randomX = []
        randomY = []

        # Create uniformly random numbers between the lower and upper limits 
        # of the function. Check to see if when evalutaed if it is the
        # maximum point of the function within the bounds.
        for x in range(numberSamples):
            randomX.append(random.uniform(lowerLimit, upperLimit))
            if function(randomX[x]) > maxY:
                maxY = function(randomX[x])
        
        # Create uniformly random numbers between 0 and the maximum point of 
        # the function. If it is under the curve count it as a hit.
        for x in range(numberSamples):
            randomY.append(random.uniform(0, maxY))
            if randomY[x] <= function(randomX[x]):
                hits += 1

        # Start integration. Once epsilon is less than acceptable error the
        # while loop is stopped.
        while epsilon >= acceptableError:


            # If the number of iterations reaches the maximum allowable
            # iterations a RuntimeError is raised.
            if iterations == maximumIterations:
                print()
                raise RuntimeError('Reached maximum number of allowed '\
                                   'iterations: {0}'.format(maximumIterations))
            else:
                iterations += 1
                
                # Calculate the ratio of points under the curve
                # to the number of samples that are generated
                ratio = hits/len(randomX)

                # Calculate epsilon
                epsilon = (2.0/3.0)*(upperLimit - lowerLimit)*maxY*\
                          sqrt((ratio*(1 - ratio))/len(randomX))

                # Calculate area under curve
                area = ratio*(upperLimit - lowerLimit)*maxY

                # Create uniformly random number between the upper and lower
                # bounds of the function. Check to see it if is the maximum
                # point of the function. 
                randomX.append(random.uniform(lowerLimit, upperLimit))
                if function(randomX[-1]) > maxY:
                    maxY = function(randomX[-1])
                
                # Create a uniformly random number between 0 and the maximum
                # point of the function. If the number is under the curve 
                # count it as a hit.
                randomY.append(random.uniform(0, maxY))
                if randomY[-1] <= function(randomX[-1]):
                    hits += 1
 
                # Prints out area under curve, epsilon, and iterations.
                # Continuously updates during integration. Comment out if
                # unnecessary.
                print('{0:.6f}\t{1:.6f}\t{2}'\
                      .format(area, epsilon, iterations),end='\r')
                     

    else:
        # Raise TypeError if the function attribute is not a function, list
        # or tuple
        msg = 'Provided attribute "function" is not a function, list or tuple'
        raise TypeError(msg)

    # Return area under curve. Print is added for command line formatting
    # purposes. Comment out if unnecessary.
    print()
    return area

if __name__ == '__main__':

    import math
    import numerical.integrate
    import time

    def f(x):
        return math.sqrt(x)

    lowerLimit = 0.0
    upperLimit = 1.0
    for acceptableError in (0.1, 0.01, 0.001, 0.0001):
        startTime = time.time()
        area = numerical.integrate.monte_carlo_hit_or_miss(f,\
                                                       lowerLimit,\
                                                       upperLimit,\
                                                       acceptableError)
        print('Elapsed time = {0:.6f} [s]'.format(time.time() - startTime))
        print('With an acceptable error of {0:.10f}'.format(acceptableError))
        print('Area of f(x)=sqrt(x) over [{0}, {1}] = {2}'.format(lowerLimit,\
                                                                  upperLimit,\
                                                                  area))
