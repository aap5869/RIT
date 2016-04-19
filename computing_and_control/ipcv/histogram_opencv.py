import cv2
import numpy

def histogram(image, bitDepth=8):

    """
    title::
        histogram_opencv

    description::
        This method will gneerate the histogram, probability density funciton 
        and the cumulative density funciton of an image. It will use the
        cv2.calcHist method from the opencv library to help generate each 
        output. Each output will be returned as a list.

    attributes::
        images
            (numpy ndarray) An image file that is read in by the cv2.imread
            function. The iamge can be either black and white or full color and
            can have any bit depth. For color images, the color channel order
            is BGR (blue, green, red).

        bitDepth
            (int [optional]) The bit depth of each color channel of the image.
            Defaults to 8 bits per color channel.

    returns::
        h
            (list) The histogram for the image. For a color image, the 
            histogram is a list of three lists with each list representing the
            histogram for each color channel in BGR order. For a grayscale
            image, the histogram will be returned as a 2^N element list, N
            being the bit depth of the image.

        pdf
            (list) The PDF (probability density function) for the image. For a
            color image, the PDF is a list of three lists with each list
            representing the PDF for each color channle in BGR order. For a 
            grayscale image, the PDf will be returned as a 2^N element list, N
            being the bit depth of the image.

        cdf
            (list) The CDF (cumulative density function) for the image. For a 
            color image, the CDF is a list of three lists with each list
            representing the CDF for each color channel in BGR order. FOr a 
            grayscale iamge, the CDF will be returned as a 2^N element list, 
            N being the bit depth of the image. 

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0

    """

    # Determine the number of pixel values in the image
    maxCount = 2**bitDepth

    # Check if the image is a color image
    if len(image.shape) == 3:
       
        # Get the number of rows, columns and planes in the image
        rows, cols, planes = image.shape

        # Determine the number of pixels in the image
        numPixels = rows*cols

        # Create the histogram with BGR color channels
        h = numpy.array([[0]*maxCount, [0]*maxCount, [0]*maxCount])

        # Iterate through each color channel and get the histogram for each
        for plane in range(planes):
            h[plane] = cv2.calcHist([image], [plane], None, [maxCount],\
                                     [0, maxCount]).reshape(-1)

        # Generate the PDF and CDF for the image
        pdf = h/numPixels
        cdf = numpy.cumsum(pdf, axis=1)

    # Image is grayscale if previous check is not met
    else:
        
        # Get the number of rows and columns in the image
        rows, cols = image.shape

        # Determine the number of pixels in the image
        numPixels = rows*cols

        # Get the histogram for the image and generate the PDF and CDF for 
        # the image
        h = cv2.calcHist([image], [0], None, [maxCount], [0, maxCount])
        pdf = h/numPixels
        cdf = numpy.cumsum(pdf)

    # Convert each output to a list
    h = h.tolist()
    pdf = pdf.tolist()
    cdf = cdf.tolist()

    return h, pdf, cdf

if __name__ == '__main__':

    import cv2
    import ipcv
    import time

    # A greyscale test image
    filename = 'crowd.jpg'
    # A 3-channel color test image
    filename = 'lenna.tif'

    im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    print('Data type = {0}'.format(type(im)))
    print('Image shape = {0}'.format(im.shape))
    print('Image size = {0}'.format(im.size))
    
    dataType = str(im.dtype)
    imType = {'uint8':8, 'uint16':16, 'uint32':32}

    startTime = time.time()
    h, pdf, cdf = ipcv.histogram(im, bitDepth=imType[dataType])
    print('Elasped time = {0} [s]'.format(time.time() - startTime))

# The follow will produce a figure containing color-coded plots of the 
# computed histogram, probability function (PDF), and cumulative density
# function (CDF)

    import matplotlib.pyplot
    import matplotlib.backends.backend_agg
    
    maxCount = 2**imType[dataType]
    bins = list(range(maxCount))

    figure = matplotlib.pyplot.figure('Histogram')
    canvas = matplotlib.backends.backend_agg.FigureCanvas(figure)
    
    histAxes = figure.add_subplot(3, 1, 1)
    pdfAxes = figure.add_subplot(3, 1, 2)
    cdfAxes = figure.add_subplot(3, 1, 3)

    if len(im.shape) == 3:

        histAxes.set_ylabel('Number of Pixels')
        histAxes.set_xlim([0, maxCount - 1])
        histAxes.plot(bins, h[0], 'b', \
                      bins, h[1], 'g', \
                      bins, h[2], 'r')

        pdfAxes.set_ylabel('PDF')
        pdfAxes.set_xlim([0, maxCount - 1])
        pdfAxes.plot(bins, pdf[0], 'b', \
                     bins, pdf[1], 'g', \
                     bins, pdf[2], 'r')

        cdfAxes.set_xlabel('Digital Count')
        cdfAxes.set_ylabel('CDF')
        cdfAxes.set_xlim([0, maxCount - 1])
        cdfAxes.plot(bins, cdf[0], 'b', \
                     bins, cdf[1], 'g', \
                     bins, cdf[2], 'r')

    else:
        histAxes.set_ylabel('Number of Pixels')
        histAxes.set_xlim([0, maxCount - 1])
        histAxes.plot(bins, h, 'k')

        pdfAxes.set_ylabel('PDF')
        pdfAxes.set_xlim([0, maxCount - 1])
        pdfAxes.plot(bins, pdf, 'k')

        cdfAxes.set_xlabel('Digital Count')
        cdfAxes.set_ylabel('CDF')
        cdfAxes.set_xlim([0, maxCount - 1])
        cdfAxes.plot(bins, cdf, 'k')
                
    matplotlib.pyplot.show()

