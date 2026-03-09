# ══════════════════════════════════════════════════════════
#  Interactive Ping Tool - Python (Windows)
#  Load devices, ping them all, save the report.
# ══════════════════════════════════════════════════════════

# --- IMPORTS ---
import subprocess             # Lets us run the ping command
import json                   # Lets us save/load device lists to a file
import os                     # Lets us check if a file exists on disk
import openpyxl               # Lets us read Excel (.xlsx) files
import datetime               # Lets us timestamp the report file
import tkinter as tk          # Base library needed to use the file dialog
from tkinter import filedialog  # The file explorer popup window


# --- FILE WHERE DEVICES ARE SAVED ---
SAVE_FILE = "../../Downloads/devices.json"

# --- COLOR CODES ---
# ANSI escape codes let us print colored text in the terminal
# \033[92m = green   \033[91m = red   \033[0m = reset back to normal
GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"


# --- FUNCTION: Open file explorer popup ---
def browse_file(title, filetypes):
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return filepath


# --- FUNCTION: Load devices from file ---
def load_devices():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []


# --- FUNCTION: Save devices to file ---
def save_devices(devices):
    with open(SAVE_FILE, "w") as f:
        json.dump(devices, f, indent=2)


# --- FUNCTION: Ping a single device ---
def ping_device(ip):
    command = ["ping", "-n", "2", ip]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


# --- FUNCTION: Add a single device manually ---
def add_device(devices):
    print()
    name = input("  Enter device name (e.g. BR-01-UPS-01) : ").strip()
    ip   = input("  Enter IP address  (e.g. 10.19.1.11)   : ").strip()
    if not name or not ip:
        print("  [!] Name and IP cannot be blank. Device not added.")
        return
    if any(d["ip"] == ip for d in devices):
        print(f"  [!] IP {ip} already exists in the list.")
        return
    devices.append({"name": name, "ip": ip})
    save_devices(devices)
    print(f"  [+] Added: {name} ({ip})")


# --- FUNCTION: Import from a .txt file ---
def import_from_txt(devices):
    print()
    print("  Opening file explorer - select your .txt file...")
    filepath = browse_file(
        title     = "Select your device list (.txt)",
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not filepath:
        print("  [!] No file selected. Cancelled.")
        return
    print(f"  [+] File selected: {filepath}")
    added   = 0
    skipped = 0
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                print(f"  [!] Skipping bad line: {line}")
                skipped += 1
                continue
            name = parts[0].strip()
            ip   = parts[1].strip()
            if any(d["ip"] == ip for d in devices):
                print(f"  [!] Duplicate IP skipped: {name} ({ip})")
                skipped += 1
                continue
            devices.append({"name": name, "ip": ip})
            print(f"  [+] Added: {name} ({ip})")
            added += 1
    save_devices(devices)
    print()
    print(f"  [+] Import complete - {added} added, {skipped} skipped.")


# --- FUNCTION: Import from an .xlsx Excel file ---
def import_from_excel(devices):
    print()
    print("  Opening file explorer - select your Excel file...")
    filepath = browse_file(
        title     = "Select your device list (.xlsx)",
        filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not filepath:
        print("  [!] No file selected. Cancelled.")
        return
    print(f"  [+] File selected: {filepath}")
    added   = 0
    skipped = 0
    workbook = openpyxl.load_workbook(filepath, data_only=True)
    sheet    = workbook.active
    for row in sheet.iter_rows(values_only=True):
        name = row[0]
        ip   = row[1]
        if not name or not ip:
            continue
        name = str(name).strip()
        ip   = str(ip).strip()
        if any(d["ip"] == ip for d in devices):
            print(f"  [!] Duplicate IP skipped: {name} ({ip})")
            skipped += 1
            continue
        devices.append({"name": name, "ip": ip})
        print(f"  [+] Added: {name} ({ip})")
        added += 1
    save_devices(devices)
    print()
    print(f"  [+] Import complete - {added} added, {skipped} skipped.")


# --- FUNCTION: Save ping results to a .txt report ---
# Online section: count only
# Offline section: full list with device names and IPs
def save_report(online, offline):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename  = f"ping_report_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("══════════════════════════════════════════════════════════\n")
        f.write("  PING REPORT\n")
        f.write(f"  Date/Time : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  Total     : {len(online) + len(offline)} devices\n")
        f.write("══════════════════════════════════════════════════════════\n\n")

        # Online section — count only, no need to list them individually
        f.write(f"  ONLINE DEVICES\n")
        f.write(f"  {'-'*54}\n")
        f.write(f"  {len(online)} device(s) responded successfully.\n")

        f.write("\n")

        # Offline section — full list so you know exactly what needs attention
        f.write(f"  OFFLINE DEVICES ({len(offline)})\n")
        f.write(f"  {'-'*54}\n")
        if offline:
            for name, ip in offline:
                f.write(f"  [OFFLINE]  {name:<30} ({ip})\n")
        else:
            f.write("  None - all devices responded!\n")

        f.write("\n")
        f.write("══════════════════════════════════════════════════════════\n")
    print(f"  [+] Report saved: {filename}")


# --- FUNCTION: Ping all devices and collect results ---
def ping_all(devices):
    total   = len(devices)
    passed  = 0
    failed  = 0
    online  = []
    offline = []

    print()
    print("══════════════════════════════════════════════════════════")
    print(f"  Pinging {total} device(s)...")
    print("══════════════════════════════════════════════════════════")

    for d in devices:
        name = d["name"]
        ip   = d["ip"]
        if ping_device(ip):
            # Green text for online — just a simple confirmation tick
            print(f"{GREEN}  [ONLINE ]  {name:<30} ({ip}){RESET}")
            online.append((name, ip))
            passed += 1
        else:
            # Red text for offline — draws your eye to what needs attention
            print(f"{RED}  [OFFLINE]  {name:<30} ({ip}){RESET}")
            offline.append((name, ip))
            failed += 1

    print()
    print("══════════════════════════════════════════════════════════")
    print("  SUMMARY")
    print("══════════════════════════════════════════════════════════")
    print(f"  Total   : {total}")
    # Online — just the count in green
    print(f"{GREEN}  Online  : {passed} device(s) responded.{RESET}")
    # Offline — full list in red so it's immediately clear what needs fixing
    if failed == 0:
        print(f"{GREEN}  Offline : 0 - All devices responded!{RESET}")
    else:
        print(f"{RED}  Offline : {failed} device(s) did not respond:{RESET}")
        for name, ip in offline:
            print(f"{RED}    - {name:<30} ({ip}){RESET}")
    print("══════════════════════════════════════════════════════════")
    print()

    save = input("  Would you like to save these results to a file? (yes/no): ").strip().lower()
    if save == "yes":
        save_report(online, offline)


# ══════════════════════════════════════════════════════════
#  MAIN PROGRAM
# ══════════════════════════════════════════════════════════

devices = load_devices()

print()
print("══════════════════════════════════════════════════════════")
print("  PING TOOL")
print("══════════════════════════════════════════════════════════")
print("  How would you like to load your devices?")
print()
print("  1. Add a device manually")
print("  2. Import from .txt file")
print("  3. Import from Excel (.xlsx)")
print("══════════════════════════════════════════════════════════")

if devices:
    print(f"  (Using {len(devices)} previously saved device(s))")
    print()
    skip = input("  Press Enter to use saved devices, or choose 1-3 to reload: ").strip()
    if skip == "":
        ping_all(devices)
        print()
        print("  Done. Goodbye!")
        exit()
    choice = skip
else:
    choice = input("  Choose an option (1-3): ").strip()

if   choice == "1": add_device(devices)
elif choice == "2": import_from_txt(devices)
elif choice == "3": import_from_excel(devices)
else:
    print("  [!] Invalid option.")
    exit()

if not devices:
    print("  [!] No devices loaded. Exiting.")
else:
    ping_all(devices)
    print()
    print("  Done. Goodbye!")
