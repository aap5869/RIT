import inspect
import random
import time
from math import sqrt

def monte_carlo_average(function, lowerLimit, upperLimit, acceptableError,\
                        maximumIterations=100000):

    """
    title::
        monte_carlo_average

    description::
        This method will perform an integration using the Monte Carlo "Average"
        method. If the method is given a list or tuple it is assumed that the 
        values are the y-values of the function and are between the desired 
        bounds to integrate over. If the method is given a function it will 
        iterate until it obtains the area under the curve to within a specified
        acceptable error.

    attributes::
        function
            (function, list or tuple) Function for which the area will be found
            under. If list or tuple, it is assumed the values are the y-values
            of the function and are between the desired bounds to integrate 
            over.

        lowerLimit
            (int or float) The lower (left-hand) boundary of the region beneath
            the function for which the area is to be found. Necessary but
            ignored if the function attribute is a list or tuple

        upperLimit
            (int or float) The upper (right-hand) boundary of the region
            beneath. Necessary but ignored if the function attribute is a
            list or tuple

        acceptableError
            (float) The acceptable error for the approximation of the area.
            Necessary but ignored if the function attribute is a list or tuple

        maximumIterations
            (int [optional]) The maximum allowable number of iterations that 
            the method may execute before raising a RuntimeError. Default
            value of 100000. Ignored if function attribute is a list or tuple

    returns::
        area
            (float) The area under the curve to within a specified acceptable
            error. If function attribute is a list or tuple, area accuracy 
            will be dependent on number of elements in the function and will
            not be within specified error.

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0

    """
    
    # Check if function attribute is a list or tuple
    if isinstance(function, list) or isinstance(function, tuple):
        
        # Get number of elements in function attribute. Calculate average
        # of all elements.
        fSquaredBar = 0
        numElements = len(function)
        fBar = sum(function)/numElements
        
        # Square the elements in the function attribute and sum toegether
        for i in function:
            fSquaredBar += i**2
    
        # Calculate average of the squares. Then calculate epsilon
        fSquaredBar /= numElements
        epsilon = (upperLimit - lowerLimit)*sqrt((fSquaredBar - fBar**2)\
                   /numElements)

        # Calculate area and print epsilon. Comment out if unnecessary to 
        # print out.
        area = (upperLimit - lowerLimit)*fBar
        print('Error: {0}'.format(epsilon))
            
    # Check if function attribute is a function    
    elif inspect.isfunction(function):

        # Create small table for display purposes on command line.
        # Comment out if unnecessary.
        print('\nArea\t\tEpsilon\t\tIterations')
        
        # Define variables. Epsilon is set to infinity in order to begin
        # while loop.
        fSum = 0
        fSquaredSum = 0
        iterations = 0
        epsilon = float('inf')

        # Start integration. Once epsilon is less than acceptable error the
        # while loop is stopped. On first iterration epsilon is 0 so 
        while epsilon >= acceptableError or iterations <= 1:

            # Create a uniformly random number between the lower and upper
            # limits of the function.
            randomNumber = random.uniform(lowerLimit, upperLimit)

            # If the number of iterations reaches the maximum allowable
            # iterations a RuntimeError is raised.
            if iterations == maximumIterations:
                print()
                raise RuntimeError('Reached maximum number of allowed '\
                                   'iterations: {0}'.format(maximumIterations))
            else:
                iterations += 1
                
                # Evaluates the function with the random number and adds
                # to the total sum. fSquaredSum sums the squares
                fSum += function(randomNumber)
                fSquaredSum += function(randomNumber)**2

                # Calculate an average of each total sum
                fBar = fSum/iterations
                fSquaredBar = fSquaredSum/iterations
                
                # Calculate epsilon
                epsilon = (upperLimit - lowerLimit)*\
                          sqrt((fSquaredBar - fBar**2) / iterations)

                # Calculate area under curve
                area = (upperLimit - lowerLimit)*fBar

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
        area = numerical.integrate.monte_carlo_average(f,\
                                                       lowerLimit,\
                                                       upperLimit,\
                                                       acceptableError)
        print('Elapsed time = {0:.6f} [s]'.format(time.time() - startTime))
        print('With an acceptable error of {0:.10f}'.format(acceptableError))
        print('Area of f(x)=sqrt(x) over [{0}, {1}] = {2}'.format(lowerLimit,\
                                                                  upperLimit,\
                                                                  area))
