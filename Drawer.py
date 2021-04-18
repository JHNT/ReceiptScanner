import cv2
import numpy as np
import OCRScanner2


def get_word_boundaries(word):
    b = []
    for l in word:
        if b == []:
            b = [l[1], l[2], l[3], l[4]]
            continue
        if l[1] < b[0]:
            b[0] = l[1]
        if l[2] < b[1]:
            b[1] = l[2]
        if l[3] > b[2]:
            b[2] = l[3]
        if l[4] > b[3]:
            b[3] = l[4]
    return b


def draw_letters(img, letters, show_text=True):
    img_letters = img.copy()
    for letter in letters:
        l, x1, y1, x2, y2 = letter
        img_letters = cv2.rectangle(img_letters, (x1,y1), (x2,y2), (0,0,255), 1)
        if show_text:
            cv2.putText(img_letters, l, (x1, y2), None, 2, (255,0,0), 2)
    return img_letters


def draw_lines(img, lines):
    # draw lines
    img_lines = img.copy()
    for line in lines:
        line = sorted(line, key=lambda x: x[1])
        b = get_word_boundaries(line)
        cv2.rectangle(img_lines, (b[0],b[1]), (b[2],b[3]), (0,0,255), 2)
        cv2.putText(img_lines, OCRScanner2.get_word_text(line), (b[0], b[3]), None, 2, (255, 0, 0), 2)
    return img_lines


def draw_words(img, word_lines):
    img_words = img.copy()
    for wl in word_lines:
        for w in wl:
            c_w = ""
            b = get_word_boundaries(w)
            for l in w:
                c_w = c_w + l[0]
            cv2.rectangle(img_words, (b[0], b[1]), (b[2], b[3]), (0,255,0), 2)
            cv2.putText(img_words, c_w, (b[0], b[3]), None, 1, (255,0,0), 2)
    return img_words


def draw_blocks(img, blocks):
    # draw blocks
    img_blocks = img.copy()
    for block in blocks:
        if len(block) < 1:
            continue
        x1 = block[0][0][1]
        y1 = block[0][0][2]
        x2 = block[-1][-1][3]
        y2 = block[-1][-1][4]
        cv2.rectangle(img_blocks, (x1, y1), (x2, y2), (255, 0, 0), 3)
    return img_blocks


def draw_product_blocks(img_product_blocks, product_blocks):
    for product_block in product_blocks:
        product = product_block[0]
        block = product_block[1]
        b = OCRScanner2.get_block_boundaries(block)
        cv2.rectangle(img_product_blocks, (b[0], b[1]), (b[2], b[3]), (255, 0, 0), 3)
        cv2.putText(img_product_blocks, product, (b[0], b[3]), None, 2, (0,255,0), 3)
    return img_product_blocks


def stack_images(scale, imgArray, lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c * eachImgWidth, eachImgHeight * d),
                              (c * eachImgWidth + len(lables[d][c]) * 13 + 27, 30 + eachImgHeight * d), (255, 255, 255),
                              cv2.FILLED)
                cv2.putText(ver, lables[d][c], (eachImgWidth * c + 10, eachImgHeight * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 5, (255, 0, 255), 2)
    return ver