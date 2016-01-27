Title: Change Windows 7 SATA driver mode from AHCI to RAID (Intel Chipset)
Date: 2012-10-25 17:46
Tags: Windows
Slug: change-windows-7-sata-driver-mode-from-ahci-to-raid-intel-chipset
Cover: {static|images/cover.png}

I wanted to use a Intel Rapid Storage controller in "RAID" mode, but Windows 7 didn't like me changing that option and refused to boot, just showing me a very generic bsod.

After quite some time I found a solution:

First start from the installer disc and go to recovery options, open a command prompt.

Look for the system drive, on my system it was just drive C, so typing `c:` changed the current directory to the base directory on that drive.

Next load the registry: `reg load HKLM\TempSys C:\Windows\System32\SYSTEM`

Now you can run `regedit.exe`, go to `HKEY_LOCAL_MACHINE\TempSys`, and look in the control sets in there for `iaStorV` directories.
In all `iaStorV` directories change the option `Start` from `3` to `0`.

After modifying the registry you need to unload it: `reg unload HKLM\TempSys`

Reboot and just hope it works.
