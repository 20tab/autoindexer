import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import PurePath
import os
import jinja2
import sys
import getopt
import math


arguments = "d:i:t:D:"

long_arguments = [
    "directory=",
    "index-name=",
    "index-template=",
    # "depth="
]

opts, extraparams = getopt.getopt(sys.argv[1:], arguments, long_arguments)

args = dict(opts)

SLEEP_SECONDS = 1
INDEX = args["-i"] if "-i" in args else 'index.html'
BASE = os.path.abspath(args["-d"])
INDEX_TEMPLATE = args["-t"] if "-t" in args else (BASE + '/' + 'index.jinja')
# DEPTH = int(args["-D"]) if "-D" in args else None
DEPTH = None  # TODO depth to fix

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='/'))
template = env.get_template(
    INDEX_TEMPLATE
)


class Item():

    def __init__(self):
        self.is_dir = False
        self.path = ""
        self.name = ""
        self.base = ""

    def __unicode__(self):
        self.path


def convert_size(size_bytes):

    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def generate(dirname, depth=None):

    items = []
    base = dirname[len(BASE):]
    PARENT = PurePath(base).parent

    for item in os.listdir(dirname):

        if (
            item.startswith('.') or
            item == INDEX or
            item == INDEX_TEMPLATE
        ):
            continue

        item_obj = Item()
        item_obj.name = item
        item_obj.path = os.path.join(dirname, item)
        item_obj.size = convert_size(os.path.getsize(item_obj.path))
        item_obj.base = base
        items.append(item_obj)

        if os.path.isdir(item_obj.path):
            item_obj.is_dir = True
            if depth != 0:
                current_depth = depth
                if depth:
                    current_depth = depth - 1

                generate(item_obj.path, current_depth)

    html = template.render(
        {
            'parent': PARENT,
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
    # observer.schedule(event_handler, path=BASE, recursive=False)
    observer.schedule(event_handler, path=BASE, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
