import paramiko
import csv

class ConnectSFTP:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_client = None
        self.sftp_client = None
    
    def connect(self):
        try:
            self.ssh_client = paramiko.SSHClient()       # buat SSH Client
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=self.hostname, 
                port=self.port, 
                username=self.username, 
                password=self.password
            )
            print("Koneksi SSH berhasil.")

            self.sftp_client = self.ssh_client.open_sftp()
            print("Koneksi SFTP berhasil.")
            

            remote_path = 'uploads/sales_data.csv'      # lokasi file
            file_path = './sales_data_download.csv'
            self.sftp_client.get(remote_path, file_path)

        except paramiko.AuthenticationException:
            print("Autentikasi gagal. Cek username/password.")
        except paramiko.SSHException as e:
            print(f"Error: Error koneksi SSH: {e}")
        except FileNotFoundError:
            print(f"Error: File tidak ditumkan di server SFTP.")
        except Exception as e:
            print(f"Error koneksi SSH: {e}")
        print("---"*30)

    def readfile(self, file_path): 
        try:
            with open(file_path, 'r') as file:
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

    def createfile(self, file_path, output_file):

        try:
            with open(file_path, 'r') as infile, open(output_file, 'w', newline='') as outfile:
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

            print(f"File baru berhasil dibuat: {output_file}.")
            

        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
        except Exception as e:
            print(f"Terjadi error: {e}")

        print("---"*30)
    
    def uploadfile(self, remote_file, output_file):
        try:
            self.sftp_client.put(output_file, remote_file)
            print(f"File '{output_file}' berhasil diupload ke '{remote_file}.'")
        except Exception as e:
            print(f"Terjadi error: {e}")
        print("---"*30)

    def close(self):
        if self.sftp_client:
            self.sftp_client.close()
            print("Sesi SFTP client ditutup.")

        if self.ssh_client:
            self.ssh_client.close()
            print("Sesi SSH client ditutup.")

    
server = ConnectSFTP(
    hostname="5.189.154.248",
    port=22,
    username="heri",
    password="Passwd093"
)

remote_path = 'uploads/sales_data.csv'      # lokasi file 
file_path = './sales_data_download.csv'
output_file = 'luwi_sales_data_new.csv'
remote_file = 'uploads/luwi_sales_data_new.csv' 

server.connect()
server.readfile(file_path)
server.createfile(file_path, output_file)
server.uploadfile( remote_file, output_file)
server.close()