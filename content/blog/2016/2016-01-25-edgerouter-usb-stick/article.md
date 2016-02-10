Title: Replace broken USB-Stick in Ubiquiti EdgeMax routers
Slug: replace-broken-usb-stick-in-ubiquiti-edgemax-routers
Date: 2016-01-25 19:48
Tags: Ubiquiti, EdgeMax, Recovery
Cover: {static|images/stick.jpg}

In this blog post I'm going to explain how to replace a broken USB-stick in Ubiquiti EdgeMax Routers or in this case the Ubiquiti EdgeMax EdgeRouter-POE.
This guide can also be used to recover from a failed firmware update.

First thing you have to do is to get a new USB-stick.
The stick has to be very slim (basically not wider than the USB-port itself).
Also you have to be a bit careful as the EdgeMax routers are very picky about the stick in use, if your stick takes too long to be recognized by the system it won't boot.
I used an Kingston DataTraveler DTSE9H 8GB USB-stick, which seems to work fine, I think you need at least 4GB for the stick to work as that is the size of the original USB-stick.

To take the EdgeRouter apart take out the screws on the back (you don't need to remove the ground-screw-terminal) and slide the cover from the router.

Internally it looks like this (the stick is on the right-hand side):
![ER-POE internals]({static|images/er-poe-internals.jpg|thumb=1024x_})

To prepare your stick format it with FAT32 using an MBR partition scheme.

![OSX Disk-Utility format dialog]({static|images/diskutility.png|thumb=1024x_})

After formatting the stick go to [http://packages.vyos.net/tools/emrk/0.9c/](http://packages.vyos.net/tools/emrk/0.9c/) and download `emrk-0.9c.bin`.
Copy that file on the stick, eject it and plug it into the internal USB-socket of your router.

Plug a console cable into your router and connect the first network port of the router to your network.
Open a serial terminal on your computer and connect power to the router.

You should see something like this:
![Bootloader prompt with USB info]({static|images/bootloader.png|thumb=1024x_})

The `vmlinux.64` error is normal, it is shown because the stick doesn't contain EdgeOS yet.
Take a good look at the USB section, it should show your USB stick.
If you get any errors or warnings about USB devices the router will not (always) boot!
It may also be a good idea to power-cycle the router a few times just to make sure it recognizes the stick every single time.

After these "debug" messages you are dropped to a bootloader shell.
We want to load `emrk-0.9c.bin` from the stick so we run `fatload usb 0 $loadaddr emrk-0.9c.bin`.
It should print a few dots followed by a message like `15665511 bytes read` and shouldn't display any errors.
When this is done we can boot into that image by executing `bootoctlinux $loadaddr`.
It should now start booting a very minimal Linux (rescue) system, will ask you to accept the disclaimer and you need to configure a network connection (I used DHCP).
The router will need internet access for the next step to work!

In the rescue-system we type `emrk-reinstall` for a full reformat and reinstall of EdgeOS on the stick.
It will ask for an EdgeOS download URL. For ER-lite and ER-POE that URL is (at the time of writing this) `http://dl.ubnt.com/firmwares/edgemax/v1.7.0/ER-e100.v1.7.0.4783374.tar`. You can get that URL from the Firmware Download page on https://ubnt.com.

The whole reinstall process while look like this:
![Log of installation process]({static|images/emrk-reinstall.png|thumb=1024x_})

After this disconnect your network cable (to avoid conflicts) and type `reboot`.
I'd suggest not to disconnect power at this point, as that may corrupt the newly created filesystems as they may not have been completely written to the stick yet). After the reboot it should be fine.

It should now boot EdgeOS from the new stick.
The default login will be `ubnt` as both username and password.
