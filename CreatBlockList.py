import requests
import re
import os

MAX_SIZE = 45 * 1024 * 1024  # 45 MB limit per file

def extract_domains(text):
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = re.search(r'(?:(?:0\.0\.0\.0|127\.0\.0\.1)\s+)?((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]+)', line)
        if match:
            domains.add(match.group(1).lower())
    return domains


def write_split_files(domains):
    sorted_domains = sorted(domains)
    file_index = 1
    current_size = 0
    output_file = f"blockList_{file_index:02d}.txt"
    f = open(output_file, "w")

    print("\nWriting output files...")

    for domain in sorted_domains:
        line = f"0.0.0.0 {domain}\n"
        encoded = line.encode("utf-8")
        line_size = len(encoded)

        # If file would exceed 45MB → create new file
        if current_size + line_size > MAX_SIZE:
            f.close()
            file_index += 1
            output_file = f"blockList_{file_index:02d}.txt"
            f = open(output_file, "w")
            current_size = 0
            print(f"→ Creating {output_file}")

        f.write(line)
        current_size += line_size

    f.close()
    print(f"Done! {file_index} files created.")


def main():
    url_file = input("Enter file containing URLs: ").strip()

    try:
        with open(url_file, "r") as f:
            urls = [u.strip() for u in f if u.strip() and not u.startswith("#")]
    except:
        print("Could not read file!")
        return

    all_domains = set()

    for url in urls:
        print(f"\nChecking: {url}")
        try:
            r = requests.get(url, timeout=8)
        except:
            print("  → ERROR: Cannot connect")
            continue

        if r.status_code != 200:
            print(f"  → ERROR: HTTP {r.status_code}")
            continue

        print("  → OK, extracting domains")
        domains = extract_domains(r.text)
        print(f"  → Found {len(domains)} domains")
        all_domains.update(domains)

    print(f"\nTotal unique domains: {len(all_domains)}")

    write_split_files(all_domains)


if __name__ == "__main__":
    main()

