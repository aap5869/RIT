import radiometry

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
    lowTemp = 0
    highTemp = 6000

    # Begin binary search. Stop if the high bound minus the low bound is less
    # than the wanted error precision.
    while (highTemp - lowTemp) > epsilon:
        
        # Find middle of bounds and redefine a blackbody object with specified
        # wavelength and the new temperature. Then recalculate the radiance of
        # the blackbody object.
        temperature = (highTemp + lowTemp)/2
        blackbody= radiometry.Blackbody(wavelength, temperature)
        currentRadiance = blackbody.radiance()
        
        # If new radiance is greater than old, the high bound of the search is
        # set to the newly computed temperature. Else the low bound of the 
        # search is set to the computed temperature.
        if currentRadiance > radiance:
            highTemp = temperature
        else:
            lowTemp = temperature

    # Return the temperature of the blackbody
    return temperature


if __name__ == '__main__':

    import radiometry

    wavelength = 10 # microns
    trueTemperature = 500 # Kelvin

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
