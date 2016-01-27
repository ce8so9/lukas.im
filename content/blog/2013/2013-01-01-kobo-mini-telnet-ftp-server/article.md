Title: Kobo Mini Telnet/FTP Server
Slug: kobo-mini-telnet-ftp-server
Date: 2013-01-01 22:02
Tags: Linux, Kobo Mini, Telnet, Hack

I recently bought a Kobo Mini ebook reader because I wanted to play around with the e-ink display.
To do that I obviously needed a shell on the device, and here I'll describe how I got that.

There are basically two ways to get the (already built-in) telnet- and ftp-server to start.
One way is to open up the Kobo Mini, take out it's internal MicroSD card, mount that on a Linux computer, and modify some scripts.
The other way it to build a fake update package.

I choose the way of opening the device and accessing the root filesystem directly.

To actually use the telnet-server we need pseudo-shells, and for that we need to create an init-script that mounts `/dev/pts` on the device.
So I created `/etc/init.d/rcS2` (like other people on the internet did) and filled it with the following little code snippet:
```bash
#!/bin/sh
# /etc/init.d/rcS2
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts
```

The file should be executable, so `chmod a+x etc/init.d/rcS2` and we are good to go.

Next we need to actually get the telnet server to start, for that we modify `/etc/inetd.conf` and add the following lines:

```
21 stream tcp nowait root /bin/busybox ftpd -w -S /
23 stream tcp nowait root /bin/busybox telnetd -i
```

To get our init-script and inetd to run we also need to append some lines to `/etc/inittab`:

```
::sysinit:/etc/init.d/rcS2
::respawn:/usr/sbin/inetd -f /etc/inetd.conf
```

If you want to go the route with the fake update package you'll have to put all these new and modified files into a gzip compressed tar-file and put it as `.kobo/KoboRoot.tgz` on the device.
Keep in mind that you will need the original content of `/etc/inittab`, so you may need to extract that from an official firmware update or get it from somewhere else on the internet.

After putting the MicroSD back into my Kobo Mini i started it up and ran the Webbrowser to start the wifi connection.
After all that telnet was finally reachable, and I could login with user `root` without a password (probably a bad idea to do this on a public wifi network...).

On the shell you can run `killall nickel` to get rid of the original eBook-software (until next reboot), which also disables the automatic disconnect of the wifi connection (which will obviously drain your battery).

