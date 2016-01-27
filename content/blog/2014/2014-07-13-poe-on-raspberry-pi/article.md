Title: Power over Ethernet on Raspberry Pi
Slug: poe-on-raspberry-pi
Date: 2014-07-13 23:50
Tags: Raspberry Pi, PoE
Cover: {static|images/closed.jpg}

I have a few devices that support (passive) power-over-ethernet, and I quite like that as I don't need a power supply for every single device filling up my power strip and I even can mount devices further away where there is no power available.

The Raspberry Pi board normally has two ways of getting power: You can either connect a Micro-USB cable, or you can use the GPIO headers to inject power.

I don't like using both of these methods.
Most (cheap) Micro-USB cables I used didn't carry enough power to reliably power the Raspberry Pi, and with GPIO headers you have to connect wires to it every single time (or build a chunky breakout board with a 5V power socket or something).

Since I did have a few switch-mode power supplies laying around that were able to convert down from 24V (my passive-POE voltage) to 5V without any problems I decided to mount one of those inside a Raspberry Pi and connect it to the unused power-carrying pins of the ethernet socket.

## Power over Ethernet

The first thing I needed to do was to actually get to the connections carrying power over the network cable, but that wasn't that easy because the Raspberry Pi is using an RJ45 socket with internal magnetics, so there is no power on the pins on the board! I needed to open and modify that socket.

I carefully pried it open, cut away a piece of plastic and was able to see the 8 pins of the _actual_ RJ45 socket in front of the magnetics.

From left to right those pins are: GND, GND, DATA, 24V, 24V, DATA, DATA, DATA

I connected both ground and 24V pins and attached pieces of wire.

![Inside of RJ45 socket]({static|images/socket.jpg|thumb=1024x_})

## Power Supply 24V -> 5V

So... the "tiny" power supply I had wasn't that tiny after all, it didn't fit nicely into the case I wanted to use, so I had to desolder the Micro-USB socket and the filtering cap. I also needed to desolder and move the 3.3V regulator and naturally I destroyed it while doing that and had to replace it.

![What have I done...]({static|images/inside.jpg|thumb=1024x_})
