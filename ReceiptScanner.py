import cv2
from OCRScanner import ScannerData
from ProductFinder import ProductFinder


# takes a block from pytesseract image_to_data result and returns the x and y borders
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


# takes a data block from pytesseract image_to_data result and returns the text
def get_data_block_text(block):
    block_text = ""
    for word in block:
        if block_text:
            block_text = block_text + " "
        block_text = block_text + word[-1]
    return block_text


class ReceiptScanner:
    def __init__(self, path_products):
        self.scanner = ScannerData()
        self.product_finder = ProductFinder(path_products)

    def get_product_entries_from_block_lines(self, block_lines, rec_name=None, img=None, debug=False):
        product_entries = []
        if img.any():
            img_products = img.copy()
        first_product = False
        products_x_start = -1

        # loop threw all lines and blocks
        for line in block_lines:
            for block in line:
                b = get_data_block_boundaries(block)
                block_text = get_data_block_text(block)

                # Check if block is a product
                product = self.product_finder.match_product(block_text)
                if product != "no match":
                    if products_x_start == -1:
                        products_x_start = b[0]
                    first_product = True
                    product_entry = [product, 1, "Stk"]
                    product_entries.append(product_entry)
                    # save the boundaries of the last product to check if an amount is associated with the product
                    lp_b = b
                    if debug:
                        print("block_text: " + block_text + " - is product: " + product)
                    if img.any():
                        cv2.rectangle(img_products, (b[0], b[1]), (b[2], b[3]), (0, 255, 0), 2)
                        cv2.putText(img_products, block_text, (b[0], b[3]), None, 2, (0, 255, 0), 6)
                    continue

                # Check if block is amount of a product
                # TODO: Add Regex check for prices
                if ("Stk" in block_text or "kg" in block_text) and first_product:
                    # Check if this is a price / kg block
                    if "EUR/kg" in block_text:
                        if debug:
                            print("block_text: " + block_text + " - is price / kg")
                        if img.any():
                            cv2.rectangle(img_products, (b[0], b[1]), (b[2], b[3]), (0, 255, 0), 2)
                            cv2.putText(img_products, block_text, (b[0], b[3]), None, 2, (0, 255, 0), 6)
                        continue
                    # check if amount is near the last product on y axis
                    # if there are multiple lines between the last product and the amount then continue
                    if b[1] > lp_b[3] + b[3] - b[1]:
                        continue
                    amount = block_text.split(" ")[0]
                    # get the unit
                    if "Stk" in block_text:
                        unit = "Stk"
                    if "kg" in block_text:
                        unit = "kg"
                    if first_product:
                        product_entries[-1][1] = amount
                        product_entries[-1][2] = unit
                    if debug:
                        print("block_text: " + block_text + " - is amount: " + amount + " untit: " + unit)
                    if img.any():
                        cv2.rectangle(img_products, (b[0], b[1]), (b[2], b[3]), (0, 255, 0), 2)
                        cv2.putText(img_products, block_text, (b[0], b[3]), None, 2, (0, 255, 0), 6)
                    continue
                if debug:
                    print("block_text: " + block_text + " - no product")
                if img.any():
                    img_products = cv2.rectangle(img_products, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 3)
                    cv2.putText(img_products, block_text, (b[0], b[3]), None, 2, (0, 0, 255), 3)
        if img.any():
            cv2.imwrite("Resources/Receipts/Results/" + rec_name + ".jpg", img_products)
        return product_entries

    def scan_product_entries(self, img, rec_name, debug=False):
        block_lines = self.scanner.scan_receipt(img)
        receipt_entries = self.get_product_entries_from_block_lines(block_lines, rec_name, img, debug)
        return receipt_entries