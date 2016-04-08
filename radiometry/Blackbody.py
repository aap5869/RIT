class Blackbody():

    """
    title::
        Blackbody
        
    description::
        Creates a blackbody object with attributes wavelength and
        absolute temperature. Can compute its radiance using Planck's 
        blackbody equation at a specific wavelength and temperature as 
        well as compute its peak wavelength at which the spectral radiance 
        is the greatest. Can also calculate the radiance over a list of 
        wavelengths for each wavelength.
    
    attributes::
        wavelength 
            (int) The blackbody's wavelength in microns

        absoluteTemperature 
            (int) The blackbody's temperature in Kelvin

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0

    """

    def __init__(self, wavelength, absoluteTemperature):

        """
        description::
            Instantiates Blackbody class with wavelength and absolute
            temperature
        
        attributes::
            wavelength 
                (int): the blackbody's wavelength in microns

            absoluteTemperature 
                (int): the blackbody's temperature in Kelvin
        """

        self._wavelength = wavelength
        self._absoluteTemperature = absoluteTemperature

    @property
    def wavelength(self):
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self._wavelength = wavelength

    @property
    def absoluteTemperature(self):
        return self._absoluteTemperature

    @absoluteTemperature.setter
    def absoluteTemperature(self, absoluteTemperature):
        self._absoluteTemperature = absoluteTemperature

    def __repr__(self):

        """
        description::
            Returns the string representation of the object with
            its wavelength and absoulte temperature attributes
        """

        string = "Wavelength = {0} microns, Temperature = {1} K"\
                 .format(self._wavelength, self._absoluteTemperature)

        return string

    def radiance(self):

        """
        description::
            Calculates the blackbody's radiance using Planck's
            blackbody equation

        returns::
            L (Float): The spectral radiance of the blackbody object.
            Units are in W/m^2/micron/sr.
        """

        from math import exp
        from math import pi

        C1 = 3.74151*10**8    # Constant value in W/m^2/micron
        C2 = 1.43879*10**4    # Constant value in micronK

        # Planck's blackbody equation 
        L = C1 / (pi * self._wavelength**5)
        exponent = C2 / (self.wavelength * self.absoluteTemperature)
        L = L / (exp(exponent) - 1)

        return L

    def spectral_radiance(self, wavelengths):

        """
        description::
            Calculates the blackbody's radiance over a given list of
            wavelengths at one temperature using Planck's blackbody equation.
            Returns a list of radiance values, each of which correspond to 
            each wavelength in the list of 'wavelengths' provided.

        attributes::
            wavelengths 
                (list of floats) Wavelengths in microns

        returns::
            radiances 
                (list of floats) The spectral radiance for each wavelength
                in the wavelengths list. Units are in W/m^2/micron/sr.
        """

        radiances = []

        for wavelength in range(len(wavelengths)):
            
            self.wavelength = wavelengths[wavelength]
            radiances.append(self.radiance())
            
        return radiances

    def peak_wavelength(self):

        """
        description::
            Calculates the peak wavelength at which the blackbody's spectral 
            radiance is the greatest

        returns::
            peakWavelength 
                (Float) The peak wavelength. Units are in microns.
        """

        B = 2.897768551*10**3   # Wein's displacement in micronK

        peakWavelength = B / self._absoluteTemperature

        return peakWavelength
    

if __name__ == '__main__':

    import radiometry

    bb = radiometry.Blackbody(8, 300)
    print(bb)
    print('L = {0} [W / m^2 / micron / sr]'.format(bb.radiance()))
    print('Peak wavelength = {0} [microns]'.format(bb.peak_wavelength()))

    import matplotlib.backends.backend_agg
    import matplotlib.pyplot

    start_wavelength = 8
    end_wavelength = 14
    wavelength_increment = 0.1
    wavelengths = []

    for value in range(int((end_wavelength - start_wavelength) 
                            / wavelength_increment) + 1):
        wavelengths.append(start_wavelength + value * wavelength_increment)

    radiances = bb.spectral_radiance(wavelengths)

    figure = matplotlib.pyplot.figure('Spectral Radiance of Blackbody')
    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(figure)

    axes = figure.add_subplot(1, 1, 1)
    axes.set_xlabel('Wavelength [microns]')
    axes.set_ylabel('Radiance [W / m^2 / sr / micron]')
    axes.set_xlim([start_wavelength, end_wavelength])
    axes.xaxis.grid(True)
    axes.yaxis.grid(True)
    axes.plot(wavelengths, radiances, color='green')

    matplotlib.pyplot.show()
    canvas.print_figure('plot.eps')

