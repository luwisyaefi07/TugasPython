# LATIHAN 2.1

file_path = 'data.txt'
dict_list = [] # List untuk menampung semua dictionary

try:
    with open(file_path, 'r') as file:
        header = file.readline().strip()
        print(f"Header: {header.split(',')}") #baca baris header secara terpisah.
        print("---"*30)
        print("---Produk dan Kuantitas:")
        for line in file:
            data = line.strip().split(',')
            product = data[0]
            quantity = int(data[1])   # konversi ke integer
            price = float(data[2])    # konversi ke float

                # Simpan ke dictionary
            record = {
                    'Product': product,
                    'Quantity': quantity,
                    'Price': price
                }

            dict_list.append(record)  # Tambahkan ke list

            print(f"Product: {product}, Quantity: {quantity}")  # Cetak hasil per baris

except FileNotFoundError:
    print(f"Error: File {file_path} tidak ditemukan.")
print("---"*30)
print("Seluruh data dalam bentuk list of dictionary:")
for item in dict_list:
    print(item)
print("---"*30)