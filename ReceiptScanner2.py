from OCRScanner2 import ScannerBoxes
from ProductFinder import ProductFinder


# takes a block structured in words
def get_block_text(block):
    block_text = ""
    for word in block:
        if block_text != "":
            block_text = block_text + " "
        block_text = block_text + get_word_text(word)
    return block_text


# function for boxes
def get_word_text(word):
    text = ""
    for letter in word:
        text = text + letter[0]
    return text


class ReceiptScanner2:
    def __init__(self, path_products):
        self.scanner = ScannerBoxes()
        self.product_finder = ProductFinder(path_products)

    def get_product_entries_from_blocks(self, blocks):
        receipt_entries = []
        for block in blocks:
            block_text = get_block_text(block)
            product = self.match_product(block_text)
            if product != "no match":
                receipt_entries.append(product)
        return receipt_entries

    def scan_receipt(self, img):
        blocks = self.scanner.scan_receipt(img)
        receipt_entries = self.get_product_entries_from_blocks(blocks)
        return receipt_entries
