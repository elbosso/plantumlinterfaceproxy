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

## Backends

### PlantUML

It can be used as a standin for any [Plantuml](https://plantuml.com) server and - as far as plantuml is concerned - it is completely 
transparent. If the user configures the _environment.env_ in such a way that the properties point to a plantuml server all
that functionality still works as it has before.

So for example the following fragment (enclosed in lines containing ` ```plantuml ` and ` ``` `) would be replaced with a rendering of the diagram specified in it:

```
Alice->Bob: hello1
Alice->Bob: hello3
```
### TeX

Now the user has more options: if the first line of the plantuml script is *`%TeX`*, the remaining content of that script is interpreted
as a mathematical formula set with TeX and an image is created from it that then appears instead of the script as with plantuml diagrams. 
An example would be the following fragment (again - enclosed in lines containing ` ```plantuml ` and ` ``` `):

```
%TeX
x^n + y^n = z^n
```

### WireViz

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

### Gnuplot

If the first line of the script starts with *`#gnuplot`* followed by at least one whitespace and a dimension specification in the form of `widthxheight` for example `800x600` then the remainder of the script is processed by [Gnuplot](http://www.gnuplot.info/). This produces a rendering of the contents of the script - the image produced has the dimensions given after `#gnuplot`. This image is returned to Gitlab, replacing the script. An example for this functionality might be the following fragment (enclosed in lines containing ` ```plantuml ` and ` ``` `):

```
#gnuplot 450x800
$data << EOD
0	10.875105	5.637258	5.227558
1	6.135397	5.344249	5.26152
2	5.937079	5.737432	5.586785
3	6.3701	5.490661	5.270509
4	5.931056	5.342314	5.321101
5	6.14734	5.445428	5.43502
6	5.981091	5.442398	5.403112
7	6.4947	5.420989	5.356048
8	5.976686	5.324789	5.5428370000000005
9	6.28498	5.405057	5.388483
EOD


set terminal pngcairo size 450,800 enhanced
set output 'java_map_performanz.png'
set multiplot layout 2, 1 title "Performanz Java Map - Zahlen als Werte,\ndie im Nachhinein geändert werden" font ",12"
set grid
set title 'Vollstääöüßändig (mit Einschwingen des JIT)'
set ylabel 'Zeit (s)'
set xlabel '# Testreihe'
plot '$data' u 1:4 w lp t 'AtomicInteger (Comparable)', '$data' u 1:2 w lp t 'Integer', '$data' u 1:3 w lp t 'AtomicInteger'
set yrange [5.2:6.6]
set title 'Ohne Rücksicht auf Einschwingen des JIT'
plot '$data' u 1:4 w lp t 'AtomicInteger (Comparable)', '$data' u 1:2 w lp t 'Integer', '$data' u 1:3 w lp t 'AtomicInteger'
```
The application is designed to run inside a docker container. The docker-compose file has preparations to integrate with traefik2.x.

The docker container needs an environment file named _environment.env_ defining Properties as given in the file _environment.example_.
After the container is started, an _index.html_ file with some introduction and background is reachable that allows - among other things - 
to access the Swagger UI GUI for experimenting...

## Error Handling

As with the original PlantUML integration - errors during the rendering process are handled by returning HTTP Status *400* and an image
containing the actual error message produced by the backend. So if the user for example makes a mistake inside a TeX formula - TeXs error message is returned rendered in a PNG image so that Gitlab displays it and the user can correct her mistakes.

## Docker

### Building and running

The included _Dockerfile_ is unbiased concerning the architecture - it is based on [debian:latest](https://hub.docker.com/_/debian). A simple

```
docker-compose build
```

should build the image that can then be started by issuing

```
docker-compose up
```

### Configuration

At the moment it relies on two other servers - one for [Plantuml](https://plantuml.com) and one for [WireViz](https://github.com/formatc1702/WireViz). The configuration for both servers are specified by setting environment variables as can be seen in _environment.example_:

```
PLANTUML_HOST=plantuml.docker.lab
PLANTUML_PORT=80
PLANTUML_URL=png
WIREVIZ_HOST=wireviz.docker.lab
WIREVIZ_PORT=80
WIREVIZ_URL=wsgi/png
```

There is no additional configuration item for the Gnuplot renderer. The TeX renderer can be configured with the target resolution in dots per inch (DPI). The default value for this is `150` as can be seen in _environment.example_:

```
TEX_DPI=150
```

As a rule of thumb: the larger this value is, the larger the generated images are.

## Thanks
Thanks go out to [@Tyler-Ward](https://github.com/Tyler-Ward), [@formatc1702](https://github.com/formatc1702) and [@slightlynybbled](https://github.com/slightlynybbled) for their constructive criticism and ideas - they helped a lot!
