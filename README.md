# README

This project was created to scan grocery shopping receipts. There are two version of the Receipt Scanner
The class "ReceiptScanner" is the more accurate version using the pytesseract image_to_data function. 
It provides a function that takes an image as input and returns a list of product entries [receipt_name, amount, unit] for a receipt.

The class "ReceiptScanner2" uses the image_to_boxes function of pytesseract.
image_to_boxes returns a list of recognized characters with x and y coordinates.
"# ReceiptScanner" 
