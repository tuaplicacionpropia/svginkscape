#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
inkex.py
A helper module for creating Inkscape extensions

Copyright (C) 2005,2010 Aaron Spike <aaron@ekips.org> and contributors

Contributors:
  Aurélio A. Heckert <aurium(a)gmail.com>
  Bulia Byak <buliabyak@users.sf.net>
  Nicolas Dufour, nicoduf@yahoo.fr
  Peter J. R. Moulder <pjrm@users.sourceforge.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
import copy
import gettext
import optparse
import os
import random
import re
import sys
from math import *
import svgwrite

#a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = {
u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
u'cc'       :u'http://creativecommons.org/ns#',
u'ccOLD'    :u'http://web.resource.org/cc/',
u'svg'      :u'http://www.w3.org/2000/svg',
u'dc'       :u'http://purl.org/dc/elements/1.1/',
u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
u'xlink'    :u'http://www.w3.org/1999/xlink',
u'xml'      :u'http://www.w3.org/XML/1998/namespace'
}

'''
hola
sys.argv
['games2d_prueba.py', '--id=text4136', '/tmp/ink_ext_XXXXXX.svgANCXAZ']
os.environ
'HOME': '/home/jmramoss', 
'LANG': 'es_ES.UTF-8', 
'SHELL': '/bin/bash', 
'LANGUAGE': 'es_ES', 
'GIO_LAUNCHED_DESKTOP_FILE': '/usr/share/applications/inkscape.desktop', 
'PYTHONPATH': '/usr/share/inkscape/extensions', 
'PATH': '/usr/local/sbin:/usr/local/bin', 
'GDM_LANG': 'es_ES', 
'PWD': '/home/jmramoss', 
'PACKAGE_LOCALE_DIR': '/usr/share/locale', 
'INKSCAPE_LOCALEDIR': '/usr/share/locale', 
'USER': 'jmramoss'

'''

'''
sys.argv
['games2d_prueba.py', 
'--id=text4136', 
'--id=rect8067', 
'--active-tab="dxfpoints"', 
'--dxfpoints-action=save', 
'--filename=output.ngc', 
'--add-numeric-suffix-to-filename=true', 
'--directory=/home', 
'--Zsafe=5', 
'--unit=G21 (All units in mm)', 
'--postprocessor= ', 
'--create-log=false', 
'/tmp/ink_ext_XXXXXX.svgG8DJAZ']
'''

class InkExtension:
    """A class for creating Inkscape SVG Effects"""

    def __init__(self, *args, **kwargs):
        self.args=None
        self.script_file=None
        self.svg_file=None
        self.selected_ids=[]
        self.selected=[]
        self.options=dict()

        self.dwg=None
        #self.original_document=None

    def effect(self, dwg, selected, options):
        result = False
        return result

    def debug(what):
        sys.stderr.write(str(what) + "\n")
        return what

    def errormsg(msg):
        if isinstance(msg, unicode):
            sys.stderr.write(msg.encode("UTF-8") + "\n")
        else:
            sys.stderr.write((unicode(msg, "utf-8", errors='replace') + "\n").encode("UTF-8"))

    def parseArgs(self):
        """Parse document in specified file or on stdin"""
        self.args = sys.argv
        
        numArgs = len(sys.argv)
        if numArgs > 0:
            self.script_file = sys.argv[0]
            self.svg_file = sys.argv[numArgs - 1]
            for i in range(1, numArgs):
                arg = sys.argv[i]
                if arg.startswith('--id='):
                    idElem = arg[len('--id='):]
                    self.selected_ids.append(idElem)
                elif arg.startswith('--'):
                    assign = arg[len('--'):]
                    keyvalue = assign.split('=')
                    key = keyvalue[0]
                    value = keyvalue[1]
                    self.options[key] = value

    '''
        p = etree.XMLParser(huge_tree=True)
        self.document = etree.parse(stream, parser=p)
        self.original_document = copy.deepcopy(self.document)
        stream.close()
    '''

    def output(self):
        """Serialize document into XML on stdout"""
        original = etree.tostring(self.original_document)        
        result = etree.tostring(self.document)        
        if original != result:
            self.document.write(sys.stdout)

    def load (self):
        self.dwg = svgwrite.Drawing(self.svg_file, profile='full', debug=False)
        pass

    def select (self):
        for idElem in self.selected_ids:
            elem = self.dwg.getElementById(idElem)
            if elem is not None:
                self.selected.append(elem)

    def affect(self):
        """Affect an SVG document with a callback effect"""
        sys.stderr.write('sys.argv' + '\n')
        sys.stderr.write(str(sys.argv) + '\n')
        sys.stderr.write('os.environ' + '\n')
        sys.stderr.write(str(os.environ) + '\n')
        
        self.parseArgs()
        self.load()
        self.select()
        
        sys.stderr.write('self.args' + '\n')
        sys.stderr.write(str(self.args) + '\n')

        sys.stderr.write('self.script_file' + '\n')
        sys.stderr.write(str(self.script_file) + '\n')

        sys.stderr.write('self.svg_file' + '\n')
        sys.stderr.write(str(self.svg_file) + '\n')

        sys.stderr.write('self.selected_ids' + '\n')
        sys.stderr.write(str(self.selected_ids) + '\n')

        sys.stderr.write('self.options' + '\n')
        sys.stderr.write(str(self.options) + '\n')
        
        output = self.effect(self.dwg, self.selected, self.options)
        output = True
        if output:
            self.dwg.write(sys.stdout, False)

        '''
        self.svg_file = args[-1]
        self.getoptions(args)
        self.parse()
        self.getposinlayer()
        self.getselected()
        self.getdocids()
        self.effect()
        if output: self.output()
        '''
