Title: 🇩🇪 Fledermaus Lichtschranke
Slug: fledermaus-lichtschranke
Date: 2014-03-14 17:20
Category: Projects
Tags: Projects, Bats, Raspberry Pi, BeagleBone, AVR
Cover: {static|images/cover.jpg}

Eine Lichtschrankeninstallation zur Überwachung von Fledermausbewegungen an einem Quartier

Software: [https://github.com/lukas2511/FlederSchranke](https://github.com/lukas2511/FlederSchranke) ([Installationsanleitung](https://github.com/lukas2511/FlederSchranke/wiki/Installationsanleitung))

<!-- PELICAN_END_SUMMARY -->

## Idee

![Blick in die Röhre(n)]({static|images/2013-05-28_23-33-01_hdr.jpg|thumb=1024x_})

Anfang dieses Jahres hat mich Martin vom Bonner Arbeitskreis für Fledermausschutz [BAFF](http://www.der-baff.de/) angeschrieben und mich um Hilfe bei einigen Projekten gebeten um die Bewegungen von Fledermäusen nachvollziehen zu können.

Konkreter ging es in der ersten Mail um eine Lichtschranke, welche an einem Dachbodenfenster montiert werden soll, und dort Aufzeichnen sollte zu welchen Uhrzeiten und zu welchen ungefähren Massen die Fledermäuse ihr Quartier verlassen und betreten.

Martin hatte schon die ersten Ideen und kam beim ersten Treffen mit einem Arduino Mega, einem Ethernet Shield, ein paar Infrarot LEDs und einigen sündhaft teuren Infrarot-Sensoren an. Leider war diese Zusammenstellung an Hardware für den Anwendungsfall nicht wirklich vollständig, und durch die Sensoren auch unnötig teuer.

## Lichtschranke

### Typ 1 - Dreieck

![Erster Prototyp]({static|images/2013-04-21_03-05-06_hdr-1.jpg|thumb=1024x_})

Nach einigem hin und her hatten wir uns geeinigt wie wir die Lichtschranken umsetzen wollten: Es sollten jeweils zwölf IR-Leds und IR-Transistoren gegenüber gesetzt werden, und das ganze dann noch eine Ebene in die Tiefe gezogen werden, so dass es insgesamt 24 Lichtschranken ergibt.

Die LEDs und Transistoren sind in kleine Aluminiumröhrchen montiert um Störungen durch Licht von aussen zu vermeiden, bieten aber auch eine große Hilfe beim ausrichten der einzelnen Teile, welche sich als kniffliger erwies als zunächst gedacht. Falls möglich wollen wir bei einer weiteren Version des Lichtschrankenaufbaus auf einem Metallrahmen setzen, wir befürchten dass sich das Holz womöglich verziehen könnte, was die Lichtschranken unbrauchbar macht.

Die Transistoren haben in unserem Aufbau einen 10kOhm Pull-Up, und die LEDs einen 220Ohm Vorwiderstand. Solang der Transistor das Licht der LED sieht wird die Signalleitung auf 0 gezogen, bei Unterbrechung des Strahls wird die Signalleitung durch den Pull-Up auf 5V gezogen, und kann von unserer Elektronik eingelesen werden.

### Typ 2 - Rechteck

![Zweite Lichtschranke]({static|images/fllogger_mayen_01.jpg|thumb=1024x_})

Wir haben zum Testen unserer Elektronik eine Lichtschranke in einem anderen Format gebaut, um diese hinter einer gekauften Rahmen aus einem anderen Projekt zu testen und nachher die Daten zu vergleichen.<br>
Die Technik ist hier exakt die gleiche.

## Elektronik

### Versuch 1 - Raspberry Pi

![Elektroschrott der irgendwie Lichtschranken gesteuert hat]({static|images/2013-06-13_20-50-28_hdr.jpg|thumb=1024x_})

Unser Aufbau für den ersten Prototypen besteht aus dem bereits erwähnten Arduino Mega, einem Raspberry Pi, einem 3G-Stick für das Hochladen von Logdateien und die Kontrolle von aussen, sowie einem modifizerten USB-Hub bei dem sich die einzelnen Ports aus- und anschalten lassen.<br>
Zusätzlich hat der 3G-Stick noch sein eigenes Relais, so wie einen fetten Kondensator bekommen, da er doch beim einschalten relativ viel Strom zieht, und die Elektronik teilweise beim einschalten des Sticks abgestürzt ist.

Ausserdem befindet sich in der Box ein [Funk-Wetterdatenlogger](http://www.elv.de/usb-wetterdaten-empfaenger-usb-wde1-komplettbausatz.html), da man auch gucken wollte wie sich das Verhalten der Fledermäuse zu bestimmten Wettersituationen verändert.

Auf dem Arduino läuft ein simples Sketch, welches die Signalleitungen der Transistoren einzeln einliest, und bei Veränderung ein Signal über die USB-Verbindung an das Raspberry Pi gibt.<br>
In dem Signal steht welche Lichtschranke sich wie verändert hat, und es ist ein Timestamp (über die micros()-Funktion realisiert) angefügt.<br>
Damit die Zahl der Mikrosekunden nicht überläuft wird das Arduino alle 30 Minuten automatisch rebootet, und gibt an das Raspberry Pi zurück dass es wieder bei 0 anfängt zu zählen.

Auf dem Raspberry Pi laufen zwei Python Scripts, [UMTSkeeper](http://mintakaconciencia.net/squares/umtskeeper/), ein OpenVPN-Client, und ein kleiner Watchdog.

Der Watchdog sorgt dafür dass UMTSkeeper gestartet wird und wartet darauf dass eine Verbindung aufgebaut ist. Sobald eine Verbindung zum Internet verfügbar ist, wird mit ntpdate die Uhrzeit aus dem Netz gezogen, und kurz darauf sowohl NTPd als auch der OpenVPN-Client gestartet.

Das VPN bietet uns eine Möglichkeit von aussen auf das Raspberry Pi zuzugreifen, ohne ginge es nicht, da es im Mobilfunk natürlich hinter einem NAT hängt.

Die Python Scripts loggen relativ simpel die eingehenden Daten mit absoluten Timestamp auf eine seperate Partition der SD-Karte.

Ein Server greift in regelmäßigen Abständen (wenn möglich) auf das Raspberry Pi zu, und zieht sich mittels rsync alle Logs, und löscht die alten Logs von der SD-Karte um Platz zu sparen.

Leider stürzt der Kram regelmäßig ab und reisst SD-Karten mit in den Tod...

### Versuch 2 - BeagleBone

![BeagleBone und Arduino in einer Box, gefüllt mit Heißkleber]({static|images/2014-02-28_05-30-07-1.jpg|thumb=1024x_})

Wir hatten während unserer Tests immer wieder Probleme mit Raspberry Pis im Dauerbetrieb, ausserdem ist die Kombination aus Arduino Mega, Raspberry Pi und USB-Hub doch relativ teuer.

In meinem Regal habe ich dann das BeagleBone Black wiederentdeckt, welches ich mir "damals" kurz nachdem es verfügbar war gekauft habe. Das BeagleBone Black ist um einiges Robuster als das Raspberry Pi, das alte BeagleBone White lief bereits mehrere Monate als Temperaturlogger an meiner Heizung, ohne dass mir irgendwelche Fehler aufgefallen wären.
Es hat genug GPIO-Pins um die Lichtschranken direkt auszuwerten, und es lässt sich auch viel leichter um z.B. eine Echtzeituhr erweitern.

Zusätzlich besitzt das BeagleBone Black eine schnellere CPU (jedoch langsamere GPU, welche wir aber sowieso nicht benötigen), wodurch uns evtl. ermöglicht wird sogar die Auswertung vor Ort vorzunehmen, und/oder Log-Dateien während des Betriebs stärker zu komprimieren (beim Raspberry-Pi gab es bei hoher CPU-Auslastung teilweise Stabilitäts-Probleme).

~~Demnächst wollen wir eine Platine zusammenlöten die auf das BeagleBone Black gesteckt werden soll, dann werde ich diese Seite erweitern.~~<br>
Leider haben wir wegen Zeitdrucks keine Gelegenheit mehr gehabt das Beaglebone selbst als I/O Device zu nutzen, sondern haben es letzenendes einfach als Ersatz für das Raspberry Pi verwendet, womit auch der USB-Hub nicht mehr benötigt wurde, und die Box mit der Elektronik jetzt einigermaßen übersichtlich geworden ist.

## Bilder

Hier noch ein paar weitere Bilder:

![Raspberry Pi Elektronik ausserhalb der Box]({static|images/2013-05-29_00-00-09_hdr.jpg|thumb=1024x_})

![Mit Heißkleber befestigte Kühlkörper auf Raspberry Pi, 5 Sterne, Gerne wieder]({static|images/2013-06-04_04-19-45_hdr.jpg|thumb=1024x_})

![Anschlüsse an der Seite der Box (Video – Zur Statusprüfung, Strom und SD-Karten Slot)]({static|images/2013-06-13_21-58-23_hdr.jpg|thumb=1024x_})

![Fertige erste Lichtschranke]({static|images/2014-03-08_05-07-13.jpg|thumb=1024x_})

