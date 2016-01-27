Title: Outgoing IPv6-address
Slug: outgoing-ipv6-address
Date: 2014-04-07 17:27
Tags: Linux, IPv6, Network
Cover: {static|images/cover.png}

On my server I have multiple IPv6 addresses, but I want to define that all outgoing connections should always use one specific address.

On Linux there is an option to mark an IPv6 address as "deprecated", you can do that by setting the address parameter `preferred_lft` to `0`. After that the address is still reachable, and you can still respond over it, but Linux will newer use it for new outgoing connections.

My network config now looks like this:

```
auto 6in4
iface 6in4 inet6 v4tunnel
	address 2001:4dd0:ff00:189b::2
	netmask 64
	endpoint 78.35.24.124
	gateway 2001:4dd0:ff00:189b::1
	up ip -6 addr add 2001:4dd0:ff00:989b::1/64 dev 6in4 preferred_lft 1
	up ip -6 addr change 2001:4dd0:ff00:189b::2 dev 6in4 preferred_lft 0
	down ip -6 addr del 2001:4dd0:ff00:989b::1/64 dev 6in4
```

This creates a 6in4 device, sets the IPv6 address that SixXs assigned my tunnel, and afterwards runs the commands which marks the original address as "deprecated" and adds a new one from the subnet I get routed to the original address.

Now the server can be reached over both addresses, but any outgoing connections will come from `2001:4dd0:ff00:989b::1`.
