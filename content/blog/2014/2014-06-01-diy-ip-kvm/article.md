Title: DIY IP-KVM
Slug: diy-ip-kvm
Date: 2014-06-01 01:07
Category: Projects
Modified: 2016-01-26
Tags: KVM, Olimex, A20 SoC, USB
Cover: {static|images/bios.png}

_Note: This is a slightly updated version of the old blogpost (re-written on 2016/01/25)._

I really like IP-KVMs. They are great devices that allow you to directly connect to and control your computer from basically anywhere in the world, even if your system crashed or your network card died.
Also you can access the bios settings and raid configuration utilities which wouldn't be possible with normal remote-desktop tools.

Some of there devices also have a possibility to attach "virtual media" to your device, essentially allowing you to boot your remote system off an iso image on your local system, giving you a lot of possibilities to reinstall or rescue an operating system.

There are quite a few IP-KVMs on the market, but they are quite expensive (cheap ones starting at over 250€), and they often run outdated and insecure (custom) software.
Also these devices often need Java or Flash for their client software, which is an absolute no-go for me. These tools also often have problems with keyboard layouts, mouse positioning/acceleration and are very slow (low fps and ultra slow speed for virtual media).

It's okay(ish) for rescuing a system, but it's far from good.

So... the plan is to build an IP-KVM myself, keeping price relatively low while having a better user experience than commercial devices.

## Hardware

* [OLinuXino A20 Micro](http://www.amazon.de/gp/product/B00HCM7KO8?linkCode=wey&tag=devurando-21) ~65€
* [VGA zu S-Video Konverter](http://www.amazon.de/gp/product/B003U0PHC8?linkCode=wey&tag=devurando-21) ~20€
* [S-Video Grabber](http://www.amazon.de/gp/product/B0015HXRLQ?linkCode=wey&tag=devurando-21) ~11€
* [STM32F4-Discovery](http://www.amazon.de/gp/product/B00GGCNBAC?linkCode=wey&tag=devurando-21) ~18€

In total with required cables and SD-Card around 150€.

With a few changes in hardware selection the price probably can be under 100€.

### OLinuXino

The OLinuXino A20 Micro is used as the heart of this device.
It controls the video-streaming, keyboard inputs and as it supports USB-OTG it can emulate a USB-connected cd/dvd-drive using a normal ISO file.

Alternatively you can use OLinuXino-Lime(2), Beaglebone Black or similar devices, but if you want to use it as virtual media you need a board with USB-OTG, so that wouldn't work with e.g. a Raspberry Pi.

I originally wanted to use my Beaglebone Black for this experiment, but I accidentally shorted out some Pins and fried my board... Meh.

### VGA -> S-Video -> USB

How do we get a video signal into the device? Well, over USB of course!

I started looking for VGA to USB devices, and I actually found a few, but they were horribly expensive... More expensive than commercial IP-KVM solutions... That's no good.

So we need a workaround...

Quality doesn't really matter as all we need is to be able to read some text and navigate some menus, after all this is just for installing and configuring an OS, and not really anything else. Don't expect ultra fluid low-latency HD graphics for gaming :'D

So... the idea is: People want to connect notebooks and computers to their TVs. What do (almost all) TVs have? S-Video and composite inputs!
So these adapters (VGA->S-Video) are quite cheap, you can grab one for 20€ on Amazon (or quite a bit cheaper directly from China).

I also had a DVB-T stick with S-Video input laying around that I bought for around 80€ a few years back, so I knew that there are cheap(ish) devices for capturing S-Video.
After looking around I found a few USB devices capable of capturing S-Video.
I decided on one that was available for just 11€ on Amazon. There was a cheaper one, which probably would also have worked, but it didn't have any reviews. Directly from China these devices are probably even cheaper.

After trying this out I was quite amazed about the picture quality. I expected far worse.
Only problem I noticed was that sometimes the VGA adapter stops working, but power-cycling always helped, so maybe adding a reset-functionality would solve this problem (components like a mosfet or relay and some other stuff would only be a few euros and could be controlled by the OLinuXino).

As I didn't like having all these cables laying around I decided to combine the capture-stick and the adapter into one device, which now looks like this:

![VGA to USB converter]({static|images/vga_to_usb.jpg|thumb=1024x_})

### STM32F4-Discovery

I found it quite hard to get a combined usb-device running with the old Linux kernel version I was running back when originally writing this blog post, so I decided to use an STM32F4-Discovery as U(S)ART controlled USB keyboard.

At the point of re-writing this post (mostly for translation purposes) the Linux mainline kernel has support for USB-OTG on A20 SoCs, and therefore newer USB-OTG functionality can be used, which should make it actually quite easy to combine HID and virtual media, basically getting rid completely of the STM32F4 in this build.

I may actually try to get this running in the near future. Also I'll probably rewrite most of the software I already had.

## Software

### Linux Kernel

Back when writing this post originally it was best to use the [linux-sunxi](https://github.com/linux-sunxi/linux-sunxi)-kernel on A20 based boards, but nowadays all required features are in linux-mainline and if you want to try to build this yourself you should go with that.

If you want to use the sunxi kernel for whatever reason you'll need to install some backports to get some newer capture devices running.
These can be found on [linuxtv.org](http://linuxtv.org).

I have a [very outdated fork](https://github.com/lukas2511/linux-sunxi) which contains some patches to get these backports to compile and also includes AUFS which I wanted back in the day... no idea why.

To build a Debian package with the kernel, media modules and kernel headers I put together a [small buildsystem](https://github.com/lukas2511/olinuxino-a20-micro/tree/master/kernel).
No idea if that still works.

### Video-Streaming...

...is one of the most complicating things I've ever tried to do on a computer.

I tried tools like [mjpg-streamer](http://sourceforge.net/p/mjpg-streamer/code/HEAD/tree/mjpg-streamer/) (wrong colors and high lag),
some cgi-scripts for capturing single MJPG-frames (memory leak, only 1 client/browser or it would fail),
and I tried some other pieces of software, but all failed eventually, except for [VLC](https://www.videolan.org)...

Nobody on the internet seems to want to stream Video from `/dev/video0` to a browser with low(ish) latency... It was quite some work to get VLC working as intended, and it was especially annoying that the version of VLC without X bindings in the Debian repository wasn't compiled with ffmpeg-encoder-support, so I had to install the full package with all X requirements it had.

So, after all this, here is the magic command that actually worked:

```bash
#!/bin/sh
vlc \
  -I dummy \
  --control dummy \
  --no-disable-screensaver \
  v4l:///dev/video0 \
  :v4l2-standard=NTSC_M \
  :v4l2-input=4 \
  :v4l2-fps=0 \
  :no-v4l2-use-libv4l2 \
  :v4l2-controls-reset \
  \
  :live-caching=100 \
  \
  :sout=#transcode{vcodec=MJPG,width=720,height=480,vb=40000,scale=1,acodec=none,venc=ffmpeg{strict=1}}:http{mux=mpjpeg,dst=127.0.0.1:8080/video.mjpg} \
  :sout-keep \
  --sout-ffmpeg-qscale=1 \
  --sout-http-mime="multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a"
```

If I'd do this again I'd probably take a (brief) look at gstreamer.

### USB CD/DVD-Drive

```bash
modprobe g_mass_storage stall=0 cdrom=1 removable=1 nofua=1
echo /tmp/debian.iso > /sys/devices/platform/sw_usb_udc/gadget/lun0/file
```

Done. It's really that easy.
Don't forget the `stall=0` or your kernel will... stall.

This may be a tiny bit more complicated if you want to combine it with a HID device, but not really much harder.

### Webinterface

The webinterface is a tiny python-script using flask and some client-side javascript.

I don't have the code anymore but here is what it was basically doing:

* Generated a list of ISO-files, providing a selection (including "None") which ISO should be mounted and showing which ISO was currently in use. It basically controls `lun0/file`.
* It received `keyDown` and `keyUp` events, translated the keycodes according to the <strike>configured</strike> hardcoded keyboard layout (this was a bit of a pain to figure out, I now see why pre-build IP-KVMs have problems with this), and sent them over U(S)ART to the STM32F4-Discovery board, which translated it into USB-HID keyboard commands.
* It also had the capability to drive a GPIO pin to reset the STM32F4, and I wanted to have another pin to reset the VGA->S-Video adapter, but i never got around to build that.

### Reverse-Proxy

I'm using [nginx](http://nginx.org) as reverse-proxy to combine the webinterface and mjpg-stream into one page and also to add SSL and authentication.
This was a lot easier than writing this as custom code in the webinterface script.

Here is the important part of the nginx config:

```
	auth_basic "KaputtKVM";
	auth_basic_user_file /etc/nginx/htpasswd;
	default_type application/octet-stream;

	upstream kaputtkvm  {
		server 127.0.0.1:5000;
	}

	upstream videostream  {
		server 127.0.0.1:8080;
	}

	[...]
		location / {
			proxy_pass  http://kaputtkvm;
			proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
			proxy_redirect off;
			proxy_buffering off;
		}

		location /video.mjpg {
			proxy_pass  http://videostream;
			proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
			proxy_redirect off;
			proxy_buffering off;
		}
	[...]
```

## STM32-USB-Keyboard Firmware

...wasn't that much fun either.

I build a [libopencm3](http://libopencm3.org) based [Firmware for the STM32F4-Discovery](https://github.com/lukas2511/STM32-USB-Keyboard) which acts as an U(S)ART controlled USB keyboard.

The firmware was working quite good, but had some problems, especially USB resets weren't really recognized, which sometimes resulted in problems using it in bios.

As I already stated a few times nowadays it's probably better to just do this on the OLinuXino board as well, but that wasn't possible when I first wrote this stuff.
