#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import sys, sake, inspect, lib.pacman, lib.error, lib.check, lib.args, lib.str


def main ( inp ) :

	hierarchy, action, inp = findaction( inp, [] )
	args, kwargs = assignarguments( hierarchy, action, inp )
	action( *args, **kwargs )


def findaction ( inp, hierarchy ) :

	# DETERMINE MODULE

	lib.check.ModuleNameSpecified( sake, inp )
	moduleName = inp[0]

	modules = lib.pacman.resolve( moduleName, sake )

	lib.check.ModuleNameExists( sake, moduleName, modules )
	lib.check.ModuleNameNotAmbiguous( moduleName, modules )

	moduleName = modules[0]
	module = getattr( sake, moduleName )

	hierarchy.append( moduleName )


	# DETERMINE ACTION

	lib.check.ActionNameSpecified( inp, moduleName, module )
	actionName = inp[1]

	actions = lib.pacman.resolve( actionName, module )

	lib.check.ActionNameExists( moduleName, module, actionName, actions )
	lib.check.ActionNameNotAmbiguous( moduleName, module, actionName, actions )

	actionName = actions[0]
	action = getattr( module, actionName )

	hierarchy.append( actionName )

	return hierarchy, action, inp[2:]


def assignarguments ( hierarchy, action, inp ) :

	# CHECK ACTION ARGUMENTS

	moduleName = ".".join( hierarchy[:-1] )
	actionName = hierarchy[-1]

	args, kwargs = lib.args.parse( inp, [], {} )

	spec = inspect.getargspec( action )

	kwargslist = lib.args.kwargslist( spec )

	if kwargs :

		lib.check.KwargsNotSupportedException( actionName, kwargslist )

		_kwargs = dict()

		for kwarg in kwargs :

			matching = lib.str.mostlikely( kwarg, kwargslist )

			if not matching and spec.keywords :
				_kwargs[kwarg] = kwargs[kwarg]
			else :
				lib.check.KwargNameExists( kwarg, actionName, matching, kwargslist )
				lib.check.KwargNameNotAmbiguous( kwarg, actionName, matching )

				_kwargs[matching[0]] = kwargs[kwarg]

		kwargs = _kwargs

	# WE INFLATE AFTER RESOLVING KWARGS THUS
	# KWARGS IN JSON ARGS FILES MUST BE
	# EXACTLY MATCHING SPECS OF ACTIONS

	lib.args.inflate( args, kwargs )

	m = ( 0 if spec[0] is None else len( spec[0] ) ) -\
	    ( 0 if spec[3] is None else len( spec[3] ) )
	n = len( args )

	lib.check.NotTooFewArgumentsForAction( moduleName, actionName, n, m, spec )
	lib.check.NotTooManyArgumentsForAction( moduleName, actionName, n, m, spec )


	# DONE
	return args, kwargs


def wrapped ( argv ) :

	try :
		main( argv )

	except lib.error.MainException as e :
		print( e )


if __name__ == '__main__' :
	wrapped( sys.argv[1:] )
