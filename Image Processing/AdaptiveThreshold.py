import cv2
import DataReader

def nothing(e):
    pass


def initTrackBars():
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 360, 240)
    cv2.createTrackbar("Blur Size", "TrackBars", 3, 15, nothing)
    cv2.createTrackbar("Blur Iterations", "TrackBars", 1, 10, nothing)
    cv2.createTrackbar("Threshold", "TrackBars", 150, 255, nothing)
    cv2.createTrackbar("Block Size", "TrackBars", 3, 20, nothing)
    cv2.createTrackbar("C", "TrackBars", 3, 150, nothing)


def valTrackbars():
    blur_s = cv2.getTrackbarPos("Blur Size", "TrackBars")
    if blur_s % 2 == 0:
        blur_s = blur_s + 1
    blur_i = cv2.getTrackbarPos("Blur Iterations", "TrackBars")
    thres0 = cv2.getTrackbarPos("Threshold", "TrackBars")
    thres1 = cv2.getTrackbarPos("Block Size", "TrackBars")
    if thres1 % 2 == 0:
        thres1 = thres1 + 1
    thres2 = cv2.getTrackbarPos("C", "TrackBars")
    print(thres1)
    return blur_s, blur_i, thres0, thres1, thres2

initTrackBars()

while True:
    img = cv2.imread("../Resources/Receipts/Rewe/receipt_35.jpg")
    img = img[800:2000]
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b_s, b_i, a, b, c = valTrackbars()
    imgBlur = cv2.GaussianBlur(imgGray, (b_s, b_s), b_i)
    thresh1 = cv2.adaptiveThreshold(imgBlur, a, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, b, c)
    thresh2 = cv2.adaptiveThreshold(imgBlur, a, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, b, c)
    imgArray = [[img, imgBlur], [thresh1, thresh2]]
    labels = [["Orginal", "Blur"], ["ADAPT", "ADAPT GAUSS"]]
    stacked = DataReader.stackImages(imgArray, 0.3, labels)
    cv2.imshow("Results", stacked)
    cv2.waitKey(1)