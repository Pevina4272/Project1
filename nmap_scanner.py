import subprocess
import re
import sys


def execute_nmap_scan(target):
    """
    Executes nmap scan on Linux
    """
    try:
        result = subprocess.run(
            ["nmap", "-sS", "-T4", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout while scanning {target}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to scan {target}: {e}")
        return None


def parse_output(output):
    """
    Parses nmap output to extract host and open ports
    """
    results = []
    current_host = None

    if output is None:
        return results

    lines = output.split("\n")

    for line in lines:
        # Detect host
        host_match = re.search(r"Nmap scan report for (.+)", line)
        if host_match:
            if current_host:
                results.append(current_host)

            current_host = {
                "host": host_match.group(1),
                "ports": []
            }

        # Detect open ports
        port_match = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)", line)
        if port_match and current_host:
            port = port_match.group(1)
            protocol = port_match.group(2)
            service = port_match.group(3)

            current_host["ports"].append({
                "port": port,
                "protocol": protocol,
                "service": service
            })

    if current_host:
        results.append(current_host)

    return results


def scan_target(target):
    """
    Scans a target using nmap
    """
    output = execute_nmap_scan(target)
    results = parse_output(output)

    return results


def display_results(results):
    """
    Displays scan results
    """
    print("\n--- Nmap Scan Results ---")

    if not results:
        print("No hosts found.")
        return

    for host in results:
        print(f"\nHost: {host['host']}")

        if not host["ports"]:
            print("  No open ports found.")
            continue

        for port in host["ports"]:
            print(f"  {port['port']}/{port['protocol']} -> {port['service']}")


def main():
    """
    Main execution block
    """
    try:
        user_input = input("Enter target (IP, hostname, or subnet e.g., 192.168.1.0/24): ").strip()

        if not user_input:
            print("No input provided.")
            sys.exit(1)

        print(f"Scanning {user_input} ...")
        results = scan_target(user_input)

        display_results(results)

    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()