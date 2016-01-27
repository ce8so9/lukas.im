Title: Resize CoreOS rootfs
Slug: resize-coreos-rootfs
Date: 2014-04-07 19:27
Tags: Linux, CoreOS, btrfs, GPT
Cover: {static|images/cover.png}

I was playing around with [CoreOS](https://coreos.com) in the last few days and i had a problem that the "installer" only created a 3GB GPT-label, with the problem that the backup header wasn't at the end of my disk but at the end of this 3GB section, so I couldn't just resize my rootfs to the full disk.

To resize the `ROOT`-filesystem we'll have to move this backup data to the end of the disk:

```
localhost core # gdisk /dev/sda
GPT fdisk (gdisk) version 0.8.6

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): x

Expert command (? for help): e
Relocating backup data structures to the end of the disk

Expert command (? for help): m

Command (? for help): w

Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): Y
OK; writing new GUID partition table (GPT) to /dev/sda.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot.
The operation has completed successfully.
localhost core # reboot
```

After a reboot we open gdisk again, delete the `ROOT`-partition and recreate it with the same starting sector and the default end sector (which normally is the highest possible value).
Partition type should be FFFF.

```
localhost core # gdisk /dev/sda
GPT fdisk (gdisk) version 0.8.6

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.

Command (? for help): p
Disk /dev/sda: 234441648 sectors, 111.8 GiB
Logical sector size: 512 bytes
Disk identifier (GUID): 83A877DF-4A87-1E4A-B413-BEABFD879D68
Partition table holds up to 128 entries
First usable sector is 34, last usable sector is 234441614
Partitions will be aligned on 2048-sector boundaries
Total free space is 228543341 sectors (109.0 GiB)

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048          264191   128.0 MiB   EF00  EFI-SYSTEM
   2         2361344         2492415   64.0 MiB    FFFF  BOOT-B
   3          264192         2361343   1024.0 MiB  FFFF  USR-A
   4         2492416         4589567   1024.0 MiB  FFFF  USR-B
   6         4589568         4851711   128.0 MiB   8300  OEM
   9         4851712         5900287   512.0 MiB   FFFF  ROOT

Command (? for help): d
Partition number (1-9): 9

Command (? for help): n
Partition number (5-128, default 5): 9
First sector (34-234441614, default = 4851712) or {+-}size{KMGTP}: 4851712
Last sector (4851712-234441614, default = 234441614) or {+-}size{KMGTP}:
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): FFFF
Exact type match not found for type code FFFF; assigning type code for
'Linux filesystem'
Changed type of partition to 'Linux filesystem'

Command (? for help): w

Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): Y
OK; writing new GUID partition table (GPT) to /dev/sda.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot.
The operation has completed successfully.
localhost core # reboot
```

After another reboot we now can resize the btrfs filesystem to the whole partition:

```bash
localhost core # btrfs filesystem resize max /
Resize '/' of 'max'
```

Using `df -h /` should now show the new size:

```
localhost core # df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda9       110G  537M  109G   1% /
```
