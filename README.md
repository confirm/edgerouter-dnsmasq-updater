# Purpose

The Python script in this repository will read all static DHCP mappings of an [Ubiquiti](https://www.ubnt.com/) EdgeRouter X and store them in a [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) compatible hosts file.

This means you can add new DHCP static mappings to the EdgeRouter X, run this script to update the hosts file and therefor the DNS server / records. Of course you can also schedule this script by cron, so you no longer have run anything manually. Just add a new static mapping on the EdgeRouter X and the DNS will automatically be updated within a minute.

If configured properly, you can now add static DHCP mappings and your DNS service will resolv them properly.

# Configuration

We recommend the following DNS service configuration:

```
# Don't use the default /etc/hosts file.
service dns forwarding options no-hosts

# Use /etc/hosts.static-mappings for lookups.
service dns forwarding options addn-hosts=/etc/hosts.static-mappings

# Never forward plain names (without a dot or domain part).
service dns forwarding options domain-needed

# Never forward addresses in the non-routed address spaces.
service dns forwarding options bogus-priv

# Add the domain to hostname lookups without a domain.
service dns forwarding options expand-hosts
service dns forwarding options domain=<your domain>

# Don't forward the local domain.
service dns forwarding options local=/<your domain>/
```

If you want an additional file for host lookups (e.g. aliases), simply add a new hosts file with an additional `addn-hosts` option.

# Usage

## Copy the script

Make sure you've a copy of the [update script](update-static-hosts.py) script.
We recommend you copy the script to `/usr/local/bin/update-static-hosts.py`.

## Running the script

To update the hosts file you now can simply run:

```bash
/usr/local/bin/edgerouter_dnsmasq_updater.py /etc/hosts.static-mappings 
```

This will update the hosts file and reload `dnsmasq` via `SIGHUP`.
Please note that the rewrite of the file and reload of `dnsmasq` only occurs when the `static-mapping` config has changed between the last and current invoke.

__IMPORTANT__: The script will __REPLACE__ the defined file, so you shouldn't define `/etc/hosts` as your static hosts file.

## Cronjob

If you want your script to run every minute just create `/etc/cron.d/update-static-hosts` with the following content:

```
* * * * *   root    /usr/local/bin/update-static-hosts.py /etc/hosts.static-mappings
```
