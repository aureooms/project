import os

root = os.path.dirname(os.path.abspath(__file__))
module = os.path.basename(root)

for f in os.listdir(root):
	path = root + '/' + f
	if os.path.isfile(path) and f != '__init__.py':
		name, ext = os.path.splitext(f)

		if ext == '.py' : __import__(module + '.' + name)

os = None