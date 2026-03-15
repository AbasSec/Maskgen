import database
import utils
import os

def menu():
    print("\n--- URL Masking Tool (Research Only) ---")
    print("1. Create Masked URL")
    print("2. View Stored Masks")
    print("3. Start Redirect Server")
    print("4. Exit")
    return input("Select an option: ")

def create_mask():
    target = input("Enter Real Target URL (e.g., https://google.com): ")
    if not utils.is_valid_url(target):
        print("[!] Invalid Target URL format.")
        return

    mask = input("Enter Mask Text (e.g., https://secure-login.net): ")
    code = utils.generate_code()
    
    # Construction: Mask + @ + Local Server
    masked_url = f"{mask}@{ 'localhost:5000' }/{code}"
    
    database.save_link(mask, target, code)
    print(f"\n[+] Link Created successfully!")
    print(f"Generated Masked URL: {masked_url}")
    
    qr_choice = input("Generate QR Code? (y/n): ")
    if qr_choice.lower() == 'y':
        fname = f"qr_{code}.png"
        utils.make_qr(masked_url, fname)
        print(f"[+] QR saved to {fname}")

def list_links():
    links = database.get_all_links()
    print("\nID | Mask | Target | Code | Clicks")
    for l in links:
        print(f"{l[0]} | {l[1]} | {l[2]} | {l[3]} | {l[5]}")

if __name__ == "__main__":
    database.init_db()
    while True:
        choice = menu()
        if choice == '1': create_mask()
        elif choice == '2': list_links()
        elif choice == '3': 
            print("[*] Open a new terminal and run: python redirect_server.py")
        elif choice == '4': break
