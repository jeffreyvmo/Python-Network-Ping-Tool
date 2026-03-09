# 🖧 Python Network Ping Tool

A command-line network monitoring tool built in Python that pings devices, displays live color-coded results, and exports timestamped reports. Built for Windows and designed for IT and network teams.

---

## 📋 Features

- **Import devices** from an Excel (.xlsx) file or a tab-separated .txt file using a file explorer popup
- **Add devices manually** by typing in a name and IP address
- **Ping all devices** automatically after loading — no extra steps
- **Color-coded results** — green for online, red for offline
- **Smart summary** — shows total online count and full details for offline devices only
- **Save reports** — exports a timestamped .txt report after every ping run
- **Persistent storage** — remembers your device list between sessions using a local JSON file

---

## 📸 Preview

```
══════════════════════════════════════════════════════════
  Pinging 27 device(s)...
══════════════════════════════════════════════════════════
  [ONLINE ]  BR-01-UPS-01                   (192.168.1.10)   ← green
  [ONLINE ]  BR-02-UPS-01                   (192.168.1.11)   ← green
  [OFFLINE]  BR-03-UPS-01                   (192.168.1.12)   ← red
  ...

══════════════════════════════════════════════════════════
  SUMMARY
══════════════════════════════════════════════════════════
  Total   : 27
  Online  : 26 device(s) responded.
  Offline : 1 device(s) did not respond:
    - BR-03-UPS-01                   (192.168.1.12)
══════════════════════════════════════════════════════════

  Would you like to save these results to a file? (yes/no):
```

---

## 🚀 Getting Started

### Requirements

- Python 3.x
- Windows (uses Windows ping flags)

### Install Dependencies

Only one external library is needed:

```bash
pip install openpyxl
```

> All other modules (`subprocess`, `json`, `os`, `datetime`, `tkinter`) come built into Python.

### Run the Tool

```bash
python ping_tool.py
```

---

## 📂 How to Use

### Loading Devices

When you run the script you will be prompted to choose how to load your devices:

```
  1. Add a device manually
  2. Import from .txt file
  3. Import from Excel (.xlsx)
```

**Option 1 — Manual entry:**
Type in a device name and IP address directly.

**Option 2 — Import from .txt:**
Opens a file explorer popup. Select a tab-separated .txt file formatted like this:

```
BR-01-UPS-01    192.168.1.10
BR-02-UPS-01    192.168.1.11
BR-03-UPS-01    192.168.1.12
```

**Option 3 — Import from Excel:**
Opens a file explorer popup. Select an .xlsx file with:
- Column A = Device Name
- Column B = IP Address

No header row required — data can start on row 1.

### Saved Devices

After importing, devices are saved to a local `devices.json` file. The next time you run the script it will detect this file and offer to use the saved list — just press **Enter** to skip reloading and go straight to pinging.

### Saving a Report

After the ping run completes you will be asked:

```
  Would you like to save these results to a file? (yes/no):
```

If you choose yes, a report is saved in the same folder as the script with a timestamped filename:

```
ping_report_2026-03-09_14-35-22.txt
```

The report includes:
- Total online device count
- Full list of offline devices with names and IPs

---

## 📁 File Structure

```
ping-tool/
│
├── ping_tool.py        # Main script
├── devices.json        # Auto-generated — stores your saved device list
├── ping_report_*.txt   # Auto-generated — timestamped report after each run
└── README.md
```

---

## 🧠 What I Learned Building This

This was built as a hands-on Python learning project. Concepts covered:

- `subprocess` — running system commands from Python
- `json` — reading and writing data to disk
- `openpyxl` — parsing Excel files
- `tkinter` / `filedialog` — opening native Windows file explorer popups
- `datetime` — generating timestamps for report filenames
- Functions, loops, dictionaries, lists, and tuples
- Input validation and error handling
- ANSI color codes for terminal output
- File I/O with proper UTF-8 encoding

---

## 🛠 Future Improvements

- [ ] Add support for pinging specific device groups only
- [ ] Schedule automatic ping runs at set intervals
- [ ] Export reports to Excel instead of .txt
- [ ] Add a GUI interface

---

## 👤 Author

Built by [Your Name]  
Feel free to fork, use, or improve this tool.
