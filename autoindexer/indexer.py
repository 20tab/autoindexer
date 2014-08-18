#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import jinja2
import sys
import getopt
import glob


arguments = "d:i:t:D:"

long_arguments = [
    "directory=",
    "index-name=",
    "index-template=",
    "depth="
]

opts, extraparams = getopt.getopt(sys.argv[1:], arguments, long_arguments)

args = dict(opts)

INDEX = args["-i"] if "-i" in args else 'index.html'
INDEX_TEMPLATE = args["-t"] if "-t" in args else 'index.jinja'
BASE = os.path.abspath(args["-d"])
DEPTH = int(args["-D"]) if "-D" in args else None

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='/'))
template = env.get_template(
    BASE + '/' + INDEX_TEMPLATE
)

print "DEPTH ", DEPTH


class Item():

    def __init__(self):
        self.is_dir = False
        self.path = ""
        self.name = ""
        self.base = ""

    def __unicode__(self):
        self.path


def generate(dirname, depth=None):

    items = []
    base = dirname[len(BASE):]

    for item in os.listdir(dirname):

        if (
            item.startswith('.') or
            item.endswith('.ini') or
            item == INDEX or
            item == INDEX_TEMPLATE or
            item == "indexer.py"
        ):
            continue

        item_obj = Item()
        item_obj.name = item
        item_obj.path = os.path.join(dirname, item)
        item_obj.base = base
        items.append(item_obj)

        if os.path.isdir(item_obj.path):
            item_obj.is_dir = True
            if depth != 0:
                current_depth = depth
                if depth:
                    current_depth = depth-1

                generate(item_obj.path, current_depth)

    html = template.render(
        {
            'base': base,
            'dirname': dirname,
            'items': items,
        }
    )

    index = os.path.join(dirname, INDEX)

    with open(index, 'w') as f:
        f.write(html)


class IndexerHandler(FileSystemEventHandler):

    def on_modified(self, event):
        generate(BASE, DEPTH)

if __name__ == "__main__":
    generate(BASE, DEPTH)
    event_handler = IndexerHandler()
    observer = Observer()
    observer.schedule(event_handler, path=BASE, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
