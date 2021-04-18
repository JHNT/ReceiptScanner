#read all products
def get_products(path):
    products = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            products.append(line.split('\n')[0])
    return products