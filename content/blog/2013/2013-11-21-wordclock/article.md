Title: Wordclock
Slug: wordclock
Date: 2013-11-21 00:00
Category: Projects
Modified: 2016-01-26
Tags: Clock, AVR, STM32, Lasercutter
Cover: {static|images/screenshot.jpg}

A few months ago somebody used the lasercutter at [Dingfabrik](http://dingfabrik.de/) to cut a box for a clock that shows time using words.
I liked the idea so I asked for a box, and I got one.

Now... originally this should've been a birthday present for my dad, but the controller I built had some problems and I had no time™ and other stuff happened so yea...
I basically finished this about a year later... but hey, it works!

## Hardware (Version 1)

![AVR based hardware]({static|images/avr.jpg|thumb=1024x_})

The controller is based around an ATMega1284P, a small RTC and a DCF77 receiver.

The LEDs for the clock are separated into two sections, the upper half and the lower half.

LEDs for each word are connected, so for each word only 1 pin has to be controlled (with few exceptions).
There even are some times of the day on which the display can be static because only the upper half is used, this time period could be used to sync time using the DCF77 receiver... but I never implemented that.
I tried, but I think the receiver I build into this thing was actually broken.

Since I kinda forgot to add resistors the hardware behaved a bit... weird. Some operations in software made the controller freeze, others just did nothing.
I eventually got it to work, but only for a few days at a time. After a few more fixes it worked weeks at a time.
I kinda started hating this thing, so I didn't bother trying to fix it anymore.

## Software Update (for HW Version 1)

About a year later I started a rewrite of the firmware, mostly because I found the old code and thought to myself that it could be implemented a lot better. So I did that.

After the rewrite the clock worked quite reliable. It ran for months at a time and just crashed a few times in quite a long time.

Then I optimized the firmware again to reduce flicker and delays so the LEDs would be a bit brighter... that was not a good idea. After a few more months the ATMega just died.

So, if you ever want to control a bunch of LEDs... include resistors.

## Hardware (Version 2 - 2015 Update)

![Tiny STM32 board]({static|images/stm32.jpg|thumb=1024x_})

The clock was basically sitting in a corner of my room for a few months after the ATMega broke, I kinda didn't want to fix it, but after a bit of time my dad asked my if I'm ever going to repair it.

At that time I was experimenting with STM32 chips, and I just bought a few cheap boards from eBay, so I thought this would be a great project, especially to test out the new boards.

So, I rebuild the hardware around a small stm32f103c8t6 based board, actually used resistors this time(!), and started working on the software.

## Software (for HW Version 2)

First of: you can find the software [here](https://github.com/lukas2511/wortuhr).

I first implemented just driving the display, then I started implementing code to use the in-chip real-time-clock, and it worked beautifully!

With the old hardware every time I needed to set time (for whatever reason it got lost) I had to use an ISP to flash a firmware setting the time and afterwards flash the old firmware back to the device, that was kinda annoying and I wanted to have a better solution.

Since I also wanted to do more stuff with USB i set for the task of implementing a very simple USB device, using libusb in a tiny python script to set the time, and after a few hours of swearing it actually worked!

The new hard- and software are now running very stable, the clock never ever crashed since i finished the firmware, which at the point of writing this blogpost-update was about 10 months ago.

One problem remains, the RTC drifts slowly (not a perfect quartz), so from time to time I need to correct it.
It is actually possible to implement code to add a minute every few weeks or so, but measuring the drift over time is a bit troublesome as I'm not at home most of the time and since the clock only shows time in 5 minute intervals anyway it's not really a big problem to just set it twice a year or so.
