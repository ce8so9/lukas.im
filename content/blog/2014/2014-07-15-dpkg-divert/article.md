Title: dpkg-divert
Slug: dpkg-divert
Date: 2014-07-15 01:07
Tags: Linux, Debian, dpkg

Just a short note for myself...

To move a dpkg-managed file out of the way:

```bash
dpkg-divert --rename --divert /usr/share/initramfs-tools/dropbear.original /usr/share/initramfs-tools/scripts/init-premount/dropbear
```

Copy and edit original.

```bash
cp /usr/share/initramfs-tools/dropbear.original /usr/share/initramfs-tools/scripts/init-premount/dropbear
ed /usr/share/initramfs-tools/scripts/init-premount/dropbear
```
