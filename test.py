import cv2
from ReceiptScanner import ReceiptScanner
import ImagePreProcessor

#get test data
def get_receipt_test_data(path):
    receipts_testdata = []
    with open(path) as file:
        lines = file.readlines()
        receipt_test_products = []
        receipt_test_name = ""
        for line in lines:
            if "receipt" in line:
                if receipt_test_products != []:
                    receipt_test = [receipt_test_name, receipt_test_products]
                    receipts_testdata.append(receipt_test)
                    receipt_test_products = []
                receipt_test_name = line.split('\n')[0]
            else:
                receipt_test_products.append(line.split('\n')[0])
        receipt_test = [receipt_test_name, receipt_test_products]
        receipts_testdata.append(receipt_test)
    return receipts_testdata
def check_scanned_receipt(rec_name, rec_entries):
    result = []
    for receipt in test_data:
        if receipt[0] == rec_name:
            for entry in receipt[1]:
                match = False
                if entry in rec_entries:
                    match = True
                    result.append(entry, match)
                if match:
                    break
    return result
receipts_testdata_path = "Resources/Receipts/receipts.txt"
test_data = get_receipt_test_data(receipts_testdata_path)





products_path = "Resources/Receipts/products.txt"
receipt_images_path = "Resources/Receipts/Penny/"

receipt_scanner = ReceiptScanner(products_path)


# loop threw all 42 receipt images
count = 3
counter = 0
for i in range(1, count + 1):
    # get receipt name
    f = str(i)
    if i < 10:
        f = "0" + f
    rec_name = "penny_" + f
    rec_image_path = receipt_images_path + rec_name + ".jpg"
    rec_image = cv2.imread(rec_image_path)

    img_pre = ImagePreProcessor.preprocess_image(rec_image)
    cv2.imwrite("Resources/Receipts/Preprocessing/" + rec_name + ".jpg", img_pre)

    # get receipt_products
    receipt_products = receipt_scanner.scan_product_entries(rec_image, rec_name)
    result = check_scanned_receipt(rec_name, receipt_products)

    # print progress
    if i % 10 == 0:
        print(str(i), "receipts scanned")


