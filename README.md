# Purpose

The Python script in this repository will read all static DHCP mappings of an [Ubiquiti](https://www.ubnt.com/) EdgeRouter X and store them in a [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) compatible hosts file.

This means you can add new DHCP static mappings to the EdgeRouter X, run this script to update the hosts file and therefor the DNS server / records. Of course you can also schedule this script by cron, so you no longer have run anything manually. Just add a new static mapping on the EdgeRouter X and the DNS will automatically be updated within a minute.

If configured properly, you can now add static DHCP mappings and your DNS service will resolv them properly.

# Installation

## Copy the script

Make sure you've a copy of the [update script](update-static-hosts.py) script and placed it on the filesystem of the EdgeRouter X.  
We recommend you copy the script manually to `/usr/local/bin/update-static-hosts.py` or run:

```
sudo curl -o /usr/local/bin/update-static-hosts.py https://raw.githubusercontent.com/confirm/edgerouter-dnsmasq-updater/master/update-static-hosts.py
```

__IMPORTANT__: Please note you need to install the script everytime when you update or restore the EdgeRouter X.

## Running the script

To create or update the hosts file, you can simply run the following command:

```bash
sudo /usr/local/bin/update-static-hosts.py /etc/hosts.static-mappings 
```

In case the static mappings changed, the script will update the defined hosts file (i.e. `/etc/hosts.static-mappings`) and reload `dnsmasq` via `SIGHUP`.  

__IMPORTANT__: The script will __REPLACE__ the defined file, so you shouldn't define `/etc/hosts` as your static hosts file.

# Configuration

## Persistence

Please note, everything you touch on the filesystem directly, will be lost after an OS update or a config restore.  
To make things persistent, you've to update the EdgeRouter X config by following these steps:

- SSH into the EdgeRouter X
- Enter the config mode by executing `configure`
- Add the commands described below
- Commit and save them by executing `commit`, followed by `save`

This ensures that your dnsmasq & cron config stays in place, even after an OS update or config restore.  

__HINT__: You can also update this configuration in the EdgeRouter X WebUI under the `Config Tree` tab.

## Task scheduler configuration

To keep the hosts file up-to-date, you want to add a cronjob which runs the script every minute:

```
set system task-scheduler task update-static-hosts crontab-spec "* * * * *"
set system task-scheduler task update-static-hosts executable path /usr/local/bin/update-static-hosts.py
set system task-scheduler task update-static-hosts executable arguments /etc/hosts.static-mappings
```

## DNS configuration

Before the EdgeRouter X resolves your new mapped hosts, you need to configure dnsmasq to use your newly created file.  
We recommend the following configuration:

```
# Don't use the default /etc/hosts file.
set service dns forwarding options no-hosts

# Use /etc/hosts.static-mappings for lookups.
set service dns forwarding options addn-hosts=/etc/hosts.static-mappings

# Never forward plain names (without a dot or domain part).
set service dns forwarding options domain-needed

# Never forward addresses in the non-routed address spaces.
set service dns forwarding options bogus-priv

# Add the domain to hostname lookups without a domain.
set service dns forwarding options expand-hosts
set service dns forwarding options domain=<your domain>

# Don't forward the local domain.
set service dns forwarding options local=/<your domain>/
```

If you want an additional file for host lookups (e.g. aliases), simply add a new hosts file with an additional `addn-hosts` option.