# Requirements - opencv-python , depthai-sdk

import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)

xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')

# Properties
monoLeft.setCamera("left")
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
monoRight.setCamera("right")
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)

# Linking
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the grayscale frames from the outputs defined above
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)

    while True:
        # Instead of get (blocking), we use tryGet (non-blocking) which will return the available data or None otherwise
        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()

        if inLeft is not None:
            cv2.imshow("left", inLeft.getCvFrame())

        if inRight is not None:
            cv2.imshow("right", inRight.getCvFrame())

        key = cv2.waitKey(1)
        if key == ord('c'):
            cv2.imwrite('./left_frame.png', inLeft.getCvFrame())
            cv2.imwrite('./right_frame.png', inRight.getCvFrame())
            print("Captured frames from left and right cameras.")
        if key == ord('q'):
            break
