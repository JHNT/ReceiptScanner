import cv2


def preprocess_image(img):
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return img

def preprocess_image2(img):
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return img