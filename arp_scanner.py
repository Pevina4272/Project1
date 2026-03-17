import subprocess
import re
import sys


def execute_arp_scan(network):
    """
    Executes arp-scan command on Linux
    """
    try:
        result = subprocess.run(
            ["arp-scan", "--localnet"] if network == "local" else ["arp-scan", network],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout while scanning {network}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to scan {network}: {e}")
        return None


def parse_output(output):
    """
    Parses arp-scan output to extract IP and MAC addresses
    """
    devices = []

    if output is None:
        return devices

    lines = output.split("\n")

    for line in lines:
        # Match lines like: 192.168.1.1    aa:bb:cc:dd:ee:ff    Vendor
        match = re.match(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.*)", line, re.IGNORECASE)

        if match:
            ip = match.group(1)
            mac = match.group(2)
            vendor = match.group(3)

            devices.append({
                "ip": ip,
                "mac": mac,
                "vendor": vendor
            })

    return devices


def scan_network(network):
    """
    Scans the network using ARP
    """
    output = execute_arp_scan(network)
    devices = parse_output(output)

    return devices


def display_results(devices):
    """
    Displays ARP scan results
    """
    print("\n--- ARP Scan Results ---")

    if not devices:
        print("No devices found.")
        return

    for device in devices:
        print(f"{device['ip']} -> MAC: {device['mac']} | Vendor: {device['vendor']}")


def main():
    """
    Main execution block
    """
    try:
        user_input = input("Enter network (e.g., 192.168.1.0/24 or 'local'): ").strip()

        if not user_input:
            print("No input provided.")
            sys.exit(1)

        print(f"Scanning {user_input} ...")
        devices = scan_network(user_input)

        display_results(devices)

    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()