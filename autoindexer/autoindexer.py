# original script by Riccardo Magliocchetti

import os
import jinja2

INDEX = 'unbit.html'
BASE = 'www/cdnjs.unbit.it/cdnjs'

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='/'))
template = env.get_template(os.environ['HOME'] + '/index.jinja')

print template


def generate(dirname):
    items = []
    directories = []
    files = []
    base = dirname[len(BASE):]
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

generate('www')
