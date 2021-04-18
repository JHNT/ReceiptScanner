import pytesseract
import ImagePreProcessor


def get_data_block_boundaries(block):
    b = []
    for word in block:
        x1 = int(word[6])
        y1 = int(word[7])
        x2 = x1 + int(word[8])
        y2 = y1 + int(word[9])
        if not b:
            b = [x1, y1, x2, y2]
        if x1 < b[0]:
            b[0] = x1
        if y1 < b[1]:
            b[1] = y1
        if x2 > b[2]:
            b[2] = x2
        if y1 > b[3]:
            b[3] = y2
    return b


def get_data_block_text(block):
    block_text = ""
    for word in block:
        if block_text:
            block_text = block_text + " "
        block_text = block_text + word[-1]
    return block_text


def get_lines_from_data(data):
    lines = []
    line = []
    for d in data:
        if d[0] == "level":
            continue
        if d[-1] != "":
            line.append(d)
        if d[-1] == "" and line:
            lines.append(line)
            line = []
    return lines


def get_blocks_from_lines(lines):
    lines_block= []
    for line in lines:
        blocks = []
        block = []
        word_end = 0
        # loop threw all words in the line
        for word in line:
            # get coordination of word
            x1 = int(word[6])
            y1 = int(word[7])
            x2 = x1 + int(word[8])
            y2 = y1 + int(word[9])
            # get average char width of word
            avg_char_w = int((x2 - x1) / len(word[-1]))
            # if first word in line set word end, word end is used to check if the next word belongs to the same block
            if word_end == 0:
                word_end = x2
            # check if word belongs to the same block
            if x1 > word_end + avg_char_w * 2:
                blocks.append(block)
                block = []
            block.append(word)
            word_end = x2
        blocks.append(block)
        lines_block.append(blocks)
    return lines_block


class ScannerData:

    def scan_receipt(self, img):
        img_pre = ImagePreProcessor.preprocess_image2(img)
        d = pytesseract.image_to_data(img_pre, lang="deu", config="--psm 6").split("\n")
        data = []
        for row in d:
            data.append(row.split("\t"))
        lines = get_lines_from_data(data)
        block_lines = get_blocks_from_lines(lines)
        return block_lines
