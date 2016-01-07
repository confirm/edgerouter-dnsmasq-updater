#!/usr/bin/env python
import argparse
import subprocess
import re
import hashlib

# Setup argparser.
parser = argparse.ArgumentParser(description='Update a hosts file with static mappings')
parser.add_argument('filename', help='Path to the hosts file')
args = parser.parse_args()

# Get config from router.
config = subprocess.check_output(['cat', '/config/config.boot'])

# Find all static mappings.
matchings = re.findall('static-mapping ([^ ]+) \{\s+ip-address ([0-9.]+)[^\}]+\}', config, re.S)

# Get hash of new config.
hasher  = hashlib.md5('\n'.join([h + i for h, i in matchings]))
md5_new = hasher.hexdigest()

# Get hash of current config.
try:
    with file(args.filename, 'r') as f:
        md5_old = f.readline()[2:].strip()
except IOError:
    md5_old = None

# Check if checksum has changed.
if md5_old != md5_new:

    # Write new file.
    print('Writing {filename}...'.format(filename=args.filename))
    with file(args.filename, 'w') as f:
        f.write('# {md5}\n'.format(md5=md5_new))
        for hostname, ip in matchings:
            f.write('{ip:<15s} {hostname}\n'.format(ip=ip, hostname=hostname.lower()))

    # Reload dnsmasq.
    print('Reloading dnsmasq...')
    subprocess.check_call(['pkill', '-HUP', 'dnsmasq'])