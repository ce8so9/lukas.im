Title: letsencrypt.sh
Date: 2016-02-10 12:49
Tags: letsencrypt, letsencrypt.sh, bash, crypto, ssl
Cover: {static|images/letsencrypt.sh.png}

Trusted SSL certificates used to cost money, but in the past companies like StartCom already started to hand out domain-verified certificates for free,
but now we have Let's Encrypt, which takes a different approach.

<!-- PELICAN_END_SUMMARY -->

### How it used to work in the past

Getting one of those certificates usually involved signing up for an account,
starting a domain verification by letting StartCom send you a pin to an email address associated with your domain,
starting the signing process by either letting startcom generate a key for you or uploading a CSR,
waiting a few minutes to hours until your certificate got signed,
installing the certificate on your server, looking at tons of forum entries to exactly know which CA certificates to include in your certificate chain,
and just like that, you had your site available over trusted https! Yay! \o/

### Let's Encrypt!

Let's Encrypt takes a different approach.

Instead of you having to do all these manual steps it was designed to be nearly fully automatic.
The whole process from registering an account to getting your domain signed only takes a few seconds.<br>
It also can install the certificate for you, no more hassle trying to figure out which files to use!

Isn't that great?! Yay! \o/

### Well... kinda... but.

The official client is great if you are just getting started setting up a server,
having a simple webserver configuration and absolutely nothing writing to your config files.
In a lot of automated and/or more complex setups this will fail.

Not so great, but okay, with some additional parameters it basically allows you to work around this.

### curl | sh...ish

A different problem (at least for me) was the approach of how this updates itself.
Every time you run the official client it looks for a newer version of itself and may also install some python modules into it's virtualenv.
It mostly doesn't use your package manager, and it downloads and runs code (intended to run as root!) automatically, which is kinda bad.

You can install all the requirements manually and set it up to now download stuff, but that's kinda annoying.

### No space left on device

Another problem is the size of the requirements.
The client is written in python, requiring you to basically install python and all the other requirements,
which is quite big, and may result in a few problems on some systems that just don't have much space.

Think of a tiny ARM-based linux board with 1G nand (or even smaller, like 128MB in a router or something similar).
You really don't want that stuff on there.

This is where [letsencrypt.sh](https://github.com/lukas2511/letsencrypt.sh) comes in.

### [letsencrypt.sh](https://github.com/lukas2511/letsencrypt.sh)

I was reading [Hacker News](https://news.ycombinator.com) when I found a link to a [very tiny python based client](https://github.com/diafygi/acme-tiny) for letsencrypt.

Reading the script I noticed that most of the important stuff was just wrapped around the openssl binary,
and when it comes to wrapping stuff around a binary what do I think of? My shell of course!

I started with a very simple proof of concept, basically being just able to send a request to Boulder (the server-side of ACME, the protocol used by Let's Encrypt).<br>
This initial step was basically just trying to register an account key with Let's Encrypt, and after that worked I started expanding the script,
and finally pushed a first version to GitHub.

This first version was very simple, it generated a key and signing-request, created the files needed for domain verification, and finally received the certificate from Boulder.
Nothing too complicated, but well... There was little to no error handling, it was working, but if something went wrong you could easily have erased your certificate...
Not so great...

But that was fixed, there is a lot more error handling, also old certificates and keys are not deleted, just a symlink gets changed,
so if anything still goes wrong you can easily go back to the last working state.

It now also works on BSD and with ZSH instead of just GNU/Linux and Bash.

People started adding a lot of features to letsencrypt.sh:

- certificate revocation (thanks to [germeier](https://github.com/germeier))
- expiration checks (thanks to [tralafiti](https://github.com/tralafiti))
- domain name config change detection (thanks to [germeier](https://github.com/germeier))
- DNS-01 verification (thanks to [germeier](https://github.com/germeier))
- support for Elliptic Curve Cryptography (thanks to [germeier](https://github.com/germeier))
- signing of custom CSRs (thanks to [nielslaukens](https://github.com/nielslaukens))
- custom hooks at a lot of places inside letsencrypt.sh (initial implementation thanks to [rudis](https://github.com/rudis))

What started as a simple proof of concept is now basically a fully fledged client for Let's Encrypt (or any other ACME server).

Also thanks to all the other people who contributed to this project up to now or in the future!
Have a look at the [contributors graph](https://github.com/lukas2511/letsencrypt.sh/graphs/contributors) to see who else worked on this.
