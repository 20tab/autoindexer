autoindexer
===========

A python script to implement the auto indexing feature (mod_autoindex in Apache)


requirements:
Jinja2
pathtools
watchdog


uwsgi Example:

```
[uwsgi]
virtualenv = your_virtualenv_path
processes = 1

plugins = python3

static-index = index.html  # or your preferred index file
static-index = autoindex.html  # the auto generated index default name

static-map = /static/autoindexer/=your_lib_path/autoindexer/autoindexer/static

check-static = your_watched_root

# -d = root to watch; -t = jinja template to use; -i indexname to use
attach-daemon = %(virtualenv)/bin/python3 %(workarea_root)/autoindexer/autoindexer/indexer.py -d %(project_    root) -t %(workarea_root)/autoindexer/autoindexer/index.jinja -i autoindex.html
```
