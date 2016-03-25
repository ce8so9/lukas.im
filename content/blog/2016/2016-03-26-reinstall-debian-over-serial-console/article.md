Title: Reinstall Debian over serial console
Slug: reinstall-debian-over-serial-console
Date: 2016-03-26 00:26
Tags: Debian, Online.net, kexec
Cover: {static|images/success.png}

I ordered an SC2016 at online.net yesterday, and wanted to reinstall it with encrypted rootfs.

All my other servers had KVM consoles and possibilities to mount CD images, but this one only had a serial console and a rescue system,
so I had to be a little bit creative.

<!-- PELICAN_END_SUMMARY -->

In the end the solution was to download the netboot image, load it with kexec and boot into that minimal system,
after that I was able to continue the installation normally via the serial console.

```
apt-get install kexec-tools
wget http://ftp.stw-bonn.de/debian/dists/jessie/main/installer-amd64/current/images/netboot/netboot.tar.gz
tar xvf netboot.tar.gz
kexec --load --initrd=debian-installer/amd64/initrd.gz debian-installer/amd64/linux --append="console=ttyS1,9600"
kexec -e
```

![Debian installer language selection]({static|images/installer.png|thumb=1024x_})

## End of installation

At the end of the installation there is one more thing to do.
First open a shell (by going back when it says it finished, and selecting the option to open a shell) and mount virtual paths into target:
```
mount --bind /dev /target/dev
mount --bind /sys /target/sys
mount --bind /proc /target/proc
```

Now edit `/target/etc/default/grub`, replace `GRUB_CMDLINE_LINUX=""` with `GRUB_CMDLINE_LINUX="console=ttyS1,9600"`.

After editing the file chroot into target filesystem and update grub config:
```
chroot /target /bin/bash
update-grub # in chroot
```

If you want to you could also instruct grub to use the serial console,
but in my case it did that automatically and if it ever stops working
i'll just fix it using the rescue mode.
