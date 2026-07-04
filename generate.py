import requests
import ipaddress

URL = "https://raw.githubusercontent.com/Y3ll0w/CrowdSec-CAPI-Decisions/refs/heads/main/all.txt"

r = requests.get(URL, timeout=60)

ips = []

for line in r.text.splitlines():
    line = line.strip()

    if not line:
        continue

    try:
        ip = ipaddress.ip_address(line)

        # خدم غير IPv4
        if ip.version == 4:
            ips.append(line)

    except:
        pass

with open("crowdsec.rsc", "w") as f:
    f.write("/ip firewall address-list remove [find list=CrowdSec]\n\n")

    for ip in ips:
        f.write(
            f'/ip firewall address-list add '
            f'list=CrowdSec '
            f'address={ip} '
            f'timeout=1d '
            f'comment="CrowdSec"\n'
        )

print("IPv4 entries:", len(ips))
