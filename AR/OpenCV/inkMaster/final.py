import cv2 as cv2
import numpy as np
import imutils


def main():
    template1 = cv2.imread("C:\\Users\\Manthika\\Desktop\\opencvtest\\templates\\template1.jpg")
    template2 = cv2.imread("C:\\Users\\Manthika\\Desktop\\opencvtest\\templates\\temp.jpg")
    templates = [template1, template2]

    for i in range(len(templates)):
        templates[i] = cv2.cvtColor(templates[i], cv2.COLOR_BGR2GRAY)
        templates[i] = cv2.Canny(templates[i], 50, 140)
        templates[i] = cv2.GaussianBlur(templates[i],(5,5),0)
        templates[i] = imutils.resize(templates[i], width=50)

    (tH, tW) = templates[0].shape[:2]
    # print(tH)
    # print(tW)
    # cv2.imshow("Template", template)

    # windowName = "Something"
    # cv2.namedWindow(windowName)
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    # loop over the frames to find the template
    while ret:
        # load the image, convert it to grayscale, and initialize the
        # bookkeeping variable to keep track of the matched region
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = None

        # loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                print("frame is smaller than the template")
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            edged = cv2.Canny(resized, 50, 160)
            blurred = cv2.GaussianBlur(edged,(5,5),0)

            curr_max = 0
            index = 0
            result = None

            # find the best match
            for i in range(len(templates)):
                # perform matchtemplate
                res = cv2.matchTemplate(blurred, templates[i], cv2.TM_CCOEFF)
                # get the highest correlation value of the result
                maxVal = res.max()
                # if the correlation is highest thus far, store the value and index of template
                if maxVal > curr_max:
                    curr_max = maxVal
                    index = i
                    result = res

            print(index)
            # result = cv2.matchTemplate(edged, templates[index], cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then update
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

            # unpack the bookkeeping variable and compute the (x, y) coordinates
            # of the bounding box based on the resized ratio
        # print(found)
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        cropped = frame[startY:endY, startX:endX]
        # cv2.imshow("cropped", cropped)

        # Read the foreground image with alpha channel
        foreGroundImage = cv2.imread("C:\\Users\\Manthika\\Desktop\\opencvtest\\tattoo2.png", -1)
        # Read background image
        background = cropped
        dim = (background.shape[1], background.shape[0])
        foreGroundImage = cv2.resize(foreGroundImage, dim, interpolation = cv2.INTER_AREA)

        # Split png foreground image
        a = foreGroundImage[:, :, 3]

        # Save the foregroung RGB content into a single object
        foreground = foreGroundImage[:, :, 0:3]

        # Save the alpha information into a single Mat
        alpha = cv2.merge((a, a, a))

        # background = cv2.resize(background, dim, interpolation = cv2.INTER_AREA)

        # Convert uint8 to float
        foreground = foreground.astype(float)
        background = background.astype(float)
        alpha = alpha.astype(float) / 255

        # Perform alpha blending
        foreground = cv2.multiply(alpha, foreground)
        beta = 1.0 - alpha
        background = cv2.multiply(beta, background)
        outImage = cv2.add(foreground, background)
        outImage = outImage/255
        print(outImage.shape)

        data = outImage.copy()
        data = data / data.max()  # normalizes data in range 0 - 255
        data = 255 * data
        converted = data.astype(np.uint8)

        # Read source image.
        im_src = converted.copy()
        size = im_src.shape

        # Create a vector of source points.
        pts_src = np.array(
            [
                [0, 0],
                [size[1] - 1, 0],
                [size[1] - 1, size[0] - 1],
                [0, size[0] - 1]
            ], dtype=float
        )

        # Read destination image
        im_dst = frame.copy()

        # Create a vector of destination points.
        pts_dst = np.array(
            [
                [startX, startY],
                [endX, startY],
                [endX, endY],
                [startX, endY]
            ]
        )

        # Calculate Homography between source and destination points
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image
        im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))

        # Black out polygonal area in destination image.
        cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

        # Add warped source image to destination image.
        im_dst = im_dst + im_temp

        cv2.imshow("Final", im_dst)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()