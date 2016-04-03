from math import exp
from math import pi

def bb_temperature(wavelength, radiance, epsilon=1e-8):

    """
    title::
        bb_temperature

    description::
        This method will perform a binary search to determine a blackbody's
        temperature at a specified wavelength and radiance within a certain 
        degree of error. The search will be performed between 0 Kelvin and 
        6000 Kelvin. The temperature will be returned as a float with units 
        in Kelvin.

    attributes::
        wavelength 
            (int or float) The wavelength emitted by the blackbody.
            Units are in microns.

        radiance 
            (int or float) The spectral radiance of the blackbody. 
            Units are in W/m^2/micron/sr.

        epsilon 
            ([Optional] float) Specifies the amount of acceptable error when 
            searching for the temperature of the blackbody 
            Defaults to 1e-8 ----> 0.00000001 error

    returns::
        temperature
            (float) The temperature of the blackbody object at a specified
            wavelength and given radiance. Units are in Kelvin

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0

    """
    # Define the bounds of the binary search. Units are in Kelvin
    low_temp = 0
    high_temp = 6000

    # Begin binary search. Stop if the high bound minus the low bound is less
    # than the wanted error precision.
    while (high_temp - low_temp) > epsilon:
        
        # Find middle of bounds and calculate new radiance.
        temperature = (high_temp + low_temp)/2
        current_radiance = planck_bb_eq(wavelength, temperature)
        
        # If new radiance is greater than old, the high bound of the search is
        # set to the newly computed temperature. Else the low bound of the 
        # search is set to the computed temperature.
        if current_radiance > radiance:
            high_temp = temperature
        else:
            low_temp = temperature

    # Return the temperature of the blackbody
    return temperature


def planck_bb_eq(wavelength, temperature):

    """
    description::
        This method will compute the radiance of a blackbody at a specified
        wavelength and temperature using Planck's blackbody equation.

    attributes::
        wavelength
            (float) The wavelength the blackbody is emitting. Units are in
            microns.

        temperature
            (float) The temperature of the blackbody. Units are in Kelvin.

    returns::
        L
            (float) The radiance of the blackbody. Units are in 
            W/m^2/microns/sr.
    """

    C1 = 3.74151*10**8    # Constant value in W/m^2/micron
    C2 = 1.43879*10**4    # Constant value in micronK

    # Planck's blackbody equation
    L = C1 / (pi * wavelength**5)
    exponent = C2 / (wavelength * temperature)
    L = L / (exp(exponent) - 1)

    # Return the radiance of the blackbody.
    # Units are in W/m^2/micron/sr
    return L


if __name__ == '__main__':

    import radiometry

    wavelength = 10 # microns
    trueTemperature = 300 # Kelvin

    bb = radiometry.Blackbody(wavelength, trueTemperature)
    radiance = bb.radiance()
    
    temperature = radiometry.bb_temperature(wavelength, radiance, epsilon=1e-6)
    print('T = {0} [K]'.format(temperature))
    print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
    print('at {0} [microns]'.format(wavelength))

    temperature = radiometry.bb_temperature(wavelength, radiance, epsilon=1e-2)
    print('T = {0} [K]'.format(temperature))
    print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
    print('at {0} [microns]'.format(wavelength))

    temperature = radiometry.bb_temperature(wavelength, radiance)
    print('T = {0} [K]'.format(temperature))
    print('for a blackbody emitting {0} [W/m^2/micron/sr]'.format(radiance))
    print('at {0} [microns]'.format(wavelength))
