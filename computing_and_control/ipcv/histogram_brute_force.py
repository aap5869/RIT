def histogram(image, bitDepth=8):

    """
    title::
        histogram_brute_force

    description::
        This method will generate the histogram, probability density function, 
        and the cumulative density function for an image. It will use a brute 
        force method using only pure Python to determine each output. 

    attributes::
        image
            (numpy ndarray) An image file that is read in by the cv2.imread 
            function. The image can be either black and white or full color and 
            can have any bit depth. For color images, the color channel order 
            is BGR (blue, green, red).

        bitDepth
            (int [optional]) The bit depth of each color channel of the image.
            Defaults to 8 bits per color channel.

    returns::
        h
            (list) The histogram for the image. For a color image, the 
            histogram is a list of three lists with each list representing the
            histogram for each color channel in BRG order. For a grayscale
            image, the histogram will be returned as a 2^N element list, N
            being the bit depth of the image.

        pdf
            (list) The PDF (probability density function) for the image. For a
            color image, the PDF is a list of three lists with each list
            representing the PDF for each color channel in BGR order. For a 
            grayscale image, the PDF will be returned as a 2^N element list, N
            being the bit depth of the image.

        cdf
            (list) The CDF (cumulative density function) for the image. For a 
            color image, the CDF is a list of three lists with each list
            representing the CDF for each color channel in BGR order. For a 
            graysclae image, the CDF will be returned as a 2^N element list, N
            being the bit depth of the image. 

    author::
        Alex Perkins

    copyright::
        Copyright (C) 2016, Rochester Institute of Technology

    version::
        1.0.0
        
    """

    # Determine number of pixel values in the image
    maxCount = 2**bitDepth

    # Check if the image is a color image
    if len(image.shape) == 3:
        rows, cols, planes = image.shape
    
        # Create the outputs, each containing all zeros for each color channel
        h = [[0]*maxCount, [0]*maxCount, [0]*maxCount]
        pdf = [[0]*maxCount, [0]*maxCount, [0]*maxCount]
        cdf = [[0]*maxCount, [0]*maxCount, [0]*maxCount]

        # Determine the number of pixels in the image
        numPixels = rows*cols

        # Iterate through each row, column, and plane and generate histogram
        # and PDF based on the pixel's value
        for plane in range(planes):
            for row in range(rows):
                for col in range(cols):
                    h[plane][image[row, col, plane]] += 1
                    pdf[plane][image[row, col, plane]] += 1.0/numPixels

    # Image is grayscale there is only one plane 
    else:
        rows, cols = image.shape
        planes = 1

        # Create outputs, each containing all zeros
        h = [[0]*maxCount]
        pdf = [[0]*maxCount]
        cdf = [[0]*maxCount]

        # Determine number of pixels in the image
        numPixels = rows*cols

        # Iterate through each row, column, and plane and generate histogram
        # and PDF based on the pixel's value
        for row in range(rows):
            for col in range(cols):
                h[0][image[row, col]] += 1
                pdf[0][image[row, col]] += 1.0/numPixels

    # Iterate through each plane and the number of pixel values and generate
    # the CDF of the image
    for plane in range(planes):
        for x in range(maxCount):
            cdf[plane][x] = sum(pdf[plane][0:x])

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

    if len(im.shape) > 2:

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
        histAxes.plot(bins, h[0], 'k')

        pdfAxes.set_ylabel('PDF')
        pdfAxes.set_xlim([0, maxCount - 1])
        pdfAxes.plot(bins, pdf[0], 'k')

        cdfAxes.set_xlabel('Digital Count')
        cdfAxes.set_ylabel('CDF')
        cdfAxes.set_xlim([0, maxCount - 1])
        cdfAxes.plot(bins, cdf[0], 'k')
                
    matplotlib.pyplot.show()

