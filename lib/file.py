import hashlib, lib.dir, shutil, os, os.path


def read(f, callback, blocksize = 2**15):
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		callback(chunk)
		chunk = f.read(blocksize)

def hash(f, h = None, blocksize = 2**15):
	if h is None : h = hashlib.sha256()
	read(f, h.update, blocksize)
	return h

def walk(src, f):

	def callback(path):
		with open(path, 'r') as g : f(g)

	lib.dir.walk(src, f = callback)
	

def move(a, cwd):

	if not isinstance(a, (list)) : a = [a]

	absolute = lambda path : os.path.join(cwd, path)

	for m in a : shutil.move(*map(absolute, m))



def rm(*paths, recursive = False, force = False):

	for path in paths:
		if os.path.isdir(path) : shutil.rmtree(path)
		elif os.path.exists(path) : os.remove(path)
		elif not force : raise Exception("path '%s' does not exist" % path)