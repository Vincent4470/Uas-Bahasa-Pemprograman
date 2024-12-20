import json
import os
from datetime import datetime

inventory = {}
password1 = "owner"
password2 = "kasir"
struk_counter = 1  # Counter for struk filenames

def save_inventory():
    with open("inventory.json", "w") as file:
        json.dump(inventory, file)

def load_inventory():
    global inventory, struk_counter
    try:
        with open("inventory.json", "r") as file:
            inventory = json.load(file)
    except FileNotFoundError:
        inventory = {}
    
    # Load the struk counter from a file
    try:
        with open("struk_counter.txt", "r") as file:
            struk_counter = int(file.read().strip())
    except FileNotFoundError:
        struk_counter = 1

def save_struk_counter():
    with open("struk_counter.txt", "w") as file:
        file.write(str(struk_counter))

def owner_mode():
    while True:
        print("\n-- Mode Pemilik Toko --")
        print("1. Input Barang Masuk")
        print("2. Lihat Inventaris")
        print("3. Hapus Barang")
        print("4. Hapus Stok Barang")
        print("5. Keluar")
        choice = input("Pilih: ")

        if choice == "1":
            while True:
                num_items_input = input("Berapa banyak barang yang ingin diinput? (atau ketik 'kembali' untuk kembali): ").strip()
                if num_items_input.lower() == 'kembali':
                    break
                try:
                    num_items = int(num_items_input)
                    if num_items < 0:
                        raise ValueError
                    for _ in range(num_items):
                        item = input("Masukkan nama barang: ").strip()
                        price = float(input("Masukkan harga barang: "))
                        stock = int(input("Masukkan stok barang: "))
                        inventory[item] = {"price": price, "stock": stock}
                    save_inventory()
                    print("Barang-barang telah ditambahkan.")
                except ValueError:
                    print("Input tidak valid. Silakan masukkan jumlah yang benar.")
                continue_input = input("Apakah Anda ingin menginput barang lagi? (ya/tidak): ").strip().lower()
                if continue_input != 'ya':
                    break

        elif choice == "2":
            print("\n-- Inventaris --")
            for i, (item, details) in enumerate(inventory.items(), start=1):
                print(f"{i}. {item}: Harga = Rp{details['price']}, Stok = {details['stock']}")

        elif choice == "3":
            while True:
                item = input("Masukkan nama barang yang ingin dihapus (atau ketik 'kembali' untuk kembali): ").strip()
                if item.lower() == 'kembali':
                    break
                if item in inventory:
                    del inventory[item]
                    save_inventory()
                    print("Barang telah dihapus.")
                else:
                    print("Barang tidak ditemukan dalam inventaris.")
                continue_delete = input("Apakah Anda ingin menghapus barang lain? (ya/tidak): ").strip().lower()
                if continue_delete != 'ya':
                    break

        elif choice == "4":
            while True:
                item = input("Masukkan nama barang yang ingin dikurangi stoknya (atau ketik 'kembali' untuk kembali): ").strip()
                if item.lower() == 'kembali':
                    break
                if item in inventory:
                    try:
                        stock_to_remove = int(input("Masukkan jumlah stok yang ingin dihapus: "))
                        if stock_to_remove <= inventory[item]["stock"]:
                            inventory[item]["stock"] -= stock_to_remove
                            if inventory[item]["stock"] == 0:
                                del inventory[item]
                                print(f"Stok {item} telah habis, barang dihapus dari inventaris.")
                            save_inventory()
                            print("Stok barang telah dikurangi.")
                        else:
                            print("Stok yang ingin dihapus melebihi stok yang tersedia.")
                    except ValueError:
                        print("Input tidak valid. Silakan masukkan jumlah yang benar.")
                else:
                    print("Barang tidak ditemukan dalam inventaris.")
                continue_remove_stock = input("Apakah Anda ingin menghapus atau mengurangi stok barang lain? (ya/tidak): ").strip().lower()
                if continue_remove_stock != 'ya':
                    break

        elif choice == "5":
            break

        else:
            print("Pilihan tidak valid.")

def cashier_mode():
    cart = []
    while True:
        print("\n-- Mode Penjaga Kasir --")
        print("1. Tambah Item ke Keranjang")
        print("2. Lihat Keranjang")
        print("3. Hitung Total + PPN")
        print("4. Bayar")
        print("5. Keluar")
        choice = input("Pilih: ")

        if choice == "1":
            while True:
                print("\n-- Daftar Barang --")
                for i, (item, details) in enumerate(inventory.items(), start=1):
                    print(f"{i}. {item}: Harga = Rp{details['price']}, Stok = {details['stock']}")
                item_index = input("Masukkan nomor barang yang ingin ditambahkan (atau ketik 'kembali' untuk kembali): ").strip()
                if item_index.lower() == 'kembali':
                    break
                item_index = int(item_index) - 1
                if 0 <= item_index < len(inventory):
                    item = list(inventory.keys())[item_index]
                    quantity = int(input("Masukkan jumlah: "))
                    if quantity <= inventory[item]["stock"]:
                        inventory[item]["stock"] -= quantity
                        cart.append((item, quantity, inventory[item]["price"]))
                        print("Item telah ditambahkan ke keranjang.")
                        if inventory[item]["stock"] == 0:
                            print(f"Stok {item} telah habis, menghapus dari inventaris.")
                            del inventory[item]
                        save_inventory()
                    else:
                        print("Stok tidak mencukupi.")
                else:
                    print("Pilihan tidak valid.")
                continue_add = input("Apakah Anda ingin menambah item lain? (ya/tidak): ").strip().lower()
                if continue_add != 'ya':
                    break

        elif choice == "2":
            while True:
                print("\n-- Keranjang --")
                for item, quantity, price in cart:
                    print(f"{item} - Jumlah: {quantity} - Harga: Rp{price} - Total: Rp{quantity * price}")
                remove_item = input("Apakah ada item yang ingin dihapus pada keranjang? (ya/tidak, atau ketik 'kembali' untuk kembali): ").strip().lower()
                if remove_item == 'kembali' or remove_item == 'tidak':
                    break
                elif remove_item == 'ya':
                    item_to_remove = input("Masukkan nama item yang ingin dikurangi dari keranjang: ").strip()
                    for i, (item, quantity, price) in enumerate(cart):
                        if item == item_to_remove:
                            qty_to_remove = int(input(f"Masukkan jumlah yang ingin dihapus dari {item} (maksimal {quantity}): "))
                            if qty_to_remove > quantity:
                                print("Jumlah yang ingin dihapus melebihi jumlah yang ada di keranjang.")
                            else:
                                if qty_to_remove == quantity:
                                    cart.pop(i)
                                else:
                                    cart[i] = (item, quantity - qty_to_remove, price)
                                inventory[item]["stock"] += qty_to_remove
                                save_inventory()
                                print(f"Item {item} telah dikurangi sebanyak {qty_to_remove} dari keranjang.")
                            break
                    else:
                        print("Item tidak ditemukan dalam keranjang.")
                else:
                    print("Pilihan tidak valid.")

        elif choice == "3":
            total = sum(quantity * price for _, quantity, price in cart)
            ppn = total * 0.1
            total_with_ppn = total + ppn
            print(f"Total: Rp{total}")
            print(f"PPN (10%): Rp{ppn}")
            print(f"Total dengan PPN: Rp{total_with_ppn}")

        elif choice == "4":
            while True:
                total = sum(quantity * price for _, quantity, price in cart)
                ppn = total * 0.1
                total_with_ppn = total + ppn
                print(f"Total yang harus dibayar (dengan PPN): Rp{total_with_ppn}")
                amount = input("Masukkan nominal pembayaran (atau ketik 'kembali' untuk kembali): ").strip()
                if amount.lower() == 'kembali':
                    break
                amount = float(amount)
                kembalian = amount - total_with_ppn
                if amount >= total_with_ppn:
                    print("Pembayaran berhasil. Menunggu konfirmasi Penjaga Kasir.")
                    if confirm_payment():
                        print("Pembayaran telah dikonfirmasi. Struk sedang dicetak...")
                        print_receipt(cart, total, ppn, total_with_ppn, kembalian, amount)
                        cart.clear()  # Clear the cart after successful payment
                    else:
                        print("Pembayaran ditolak oleh kasir toko.")
                else:
                    print("Nominal pembayaran kurang. Pembayaran gagal.")
                break

        elif choice == "5":
            break

        else:
            print("Pilihan tidak valid.")

def confirm_payment():
    while True:
        print("\n-- Konfirmasi Pembayaran --")
        pwd = input("Masukkan password Penjaga Kasir untuk konfirmasi pembayaran: ")
        if pwd == password2:
            confirmation = input("Konfirmasi Transaksi (ya/tidak): ").strip().lower()
            if confirmation == "ya":
                return True
            elif confirmation == "tidak":
                return False
            else:
                print("Pilihan tidak valid. Masukkan 'ya' atau 'tidak'.")
        else:
            print("Password salah. Coba lagi.")

def print_receipt(cart, total, ppn, total_with_ppn, kembalian, amount):
    global struk_counter
    filename = f"struk{struk_counter}.txt"
    struk_counter += 1
    save_struk_counter()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "w") as file:
        file.write(f"-- Struk Belanja ({timestamp}) --\n")
        for item, quantity, price in cart:
            file.write(f"{item} - Jumlah: {quantity} - Harga: Rp{price} - Total: Rp{quantity * price}\n")
        file.write(f"\nTotal: Rp{total}\n")
        file.write(f"PPN (10%): Rp{ppn}\n")
        file.write(f"Total dengan PPN: Rp{total_with_ppn}\n")
        file.write(f"Jumlah uang yang dibayar: Rp{amount}\n")
        file.write(f"Kembalian: Rp{kembalian}\n") 
    print(f"Struk telah dicetak ke {filename}.\n")

    # Append to history file
    with open("history.txt", "a") as history_file:
        history_file.write(f"-- Struk Belanja ({timestamp}) --\n")
        for item, quantity, price in cart:
            history_file.write(f"{item} - Jumlah: {quantity} - Harga: Rp{price} - Total: Rp{quantity * price}\n")
        history_file.write(f"\nTotal: Rp{total}\n")
        history_file.write(f"PPN (10%): Rp{ppn}\n")
        history_file.write(f"Total dengan PPN: Rp{total_with_ppn}\n")
        history_file.write(f"Jumlah uang yang dibayar: Rp{amount}\n")
        history_file.write(f"Kembalian: Rp{kembalian}\n\n")

def main():
    load_inventory()
    while True:
        print("\n-- Menu Utama --")
        print("1. Masuk sebagai Pemilik Toko")
        print("2. Masuk sebagai Penjaga Kasir")
        print("3. Keluar")
        choice = input("Pilih: ")

        if choice == "1":
            pwd = input("Masukkan password: ")
            if pwd == password1:
                owner_mode()
            else:
                print("Password salah.")
        elif choice == "2":
            cashier_mode()
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
