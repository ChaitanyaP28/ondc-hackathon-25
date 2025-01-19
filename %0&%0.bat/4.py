import time
import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="debugon",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def fetch_seller_catalogs():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT SellerID, SellerName FROM Sellers")
    sellers = cursor.fetchall()
    seller_catalogs = {}
    for seller in sellers:
        seller_id = seller["SellerID"]
        cursor.execute(f"""
            SELECT p.ProductID, p.ProductName, p.Description, p.Price, c.CategoryName
            FROM Products p
            JOIN Categories c ON p.CategoryID = c.CategoryID
            JOIN ProductInventory pi ON p.ProductID = pi.ProductID
            WHERE pi.SellerID = {seller_id}
        """)
        products = cursor.fetchall()
        seller_catalogs[seller["SellerName"]] = products

    cursor.close()
    connection.close()

    return seller_catalogs

def nxn_query(buyers, sellers):
    results = []
    for buyer in buyers:
        for seller in sellers:
            print(f"Buyer {buyer} querying Seller {seller}")
            results.append(sellers[seller])
    return results

def n_plus_n_query(buyers):
    seller_catalogs = fetch_seller_catalogs()
    gcr = consolidate_catalogs(seller_catalogs)
    results = []
    for buyer in buyers:
        print(f"Buyer {buyer} querying the Global Catalog Repository (GCR)")
        results.append(gcr)
    return results

def consolidate_catalogs(sellers):
    all_products = []
    for seller, catalog in sellers.items():
        for product in catalog:
            all_products.append(product)
    return all_products

buyers = ["Buyer A", "Buyer B", "Buyer C"]

start_time = time.time()
seller_catalogs = fetch_seller_catalogs()
nxn_results = nxn_query(buyers, seller_catalogs)
end_time = time.time()
print("\nTime taken for NxN Model: ", end_time - start_time)

start_time = time.time()
n_plus_n_results = n_plus_n_query(buyers)
end_time = time.time()
print("\nTime taken for N+N Model: ", end_time - start_time)

print("\nResults of NxN Query:")
for result in nxn_results:
    for product in result:
        print(product)

print("\nResults of N+N Query:")
for result in n_plus_n_results:
    for product in result:
        print(product)
