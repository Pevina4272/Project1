import subprocess
import re
import sys


def execute_ping(host):
    """
    Executes ping command on Linux
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "4", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout while pinging {host}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to ping {host}: {e}")
        return None


def parse_output(output):
    """
    Parses ping output to determine reachability and average response time
    """
    if output is None:
        return False, None

    # Check if host is reachable
    reachable = "0% packet loss" in output

    # Extract average time from: min/avg/max/mdev
    match = re.search(r"= [\d\.]+/([\d\.]+)/[\d\.]+/[\d\.]+", output)

    avg_time = float(match.group(1)) if match else None

    return reachable, avg_time


def scan_host(host):
    """
    Scans a single host
    """
    output = execute_ping(host)
    reachable, avg_time = parse_output(output)

    return {
        "host": host,
        "reachable": reachable,
        "avg_time": avg_time
    }


def display_results(results):
    """
    Displays scan results
    """
    print("\n--- Scan Results ---")
    for result in results:
        status = "Reachable" if result["reachable"] else "Unreachable"

        if result["avg_time"] is not None:
            print(f"{result['host']} -> {status}, Avg Time: {result['avg_time']} ms")
        else:
            print(f"{result['host']} -> {status}, Avg Time: N/A")


def main():
    """
    Main execution block
    """
    try:
        user_input = input("Enter hostname(s) or IP(s) (comma-separated): ").strip()

        if not user_input:
            print("No input provided.")
            sys.exit(1)

        hosts = [h.strip() for h in user_input.split(",") if h.strip()]

        results = []

        for host in hosts:
            print(f"Pinging {host}...")
            results.append(scan_host(host))

        display_results(results)

    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()