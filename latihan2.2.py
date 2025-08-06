# LATIHAN 2.2
# dict_list didefinisikan pada code latihan2.1

output_file = 'high_value_products.txt'
data_to_write = [item for item in dict_list if item['Price'] > 100.00] # produk dengan harga > 100.00

try:
    with open(output_file, 'w') as out_file: 
        out_file.write("Product,Price\n")     # Tulis header
        for item in data_to_write:            # Tulis data hasil filter
            out_file.write(f"{item['Product']},{item['Price']}\n")

    print(f"\n{len(data_to_write)} produk dengan harga > 100 berhasil ditulis ke '{output_file}'.")

except Exception as e:
    print(f"Error saat menulis file: {e}")