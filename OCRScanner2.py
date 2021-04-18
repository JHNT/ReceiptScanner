import pytesseract
import ImagePreProcessor


def get_letters_from_image(img):
    # get boxes
    boxes = pytesseract.image_to_boxes(img, lang="deu", config="--psm 6").split("\n")
    img_h = img.shape[0]
    # boxes -> letters
    letters = []
    for box in boxes:
        letter = [1, 2, 3, 4, 5]
        b = box.split(" ")
        if len(box) < 4:
            continue
        letter[0] = b[0]
        letter[1] = int(b[1])
        letter[2] = img_h - int(b[4])
        letter[3] = int(b[3])
        letter[4] = img_h - int(b[2])
        letters.append(letter)
    return letters


def check_letter_near_boundary(letter, boundaries, avg_w):
    l_x1 = letter[1]
    l_y1 = letter[2]
    l_x2 = letter[3]
    l_y2 = letter[4]
    b_x1 = boundaries[0]
    b_y1 = boundaries[1]
    b_x2 = boundaries[2]
    b_y2 = boundaries[3]

    if l_y2 < b_y1:
        return False
    if l_y1 > b_y2:
        return False
    if l_x2 < b_x1 - avg_w:
        return False
    if l_x1 > b_x2 + avg_w:
        return False
    return True


def get_avg_char_w(letters):
    t = 0
    for letter in letters:
        w = letter[3] - letter[1]
        t = t + w
    return int(t / len(letters))


def get_avg_char_h(letters):
    t = 0
    for letter in letters:
        w = letter[4] - letter[2]
        t = t + w
    return int(t / len(letters))


def get_lines_from_letters(letters):
    letters = sorted(letters, key=lambda x: x[4])  # sort letters with ascending upper y boundary
    c_l = []  # boundaries of current line
    line = []  # list for letters of current line
    lines = []  # list for all lines
    for letter in letters:  # loop threw all letters
        # get position of letter
        l_x1 = letter[1]
        l_y1 = letter[2]
        l_x2 = letter[3]
        l_y2 = letter[4]

        if not c_l:  # check if first line
            c_l = [l_y1, l_y2, l_x1, l_x2]
        elif l_y1 > c_l[1]:  # check if upper boundary of letter is lower than current line boundaries (y is descending) -> new line
            lines.append(line)
            line = []
            c_l = [l_y1, l_y2, l_x1, l_x2]
        line.append(letter)
    lines.append(line)
    return lines


def get_word_boundaries(word):
    b = []
    for l in word:
        if not b:
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


def get_block_boundaries(block):
    b = []
    for word in block:
        b_w = get_word_boundaries(word)
        if not b:
            b = b_w
        if b_w[0] < b[0]:
            b[0] = b_w[0]
        if b_w[1] < b[1]:
            b[1] = b_w[1]
        if b_w[2] > b[2]:
            b[2] = b_w[2]
        if b_w[3] > b[3]:
            b[3] = b_w[3]
    return b


def get_words_from_letters(scanned_letters):
    letters = scanned_letters.copy()
    words = []
    word = []
    avg_w = get_avg_char_w(letters)
    for letter in letters:
        word.append(letter)
        letters.remove(letter)
        b = get_word_boundaries(word)
        while word: # loop threw all letters until no new letters are near the word, if there are no new letter near the word, word is set to []
            b = get_word_boundaries(word)
            found = False
            for letter2 in letters:
                if check_letter_near_boundary(letter2, b, avg_w):
                    found = True
                    word.append(letter2)
                    letters.remove(letter2)
                    b = get_word_boundaries(word)
                    break
            if not found:
                words.append(word)
                word = []
    return words


def get_word_text(word):
    text = ""
    for letter in word:
        text = text + letter[0]
    return text


def get_words_from_line(line, char_w):
    word = []
    words = []
    line = sorted(line, key=lambda x: x[1])
    x = 0
    for letter in line:
        if not word:
            word.append(letter)
            x = letter[3]
            continue
        if letter[1] > x + char_w:
            words.append(word)
            word = [letter]
        else:
            word.append(letter)
        x = letter[3]
    words.append(word)
    return words


def get_word_lines_from_lines(lines, avg_w):
    # get words from lines
    word_lines = []
    for line in lines:
        words = get_words_from_line(line, avg_w)
        word_lines.append(words)
    return word_lines


def get_blocks_from_words(word_lines, avg_w):
    blocks = []
    block = []
    for w_l in word_lines:
        l_x = -1  # x end of last word
        block = []  # current block
        for word in w_l:
            b = get_word_boundaries(word)
            if l_x == -1:
                l_x = b[2]
            if b[0] > l_x + avg_w * 3:  # check if new word
                blocks.append(block)
                block = []
            l_x = b[2]
            block.append(word)
        blocks.append(block)
        block = []
    if block:
        blocks.append(block)
    return blocks


def get_block_text(block):
    block_text = ""
    for word in block:
        if block_text != "":
            block_text = block_text + " "
        block_text = block_text + get_word_text(word)
    return block_text


def get_words_from_image(img):
    letters = get_letters_from_image(img)
    avg_w = get_avg_char_w(letters)
    lines = get_lines_from_letters(letters)
    return get_word_lines_from_lines(lines, avg_w)


def get_blocks_from_image(img):
    letters = get_letters_from_image(img)
    avg_w = get_avg_char_w(letters)
    word_lines = get_words_from_image(img)
    blocks = get_blocks_from_words(word_lines, avg_w)
    return blocks


class ScannerBoxes:
    def scan_receipt(self, img):
        img_pre = ImagePreProcessor.preprocess_image(img)
        blocks = get_blocks_from_image(img_pre)
        return blocks
