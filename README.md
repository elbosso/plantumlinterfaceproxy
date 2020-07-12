# gitlabsvgbadges

<!---
[![start with why](https://img.shields.io/badge/start%20with-why%3F-brightgreen.svg?style=flat)](http://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action)
--->
[![GitHub release](https://img.shields.io/github/release/elbosso/gitlabsvgbadges/all.svg?maxAge=1)](https://GitHub.com/elbosso/gitlabsvgbadges/releases/)
[![GitHub tag](https://img.shields.io/github/tag/elbosso/gitlabsvgbadges.svg)](https://GitHub.com/elbosso/gitlabsvgbadges/tags/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-flask](https://img.shields.io/badge/Made%20with-Flask-blueviolet)](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
[![GitHub license](https://img.shields.io/github/license/elbosso/gitlabsvgbadges.svg)](https://github.com/elbosso/gitlabsvgbadges/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/elbosso/gitlabsvgbadges.svg)](https://GitHub.com/elbosso/gitlabsvgbadges/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/elbosso/gitlabsvgbadges.svg)](https://GitHub.com/elbosso/gitlabsvgbadges/issues?q=is%3Aissue+is%3Aclosed)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/elbosso/gitlabsvgbadges/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/elbosso/gitlabsvgbadges.svg)](https://GitHub.com/elbosso/gitlabsvgbadges/graphs/contributors/)
[![Github All Releases](https://img.shields.io/github/downloads/elbosso/gitlabsvgbadges/total.svg)](https://github.com/elbosso/gitlabsvgbadges)
[![Website elbosso.github.io](https://img.shields.io/website-up-down-green-red/https/elbosso.github.io.svg)](https://elbosso.github.io/)

This project generates SVG images as badges for gitlab. It uses the gitlab API - therefore one must give the app the host and port of the gitlab installation and a secret that allows using the api. All operations have one mandatory parameter or argument - the project id. all other arguments are not mandatory and have sensible defaults.

The application is designed to run inside a docker container. The docker-compose file has preparations to integrate with traefik1.x.

The docker container needs an environment file defining
```
GITLAB_HOST
GITLAB_PORT
GITLAB_SECRET
```
The application can provide badges for

* open issues
* closed issues
* new issues in a specified time interval
* modified issues a specified time interval
* issues not modified for a specified time interval

The exact paths and descriptions for the operations as well as for the parameters can be found in the api - online accessible using the path _/doc_.
