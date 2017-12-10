#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: drawing
# Created: 10.09.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License
"""
The *Drawing* object is the overall container for all SVG
elements. It provides the methods to store the drawing into a file or a
file-like object. If you want to use stylesheets, the reference links
to this stylesheets were also stored (`add_stylesheet`)
in the *Drawing* object.

set/get SVG attributes::

    element['attribute'] = value
    value = element['attribute']

The Drawing object also includes a defs section, add elements to the defs
section by::

    drawing.defs.add(element)

"""
from __future__ import unicode_literals
import io
import os.path

from svgwrite.container import SVG, Defs
from svgwrite.elementfactory import ElementFactory
from svgwrite.utils import pretty_xml
from svgwrite.svgloader import SvgLoader

class Drawing(SVG, ElementFactory):
    """ This is the SVG drawing represented by the top level *svg* element.

    A drawing consists of any number of SVG elements contained within the drawing
    element, stored in the *elements* attribute.

    A drawing can range from an empty drawing (i.e., no content inside of the drawing),
    to a very simple drawing containing a single SVG element such as a *rect*,
    to a complex, deeply nested collection of container elements and graphics elements.
    """
    def __init__(self, filename="noname.svg", size=('100%', '100%'), **extra):
        """
        :param string filename: filesystem filename valid for :func:`open`
        :param 2-tuple size: width, height
        :param keywords extra: additional svg-attributes for the *SVG* object

        Important (and not SVG Attributes) **extra** parameters:

        :param string profile: ``'tiny | full'`` - define the SVG baseProfile
        :param bool debug: switch validation on/off

        """
        super(Drawing, self).__init__(size=size, **extra)
        self.filename = filename
        self._stylesheets = []  # list of stylesheets appended
        self.load_xml()


    # defines view_center in terms of document units
    def getposinlayer(self):
        #defaults
        self.current_layer = self.document.getroot()
        self.view_center = (0.0,0.0)

        layerattr = self.document.xpath('//sodipodi:namedview/@inkscape:current-layer', namespaces=NSS)
        if layerattr:
            layername = layerattr[0]
            layer = self.document.xpath('//svg:g[@id="%s"]' % layername, namespaces=NSS)
            if layer:
                self.current_layer = layer[0]

        xattr = self.document.xpath('//sodipodi:namedview/@inkscape:cx', namespaces=NSS)
        yattr = self.document.xpath('//sodipodi:namedview/@inkscape:cy', namespaces=NSS)
        if xattr and yattr:
            x = self.unittouu( xattr[0] + 'px' )
            y = self.unittouu( yattr[0] + 'px')
            doc_height = self.unittouu(self.document.getroot().get('height'))
            if x and y:
                self.view_center = (float(x), doc_height - float(y)) # FIXME: y-coordinate flip, eliminate it when it's gone in Inkscape

    def getNamedView(self):
        return self.document.xpath('//sodipodi:namedview', namespaces=NSS)[0]

    def createGuide(self, posX, posY, angle):
        atts = {
          'position': str(posX)+','+str(posY),
          'orientation': str(sin(radians(angle)))+','+str(-cos(radians(angle)))
          }
        guide = etree.SubElement(
                  self.getNamedView(),
                  addNS('guide','sodipodi'), atts )
        return guide

    #a dictionary of unit to user unit conversion factors
    __uuconv = {'in':90.0, 'pt':1.25, 'px':1.0, 'mm':3.5433070866, 'cm':35.433070866, 'm':3543.3070866,
              'km':3543307.0866, 'pc':15.0, 'yd':3240.0 , 'ft':1080.0}

    # Function returns the unit used for the values in SVG.
    # For lack of an attribute in SVG that explicitly defines what units are used for SVG coordinates,
    # try to calculate the unit from the SVG width and SVG viewbox.
    # Defaults to 'px' units.
    def getDocumentUnit(self):
        svgunit = 'px' #default to pixels

        svgwidth = self.document.getroot().get('width')
        viewboxstr = self.document.getroot().get('viewBox')
        if viewboxstr:
            unitmatch = re.compile('(%s)$' % '|'.join(self.__uuconv.keys()))
            param = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')

            p = param.match(svgwidth)
            u = unitmatch.search(svgwidth)    
            
            width = 100 #default
            viewboxwidth = 100 #default
            svgwidthunit = 'px' #default assume 'px' unit
            if p:
                width = float(p.string[p.start():p.end()])
            else:
                errormsg(_("SVG Width not set correctly! Assuming width = 100"))
            if u:
                svgwidthunit = u.string[u.start():u.end()]

            viewboxnumbers = []
            for t in viewboxstr.split():
                try:
                    viewboxnumbers.append(float(t))
                except ValueError:
                    pass
            if len(viewboxnumbers) == 4:  #check for correct number of numbers
                viewboxwidth = viewboxnumbers[2]

            svgunitfactor = self.__uuconv[svgwidthunit] * width / viewboxwidth

            # try to find the svgunitfactor in the list of units known. If we don't find something, ...
            eps = 0.01 #allow 1% error in factor
            for key in self.__uuconv:
                if are_near_relative(self.__uuconv[key], svgunitfactor, eps):
                    #found match!
                    svgunit = key;

        return svgunit


    def unittouu(self, string):
        '''Returns userunits given a string representation of units in another system'''
        unit = re.compile('(%s)$' % '|'.join(self.__uuconv.keys()))
        param = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')

        p = param.match(string)
        u = unit.search(string)    
        if p:
            retval = float(p.string[p.start():p.end()])
        else:
            retval = 0.0
        if u:
            try:
                return retval * (self.__uuconv[u.string[u.start():u.end()]] / self.__uuconv[self.getDocumentUnit()])
            except KeyError:
                pass
        else: # default assume 'px' unit
            return retval / self.__uuconv[self.getDocumentUnit()]

        return retval

    def uutounit(self, val, unit):
        return val / (self.__uuconv[unit] / self.__uuconv[self.getDocumentUnit()])

    def addDocumentUnit(self, value):
        ''' Add document unit when no unit is specified in the string '''
        try:
            float(value)
            return value + self.getDocumentUnit()
        except ValueError:
            return value







    """
      Load elements from svg file
    """
    def load_xml(self):
        if os.path.isfile(self.filename):
          SvgLoader().load(self, self.filename)

    def get_xml(self):
        """ Get the XML representation as `ElementTree` object.

        :return: XML `ElementTree` of this object and all its subelements

        """
        profile = self.profile
        version = self.version
        self.attribs['xmlns'] = "http://www.w3.org/2000/svg"
        self.attribs['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
        self.attribs['xmlns:ev'] = "http://www.w3.org/2001/xml-events"

        self.attribs['baseProfile'] = profile
        self.attribs['version'] = version
        return super(Drawing, self).get_xml()

    def add_stylesheet(self, href, title, alternate="no", media="screen"):
        """ Add a stylesheet reference.

        :param string href: link to stylesheet <URI>
        :param string title: name of stylesheet
        :param string alternate: ``'yes'|'no'``
        :param string media: ``'all | aureal | braille | embossed | handheld | print | projection | screen | tty | tv'``

        """
        self._stylesheets.append((href, title, alternate, media))

    def write(self, fileobj, pretty=False):
        """ Write XML string to **fileobj**.

        :param fileobj: a *file-like* object
        :param pretty: True for easy readable output

        Python 3.x - set encoding at the open command::

            open('filename', 'w', encoding='utf-8')
        """
        # write xml header
        fileobj.write('<?xml version="1.0" encoding="utf-8" ?>\n')

        # don't use DOCTYPE. It's useless. see also:
        # http://tech.groups.yahoo.com/group/svg-developers/message/48562
        # write stylesheets
        stylesheet_template = '<?xml-stylesheet href="%s" type="text/css" ' \
            'title="%s" alternate="%s" media="%s"?>\n'
        # removed map(), does not work with Python 3
        for stylesheet in self._stylesheets:
            fileobj.write(stylesheet_template % stylesheet)

        xml_string = self.tostring()
        if pretty:  # write easy readable XML file
            xml_string = pretty_xml(xml_string)
        fileobj.write(xml_string)

    def save(self, pretty=False):
        """ Write the XML string to **filename**. """
        fileobj = io.open(self.filename, mode='w', encoding='utf-8')
        self.write(fileobj, pretty=pretty)
        fileobj.close()

    def saveas(self, filename, pretty=False):
        """ Write the XML string to **filename**.

        :param string filename: filesystem filename valid for :func:`open`
        :param pretty: True for easy readable output
        """
        self.filename = filename
        self.save(pretty=pretty)
