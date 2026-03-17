import subprocess
import re
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


# -------------------- SCANNERS --------------------

def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "2", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return "0% packet loss" in result.stdout
    except:
        return False


def arp_scan(network):
    devices = []
    try:
        result = subprocess.run(
            ["arp-scan", network],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20
        )

        for line in result.stdout.split("\n"):
            match = re.match(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.*)", line, re.I)
            if match:
                devices.append({
                    "ip": match.group(1),
                    "mac": match.group(2),
                    "vendor": match.group(3)
                })

    except Exception as e:
        return [], str(e)

    return devices, None


def nmap_scan(target):
    hosts = []
    try:
        result = subprocess.run(
            ["nmap", "-sS", "-T4", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        current_host = None

        for line in result.stdout.split("\n"):

            host_match = re.search(r"Nmap scan report for (.+)", line)
            if host_match:
                if current_host:
                    hosts.append(current_host)

                current_host = {
                    "host": host_match.group(1),
                    "ports": []
                }

            port_match = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)", line)
            if port_match and current_host:
                current_host["ports"].append({
                    "port": port_match.group(1),
                    "protocol": port_match.group(2),
                    "service": port_match.group(3)
                })

        if current_host:
            hosts.append(current_host)

    except Exception as e:
        return [], str(e)

    return hosts, None


# -------------------- GUI APP --------------------

class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Network Scanner Tool")
        self.root.geometry("700x500")

        # Input
        tk.Label(root, text="Enter Network (e.g., 192.168.1.0/24):").pack(pady=5)
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        # Buttons
        self.scan_btn = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_btn.pack(pady=5)

        self.save_btn = tk.Button(root, text="Save Results", command=self.save_results)
        self.save_btn.pack(pady=5)

        # Output box
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.output.pack(pady=10)

        self.results = {}

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def start_scan(self):
        network = self.entry.get().strip()

        if not network:
            messagebox.showerror("Error", "Please enter a network")
            return

        self.output.delete(1.0, tk.END)
        thread = threading.Thread(target=self.run_scan, args=(network,))
        thread.start()

    def run_scan(self, network):
        self.log("[1] Running ARP Scan...")
        arp_devices, err = arp_scan(network)

        if err:
            self.log(f"[ERROR] {err}")
            return

        self.log(f"Found {len(arp_devices)} devices\n")

        self.log("[2] Running Ping Check...")
        ping_results = {}
        for d in arp_devices:
            ip = d["ip"]
            status = ping_host(ip)
            ping_results[ip] = status
            self.log(f"{ip} -> {'UP' if status else 'DOWN'}")

        self.log("\n[3] Running Nmap Scan...")
        nmap_results, err = nmap_scan(network)

        if err:
            self.log(f"[ERROR] {err}")
            return

        for host in nmap_results:
            self.log(f"\nHost: {host['host']}")
            if not host["ports"]:
                self.log("  No open ports")
            for p in host["ports"]:
                self.log(f"  {p['port']}/{p['protocol']} -> {p['service']}")

        self.results = {
            "arp": arp_devices,
            "ping": ping_results,
            "nmap": nmap_results
        }

        self.log("\n✅ Scan Completed!")

    def save_results(self):
        if not self.results:
            messagebox.showwarning("Warning", "No results to save")
            return

        with open("scan_results.json", "w") as f:
            json.dump(self.results, f, indent=4)

        messagebox.showinfo("Saved", "Results saved to scan_results.json")


# -------------------- MAIN --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()