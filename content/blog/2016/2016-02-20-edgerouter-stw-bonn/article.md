Title: Configuring EdgeRouter for internet over PPTP (Part 2)
Slug: edgerouter-internet-pptp-part2
Date: 2016-02-20 23:47
Tags: Ubiquiti, EdgeMax, PPTP, STWB
Cover: {static|images/edgerouter_with_lan.jpg}

In the last post I showed you how to configure an Ubiquiti EdgeRouter to use kernelmode PPTP.

This post will be a continuation on the general config, showing how to set up the local network.

<!-- PELICAN_END_SUMMARY -->

Parts of this post may be specific to the configuration for Studierendenwerk Bonn, but most should work everywhere.

Also this probably isn't complete, I just wanted to provice a little insight for people figuring out how to use these devices.

### Local Network: br0

For my local network I want to use a bridge, so this is how I have configured it:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit interfaces bridge br0
[edit interfaces bridge br0]
ubnt@ubnt# set address 10.25.11.1/24
[edit interfaces bridge br0]
ubnt@ubnt# set address 2a00:5ba0:8000:9e5b::1/64
[edit interfaces bridge br0]
ubnt@ubnt# set description "Local Network"
[edit interfaces bridge br0]
ubnt@ubnt# up
[edit interfaces]
ubnt@ubnt# edit ethernet eth0
[edit interfaces ethernet eth0]
ubnt@ubnt# delete address
[edit interfaces ethernet eth0]
ubnt@ubnt# set bridge-group bridge br0
[edit interfaces ethernet eth0]
ubnt@ubnt# commit
[ interfaces ethernet eth0 bridge-group ]
Adding interface eth0 to bridge br0

[edit interfaces ethernet eth0]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

### DNS

Enable DNS forwarding on the router:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# set service dns forwarding listen-on br0
[edit]
ubnt@ubnt# commit
[edit]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

### IPv4

#### DHCP server on br0

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit service dhcp-server shared-network-name LAN
[edit service dhcp-server shared-network-name LAN]
ubnt@ubnt# set subnet 10.25.11.0/24
[edit service dhcp-server shared-network-name LAN]
ubnt@ubnt# edit subnet 10.25.11.0/24
[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# set start 10.25.11.100 stop 10.25.11.200
[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# set default-router 10.25.11.1
[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# set dns-server 10.25.11.1
[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# set domain-name ip
[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# commit
[ service dhcp-server ]
Starting DHCP server daemon...

[edit service dhcp-server shared-network-name LAN subnet 10.25.11.0/24]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

#### Firewall

This is a lot of config, so I'll just give you the export of the config, you'll have to type the commands yourself:

```
ubnt@ubnt# show firewall name
 name LAN_IN {
     default-action accept
     description "Local network to internet"
 }
 name STW_IN {
     default-action drop
     description "STW to local network"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
 }
 name STW_LOCAL {
     default-action drop
     description "STW to router"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
     rule 3 {
         action drop
         description "Drop some ports, just to be sure they never get exposed."
         destination {
             port 21,22,23,80,443,843,3389,5631
         }
         log disable
         protocol tcp
     }
     rule 4 {
         action accept
         description "Allow icmp echo-requests"
         icmp {
             type-name echo-request
         }
         log disable
         protocol icmp
     }
     rule 5 {
         action accept
         description "Allow DHCP"
         destination {
             port 67,68
         }
         log disable
         protocol udp
         source {
             address 192.168.128.1-192.168.128.3
         }
     }
 }
 name STW_WAN_IN {
     default-action drop
     description "Internet to local network"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
 }
 name STW_WAN_LOCAL {
     default-action drop
     description "Internet to router"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
     rule 3 {
         action drop
         description "Drop some ports, just to be sure they never get exposed."
         destination {
             port 21,22,23,80,443,843,3389,5631
         }
         log disable
         protocol tcp
     }
     rule 4 {
         action accept
         description "Allow icmp echo-requests"
         icmp {
             type-name echo-request
         }
         log disable
         protocol icmp
     }
 }
[edit]
```

To enable these rules:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# set interfaces bridge br0 firewall in name LAN_IN
[edit]
ubnt@ubnt# set interfaces pptp-client pptpc0 firewall in name STW_WAN_IN
[edit]
ubnt@ubnt# set interfaces pptp-client pptpc0 firewall local name STW_WAN_LOCAL
[edit]
ubnt@ubnt# set interfaces ethernet eth1 firewall in name STW_IN
[edit]
ubnt@ubnt# set interfaces ethernet eth1 firewall local name STW_LOCAL
[edit]
ubnt@ubnt# commit
[edit]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

#### NAT

To enable NAT set the following configuration:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit service nat rule 5000
[edit service nat rule 5000]
ubnt@ubnt# set log disable
[edit service nat rule 5000]
ubnt@ubnt# set outbound-interface pptpc0
[edit service nat rule 5000]
ubnt@ubnt# set type masquerade
[edit service nat rule 5000]
ubnt@ubnt# set protocol all
[edit service nat rule 5000]
ubnt@ubnt# up
[edit service nat]
ubnt@ubnt# edit rule 5001
[edit service nat rule 5001]
ubnt@ubnt# set log disable
[edit service nat rule 5001]
ubnt@ubnt# set outbound-interface eth1
[edit service nat rule 5001]
ubnt@ubnt# set type masquerade
[edit service nat rule 5001]
ubnt@ubnt# set protocol all
[edit service nat rule 5001]
ubnt@ubnt# commit
[edit service nat rule 5001]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

At this point you should be able to connect to the internet on your local network.
The internal network (between your PPTP server and your router) should also be rechable.

### IPv6

#### Router Advertisements on br0

For IPv6 we want to enable router advertisements:

```
ubnt@ubnt:~$ configure
[edit]
ubnt@ubnt# edit interfaces bridge br0
[edit interfaces bridge br0]
ubnt@ubnt# set ipv6 router-advert prefix 2a00:5ba0:8000:9e5b::/64
[edit interfaces bridge br0]
ubnt@ubnt# set ipv6 router-advert send-advert true
[edit interfaces bridge br0]
ubnt@ubnt# set ipv6 router-advert name-server 2a00:5ba0:8000:9e5b::1
[edit interfaces bridge br0]
ubnt@ubnt# commit
[ interfaces bridge br0 ipv6 router-advert ]
Re-generating radvd config file for interface br0...
Starting radvd...
Starting radvd: radvd.

[edit interfaces bridge br0]
ubnt@ubnt# save
Saving configuration to '/config/config.boot'...
Done
```

#### Firewall

Again, a lot of configuration, here just the export:

```
ubnt@ubnt# show firewall ipv6-name
 ipv6-name LAN6_IN {
     default-action accept
 }
 ipv6-name STW6_IN {
     default-action drop
     description "STW to local network (IPv6)"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
     rule 3 {
         action accept
         description "Allow ICMPv6 echo-requests"
         icmpv6 {
             type echo-request
         }
         log disable
         protocol icmpv6
     }
     rule 4 {
         action accept
         description "Allow incoming SSH connections on various ports"
         destination {
             port 22,222,2222,1337
         }
         protocol tcp
     }
 }
 ipv6-name STW6_LOCAL {
     default-action drop
     description "STW to router (IPv6)"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         state {
             invalid enable
         }
     }
     rule 3 {
         action accept
         description "Allow ICMPv6 echo-requests"
         icmpv6 {
             type echo-request
         }
         log disable
         protocol icmpv6
     }
 }
 ipv6-name STW_WAN6_IN {
     default-action drop
     description "Internet to local network (IPv6)"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         log disable
         state {
             invalid enable
         }
     }
     rule 3 {
         action accept
         description "Allow ICMPv6 echo-requests"
         icmpv6 {
             type echo-request
         }
         log disable
         protocol icmpv6
     }
     rule 4 {
         action accept
         description "Allow incoming SSH connections on various ports"
         destination {
             port 22,222,2222,1337
         }
         protocol tcp
     }
 }
 ipv6-name STW_WAN6_LOCAL {
     default-action drop
     description "Internet to router (IPv6)"
     rule 1 {
         action accept
         description "Allow established/related connections"
         log disable
         state {
             established enable
             related enable
         }
     }
     rule 2 {
         action drop
         description "Drop invalid packets"
         state {
             invalid enable
         }
     }
     rule 3 {
         action accept
         description "Allow ICMPv6 echo-requests"
         icmpv6 {
             type echo-request
         }
         log disable
         protocol icmpv6
     }
     rule 4 {
         action accept
         description "Allow router advertisements"
         icmpv6 {
             type router-advertisement
         }
         log disable
         protocol icmpv6
     }
 }
[edit]
```

To enable that config:

```
ubnt@ubnt# set interfaces bridge br0 firewall in ipv6-name LAN6_IN
[edit]
ubnt@ubnt# set interfaces ethernet eth1 firewall in ipv6-name STW6_IN
[edit]
ubnt@ubnt# set interfaces ethernet eth1 firewall local ipv6-name STW6_LOCAL
[edit]
ubnt@ubnt# set interfaces pptp-client pptpc0 firewall in ipv6-name STW_WAN6_IN
[edit]
ubnt@ubnt# set interfaces pptp-client pptpc0 firewall local ipv6-name STW_WAN6_LOCAL
```
