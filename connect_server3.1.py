import paramiko

HOSTNAME = "5.189.154.248"
PORT = 22
USERNAME = "heri"
PASSWORD = "Passwd093"


print(f"⏳Menyambungkan ke server SFTP: {HOSTNAME}:{PORT}...")
ssh_client = paramiko.SSHClient()       # buat SSH Client
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
    print("✅ Koneksi SSH berhasil")

    sftp_client = ssh_client.open_sftp()    # connect SFTP
    print("✅ Koneksi SFTP berhasil")

    remote_path = 'uploads/sales_data.csv' # lokasi file
    file_path = './sales_data_download.csv'
    sftp_client.get(remote_path, file_path)

except paramiko.AuthenticationException:
    print(f"Error: Autentifikasi gagal. Cek lagi username dan kata sandi")
except paramiko.SSHException as e:
    print(f"Error: Error koneksi SSH: {e}")
except FileNotFoundError:
    print(f"Error: File tidak ditumkan di server SFTP.")
except Exception as e:
    print("Terjadi Error tak terduga: {e}")

print("---"*30)

try:
    with open('sales_data_download.csv', 'r') as file:
        header = file.readline().strip().split(',')  # baca header
        print(f"Header: {header}")

        # Cek posisi kolom Product dan Quantity (biar fleksibel)
        product_index = header.index('ProductName')
        quantity_index = header.index('QuantitySold')

        # Loop sisa baris
        for line in file:
            values = line.strip().split(',')
            if len(values) >= max(product_index, quantity_index) + 1:
                product = values[product_index]
                quantity = values[quantity_index]
                print(f"Product: {product}, Quantity: {quantity}")

except FileNotFoundError:
    print("File sales_data.csv tidak ditemukan.")
except Exception as e:
    print(f"Terjadi error saat membaca file: {e}")

print("---"*30)

import csv

input_file = 'sales_data_download.csv'
output_file = 'luwi_sales_data_new.csv'

try:
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Total_Amount']  # tambahkan kolom baru

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Hitung total_amount
            quantity = int(row['QuantitySold'])
            price = float(row['Price'])
            total = quantity * price

            row['Total_Amount'] = round(total, 2)
            writer.writerow(row)

    print(f"✅ File baru berhasil dibuat: {output_file}")

except FileNotFoundError:
    print(f"File {input_file} tidak ditemukan.")
except Exception as e:
    print(f"Terjadi error: {e}")

    print("---"*30)
    
    # Upload file
try:
    remote_file = 'uploads/luwi_sales_data_new.csv' # lokasi file
    local_file = './luwi_sales_data_new.csv'

    sftp_client.put(local_file, remote_file)
    print(f"✅ File '{local_file}' berhasil diupload ke '{remote_file}'")


finally:
    if sftp_client:
        sftp_client.close()
        print("📴Sesi SFTP client ditutup")

    if ssh_client:
        ssh_client.close()
        print("📴Sesi SSH client ditutup")
