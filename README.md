# plantumlinterfaceproxy

<!---
[![start with why](https://img.shields.io/badge/start%20with-why%3F-brightgreen.svg?style=flat)](http://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action)
--->
[![GitHub release](https://img.shields.io/github/release/elbosso/plantumlinterfaceproxy/all.svg?maxAge=1)](https://GitHub.com/elbosso/plantumlinterfaceproxy/releases/)
[![GitHub tag](https://img.shields.io/github/tag/elbosso/plantumlinterfaceproxy.svg)](https://GitHub.com/elbosso/plantumlinterfaceproxy/tags/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-flask](https://img.shields.io/badge/Made%20with-Flask-blueviolet)](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
[![GitHub license](https://img.shields.io/github/license/elbosso/plantumlinterfaceproxy.svg)](https://github.com/elbosso/plantumlinterfaceproxy/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/elbosso/plantumlinterfaceproxy.svg)](https://GitHub.com/elbosso/plantumlinterfaceproxy/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/elbosso/plantumlinterfaceproxy.svg)](https://GitHub.com/elbosso/plantumlinterfaceproxy/issues?q=is%3Aissue+is%3Aclosed)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/elbosso/plantumlinterfaceproxy/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/elbosso/plantumlinterfaceproxy.svg)](https://GitHub.com/elbosso/plantumlinterfaceproxy/graphs/contributors/)
[![Github All Releases](https://img.shields.io/github/downloads/elbosso/plantumlinterfaceproxy/total.svg)](https://github.com/elbosso/plantumlinterfaceproxy)
[![Website elbosso.github.io](https://img.shields.io/website-up-down-green-red/https/elbosso.github.io.svg)](https://elbosso.github.io/)

[![Small video for illustration purposes...](http://img.youtube.com/vi/gB1UfRYJoYc/maxresdefault.jpg)](http://www.youtube.com/watch?v=gB1UfRYJoYc "")

This project acts as a backend for the [gitlab](https://about.gitlab.com/) [plantuml](https://plantuml.com/) [integration](https://docs.gitlab.com/ee/administration/integration/plantuml.html):

It can be used as a standin for any plantuml server and - as far as plantuml is concerned - it is completely 
transparent. If the user configures the _environment.env_ in such a way that the properties point to a plantuml server all
that functionality still works as it has before.

So for example the following fragment (enclosed in lines containing ` ```plantuml ` and ` ``` `) would be replaced with a rendering of the diagram specified in it:

```
Alice->Bob: hello1
Alice->Bob: hello3
```

Now the user has more options: if the first line of the plantuml script is *`%TeX`*, the remaining content of that script is interpreted
as a mathematical formula set with TeX and an image is created from it that then appears instead of the script as with plantuml diagrams. 
An example would be the following fragment (again - enclosed in lines containing ` ```plantuml ` and ` ``` `):

```
%TeX
x^n + y^n = z^n
```

If the first line of the script is *`wireviz`* then the remainder of the script is sent on to a [WireViz](https://github.com/formatc1702/WireViz) renderer. This renderer produces and
image and that image is returned to gitlab, replacing the script. An example for this functionality might be the following fragment (enclosed in lines containing ` ```plantuml ` and ` ``` `):

```
#wireviz
connectors:
  X1:
    type: D-Sub
    subtype: female
    pinout: [DCD, RX, TX, DTR, GND, DSR, RTS, CTS, RI]
  X2:
    type: Molex KK 254
    subtype: female
    pinout: [GND, RX, TX]

cables:
  W1:
    gauge: 0.25 mm2
    length: 0.2
    color_code: DIN
    wirecount: 3
    shield: true

connections:
  -
    - X1: [5,2,3]
    - W1: [1,2,3]
    - X2: [1,3,2]
  -
    - X1: 5
    - W1: s
```

The application is designed to run inside a docker container. The docker-compose file has preparations to integrate with traefik2.x.

The docker container needs an environment file named _environment.env_ defining Properties as given in the file _environment.example_.
After the container is started, an _index.html_ file with some introduction and background is reachable that allows - among other things - 
to access the Swagger UI GUI for experimenting...
