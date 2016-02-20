Title: Fast PPTP client on Ubiquiti EdgeRouter (+ basic config for STW Bonn)
Slug: edgerouter-fast-pptp
Date: 2016-02-13 22:00
Tags: Ubiquiti, EdgeMax, PPTP, STWB
Cover: {static|images/edgerouter.jpg}

I'm currently living in a building of Studierendenwerk Bonn and for our internet connection we have to use a PPTP client.

As a big fan of the Ubiquiti EdgeMax series of routers I wanted to use my EdgeRouter PoE for this,
but there is a problem: PPTP on EdgeMax devices is running in Userland, and it is slow, very very slow.
Of my 100Mbit/s connection i was only able to get around 12Mbit/s, this is not good.

Unfortunately Ubiquiti doesn't see improving this as a priority, so I'll have to fix it myself.
Here is a tutorial on how to configure PPTP on EdgeMax devices to run with the pptp kernel module.

<!-- PELICAN_END_SUMMARY -->

### Important note

Sadly while actually improving the performance a lot, the finished result of this howto is not really what I would call "production-ready".

Some of the problems:

* Packet loss (on my custom Debian based router and on openwrt which both use the same software this issue doesn't occure)
* Firmware-Updates will remove some of the changes, requiring you to reapply them
* Firmware-Updates may at some point have an updated pppd version, you'll have to find the correct header files again
* Installing the required packages (further down) updates some essential system packages, which may at some point result in a (soft-)bricked router...

Also unrelated to the changes:

* IPv6 on PPTP seems to be broken a little bit in EdgeMax firmware right now... it sets `forwarding=1` but leaves `accept_ra=1`, which should be `accept_ra=2`...

### DHCP on eth1

First step to get this working is to just enable DHCP (client) on eth1, to get a connection to the intranet:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit interfaces ethernet eth1
[edit interfaces ethernet eth1]
ubnt@ubnt# set address dhcp
[edit interfaces ethernet eth1]
ubnt@ubnt# set description "STW Intranet"
[edit interfaces ethernet eth1]
ubnt@ubnt# set dhcp-options default-route no-update
[edit interfaces ethernet eth1]
ubnt@ubnt# commit
[ interfaces ethernet eth1 address dhcp ]
Starting DHCP client on eth1 ...

[edit interfaces ethernet eth1]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
[edit]
ubnt@ubnt# exit
```

Also set up a route for the internal network:

```
ubnt@ubnt# set protocols static route 192.168.0.0/16 next-hop 192.168.128.1
```

Check that it is working by running `show interfaces ethernet eth1` (outside of config mode).
It should look like this:

```
eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/ether 24:a4:3c:05:6c:90 brd ff:ff:ff:ff:ff:ff
    inet 192.168.128.250/24 brd 192.168.128.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::26a4:3cff:fe05:6c90/64 scope link
       valid_lft forever preferred_lft forever
    Description: STW Intranet

    RX:  bytes    packets     errors    dropped    overrun      mcast
          1978         19          0          0          0          0
    TX:  bytes    packets     errors    dropped    carrier collisions
          1134          7          0          0          0          0
```

At this point I rebooted my router to make sure that my route overrides were exactly as they should be.

### PPTP configuration

After this just normally configure your PPTP connection:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit interfaces pptp-client pptpc0
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set server-ip vpn.stw-bonn.de
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set user-id z[...]
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set password [...]
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set default-route auto
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set description "STW VPN"
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set ipv6 enable
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set ipv6 address autoconf
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set mtu 1486
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# commit
[ interfaces pptp-client pptpc0 ipv6 address autoconf ]
Address auto-configuration will be enabled when interface comes up.

[ interfaces pptp-client pptpc0 ipv6 dup-addr-detect-transmits 1 ]
Will set dup_addr_detect_transmits when pptpc0 comes up

[edit interfaces pptp-client pptpc0]
```

Again verify that everything is working to this point by running `show interfaces pptp-client pptpc0` (again outside of config mode).
It should look like this:

```
ubnt@ubnt:~$ show interfaces pptp-client pptpc0
pptpc0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1486 qdisc pfifo_fast state UNKNOWN qlen 100
    link/ppp
    inet 212.201.70.162 peer 192.168.1.31/32 scope global pptpc0
       valid_lft forever preferred_lft forever

    RX:  bytes    packets     errors    dropped    overrun      mcast
          3312         46          0          0          0          0
    TX:  bytes    packets     errors    dropped    carrier collisions
           186         10          0          0          0          0
```

At this point you should be able to ping the outside world from the router.

### PPTP in Kernel

Now this is where it gets a bit ugly. We have to change quite a lot of stuff...

#### Kernel module

First we need to get root access: `sudo -s`.

Try loading the pptp kernel module with `modprobe pptp`, and add loading it to rc.local by running `echo -e '#!/bin/sh -e\nmodprobe pptp\nexit 0' > /etc/rc.local`.

#### Add Debian repository

We need to compile a different client, so we need to install some tools.
For this we first add a debian repository.

Go back to config mode and set up the repository:

```
ubnt@ubnt# set system package repository debian url http://ftp.stw-bonn.de/debian/
[edit]
ubnt@ubnt# set system package repository debian distribution jessie
[edit]
ubnt@ubnt# set system package repository debian components "main"
[edit]
ubnt@ubnt# commit
[ system package repository debian ]
Adding new entry to /etc/apt/sources.list...

[edit]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
[edit]
ubnt@ubnt# exit
```

After this go back to a root shell and run `apt-get update`.

#### Install packages

Install required packages: `apt-get install gcc g++ make cmake`

If you get some questions while installing answer `Restart services during package upgrades without asking?` with `no` and on the question what to restart just press enter.

#### Get ppp headers

We can't install ppp-dev the normal way since (at least the Ubiquiti-modified) vyatta comes with its own (kinda outdated...) pppd,
and apt would basically try uninstalling vyatta because of this... that's not good.

As a workaround we download and extract an archived package manually:

```
vbash-4.1# cd /config/user-data
vbash-4.1# mkdir ppp-dev
vbash-4.1# cd ppp-dev
vbash-4.1# curl -LO http://archive.debian.org/debian-archive/backports.org/pool/main/p/ppp/ppp-dev_2.4.4rel-1bpo1_all.deb
vbash-4.1# ar x ppp-dev_2.4.4rel-1bpo1_all.deb
vbash-4.1# rm control.tar.gz debian-binary ppp-dev_2.4.4rel-1bpo1_all.deb
vbash-4.1# gzip -d data.tar.gz
vbash-4.1# tar xf data.tar
vbash-4.1# cp -Ra usr /
```

#### Build accel-pptp

Now with everything in place we can build accel-pptp:

```
vbash-4.1# cd /config/user-data
vbash-4.1# curl -Lso accel-pptp.tar.gz https://github.com/winterheart/accel-pptp/archive/master.tar.gz
vbash-4.1# tar xf accel-pptp.tar.gz
vbash-4.1# rm accel-pptp.tar.gz
vbash-4.1# cd accel-pptp-master/
vbash-4.1# mkdir build
vbash-4.1# cd build
vbash-4.1# cmake -DPPP_PREFIX_DIR=/usr ../
vbash-4.1# make
vbash-4.1# make install
vbash-4.1# mv /usr/lib/pppd/2.4.4/pptp.so /usr/lib/pppd/pptp.so
```

#### Modify vyatta to use accel-pptp instead of pptp-linux

Run this and hope for the best:

```
vbash-4.1# cat > /opt/vyatta/share/vyatta-cfg/templates/interfaces/pptp-client/node.tag/server-ip/node.def << EOF
type: txt
help: Remote IP address or hostname for this tunnel [REQUIRED]

syntax:expression: pattern \$VAR(@) "^[[:alnum:]][-.[:alnum:]]*[[:alnum:]]\$"
                   ; "Invalid server \$VAR(@)"

update: sudo sed -i -e '/^pty/d' -e '/^plugin pptp.so/d' -e '/^pptp_server/d' /etc/ppp/peers/\$VAR(../@)
        sudo sh -c "echo plugin pptp.so >> /etc/ppp/peers/\$VAR(../@)"
        sudo sh -c "echo pptp_server \$VAR(@) >> /etc/ppp/peers/\$VAR(../@)"

delete: sudo sed -i -e '/^pty/d' -e '/^plugin pptp.so/d' -e '/^pptp_server/d' /etc/ppp/peers/$VAR(../@)
EOF
```

It replaces the definitions on how to generate the server-ip part of the pptp client config.

#### Regenerate ppp client config

To regenerate the ppp client config the easiest way is go into config mode, change a few settings, commit, change them back.

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit interfaces pptp-client pptpc0
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set server-ip 127.0.0.1
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# commit
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# set server-ip vpn.stw-bonn.de
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# commit
[edit interfaces pptp-client pptpc0]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
[edit]
ubnt@ubnt# exit
```

You can verify that it worked by looking at the client config.
This is how it should look:

```
ubnt@ubnt:~$ tail -n2 /etc/ppp/peers/pptpc0
plugin pptp.so
pptp_server vpn.stw-bonn.de
```

#### Troubleshooting

If you ever run into a problem and need internet access to get something working you have to remove the `plugin pptp.so` and `pptp_server vpn.stw-bonn.de` lines and add `pty "/usr/sbin/pptp vpn.stw-bonn.de --nolaunchpppd"` to `/etc/ppp/peers/pptpc0`.

### IPv6 workaround

We need a workaround to enable IPv6 on the pptp client interface:

```
ubnt@ubnt:~$ sudo -s
vbash-4.1# mkdir -p /config/scripts/ppp/ip-up.d
vbash-4.1# cat > /config/scripts/ppp/ip-up.d/autoconf.sh << EOF
#!/bin/bash
sysctl -w net.ipv6.conf.pptpc0.autoconf=2
sysctl -w net.ipv6.conf.pptpc0.accept_ra=2
ip -6 addr flush dev pptpc0
ip -6 addr add \$(ip -6 addr show eth1 | grep fe80:: | awk '{print \$2}' | awk -F ':' '{print \$1"::"1337":"\$4":"\$5":"\$6}') dev pptpc0
EOF
vbash-4.1# chmod a+x /config/scripts/ppp/ip-up.d/autoconf.sh
```

This sets the appropriate system configuration to allow autoconf on forwarding devices and adds a link local address (derived from eth1 address) to the pptp client interface.

### Nearly Done

You now should have pptp working in your kernel, making it a lot faster.

But: You are not yet finished configuring your router! You'll need to configure your local network and you'll need to define firewall rules!
