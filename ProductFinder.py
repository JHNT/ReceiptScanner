from difflib import SequenceMatcher
import DataReader


class ProductFinder:
    def __init__(self, path):
        self.products = DataReader.get_products(path)

    # find best match for receipt entry in known products
    def match_product(self, product):
        # threshold for match
        th = 0.7
        match = "no match"
        for check in self.products:
            if SequenceMatcher(None, product, check).ratio() > th:
                match = check
                th = SequenceMatcher(None, product, check).ratio()
        return match

