Title: Mac App: Wineskin Winery
Slug: mac-app-wineskin-winery
Date: 2012-08-04 19:21
Tags: OS X, App, Wine
Cover: {static|images/cover.png}

Sometimes there is the need to run a piece of Windows software, and if you don't have Windows running on your system you will need a workaround. Solutions are using a virtual machine with Windows or using wine, which can sometimes be a bit annoying.

As a mac user there is a solution that makes wine a bit more comfortable: [Wineskin Winery](http://wineskin.urgesoftware.com/tiki-index.php)
It's (obviously) based on [wine](https://winehq.org) and bundles Windows programs as Mac apps, including a fancy Icon in your Dock while it is running!

<p style="float: right;">
<img src="{static|images/winery.png|thumb=1024x_}" />
</p>

When you first start Wineskin you have to download a wine version.
That can be done in just three clicks, just take the suggested (newest stable) version.
If you know that the application you want to bundle is working best under an older wine version you can select that instead (e.g. Warcraft III had problems in the past the reappeared from time to time in newer versions, but this should be solved by now).

You'll also need to update the wrapper, which can be done with a click on the Update button.

Now you are ready to create your first wrapper. Click on the button to create a new blank wrapper, and it will ask you for the name of the application you want to install.
On newer versions of wine you'll also be asked if you want to install mono (open .NET implementation) and gecko (IE-like HTML rendering library). I'd suggest to do that, as most Windows software needs one or even both of those libraries.

After the wrapper is created just start it as if it was a normal app. You'll get a menu that asks you what you want to do, you can install software from a setup executable, copy over existing files, or do advanced configuration. If your installer asks for a target location make sure to select a location under C:\\.

When everything installed without problems you'll get a dialog asking you for the executable of the program you just installed (e.g. putty.exe), and you'll have the option to set an app icon.
You can also do some advanced stuff like opening regedit to set some options (e.g. for Warcraft III you may want to enable OpenGL rendering and maybe window-mode).

After this the app is build. If you want to make some changes at a later point you can right-click the app, select "Show Package Contents", and open the Wineskin app you'll find inside.
This can be useful if e.g. you want to install an expansion pack for a game.

All these bundles are normally written to a location under `/Users/$username/Applications/Wineskin`, but you can move and copy them without any problems.
I even copied a few apps over to another mac and they worked fine.

The only downside I see with Wineskin is the size of the bundles you create. As every bundle contains wine, the wineskin wrapper software, a few Windows libraries and temporary files and of course the software you installed those apps can get quite big.
My putty wrapper had a size of 350MB, where putty itself only takes around 0.5MB... yea... but since this only is for the rare case that you may need to run a Windows application and you'll only have very few of those I guess it's okay.
