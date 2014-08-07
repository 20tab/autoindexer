#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import jinja2

INDEX = 'index.html'
BASE = '/Users/twentytab/projects/autoindexer'

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='/'))
template = env.get_template(
    os.environ['HOME'] + '/projects/autoindexer/index.jinja'
)

print template


def generate(dirname):
    items = []
    directories = []
    files = []
    print BASE
    base = dirname[len(BASE):]
    print "aaaaaaa", base
    for item in os.listdir(dirname):
        if item.startswith('.'):
            continue
        path = os.path.join(dirname, item)
        items.append(item)
        if os.path.isdir(path):
            generate(path)
    items.sort()
    directories.sort()
    files.sort()
    html = template.render(
        {'base': base, 'dirname': dirname, 'items': items,
         'directories': directories, 'files': files})
    index = os.path.join(dirname, INDEX)
    with open(index, 'w') as f:
        f.write(html)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print "MODIFIED"
        generate(BASE)

if __name__ == "__main__":
    generate(BASE)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
