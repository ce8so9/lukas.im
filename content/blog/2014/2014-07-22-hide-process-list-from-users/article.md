Title: Hide process list from users
Slug: hidepid
Date: 2014-07-22 15:48
Tags: Linux
Cover: {static|images/cover.png}

If you have multiple users on a single machine every user can normally see all running processes, their own, other users processes and even system processes.
Sometimes people append sensitive data like passwords to a command, and since you can see the process list you'll also get that password, which isn't good.

One solution would be to teach all your users to never ever do this, as if that would work...
Also sometimes you may not even do this yourself but an installer script could download a piece of software with the product serial as parameter of the URL or something similar.

The better solution is to hide processes the user isn't controlling.

To do this temporarily you can run `mount -o remount,hidepid=2 /proc`, which will remount `/proc` (the directory containing all process information) with the `hidepid` parameter which will control what a user can see.
As root you'll continue seeing all processes.

To get this as a permanent setting you can alter `/etc/fstab` to have a line for `/proc` looking something like this:

```
proc /proc proc defaults,hidepid=2 0 0
```

[Here](https://www.kernel.org/doc/Documentation/filesystems/proc.txt) under "4.1 Mount options" you can find a few more details.
There also is an option to allow a group to see all processes which could be useful if you have non-root admin accounts.
