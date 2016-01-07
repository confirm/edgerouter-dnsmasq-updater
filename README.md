# Purpose

The Python script in this repository will read all static DHCP mappings of an [Ubiquiti](https://www.ubnt.com/) EdgeRouter X and store them in a [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) compatible hosts file.

This means you can add new static mappings to the EdgeRouter X and run this script to update the hosts file and therefor the DNS server. Of course you can also schedule this script by cron, so you no longer have run anything manually. Just add a new static mapping on the EdgeRouter X and the DNS will automatically be updated within one minute.

# Configuration

We recommend you create a new `dnsmasq` config file located at `/etc/dnsmasq.d/*.conf`, because `/etc/dnsmasq.conf` will automatically be overwritten by vyatta.
Here's an example of an additional config file:

```
# Additional hosts file.
addn-hosts=/etc/hosts.static

# Never forward plain names (without a dot or domain part).
domain-needed

# Never forward addresses in the non-routed address spaces.
bogus-priv

# Add the domain to simple hostnames.
expand-hosts
domain=<your domain>

# Local domains which will should not be forwarded.
local=/<your domain>/
```

Please note you need at least the `addn-hosts` parameter.

# Usage

## Copy the script

Make sure you've a copy of the [update script](update-static-hosts.py) script.
We recommend you copy the script to `/usr/local/bin/update-static-hosts.py`.

## Running the script

To update the hosts file you now can simply run:

```bash
/usr/local/bin/edgerouter_dnsmasq_updater.py <your static hosts file>
```

This will update the hosts file and reload `dnsmasq` via `SIGHUP`.
Please note that the rewrite of the file and reload of `dnsmasq` only occurs when the `static-mapping` config has changed between the last and current invoke.

__IMPORTANT__: The script will __REPLACE__ the defined file, so you shouldn't define `/etc/hosts` as your static hosts file.

## Cronjob

If you want your script to run every minute just create `/etc/cron.d/update-static-hosts` with the following content:

```
* * * * *   root    /usr/local/bin/update-static-hosts.py <your static hosts file>
```
