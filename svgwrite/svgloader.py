#!/usr/bin/env python
#coding:utf-8
# Author:  tuaplicacionpropia
# Purpose: svgloader
# Created: 06.12.2017
# Copyright (C) 2017, Tu aplicación propia
# License: MIT License
"""
The *Drawing* object is the overall container for all SVG
elements. It provides the methods to store the drawing into a file or a
file-like object. If you want to use stylesheets, the reference links
to this stylesheets were also stored (`add_stylesheet`)
in the *Drawing* object.


<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 744.09448819 1052.3622047"
   id="svg3344"
   version="1.1"
   inkscape:version="0.91 r13725"
   sodipodi:docname="test.svg">
  <defs
     id="defs3346" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="375"
     inkscape:cy="520"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1855"
     inkscape:window-height="1056"
     inkscape:window-x="65"
     inkscape:window-y="24"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata3349">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Capa 1"
     inkscape:groupmode="layer"
     id="layer1">
    <rect
       style="fill:#0000ff;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       id="rect3352"
       width="308.57144"
       height="291.42856"
       x="145.71428"
       y="172.3622" />
    <ellipse
       style="fill:#ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       id="path3354"
       cx="534.28571"
       cy="763.79077"
       rx="125.71429"
       ry="114.28571" />
    <path
       sodipodi:type="star"
       style="fill:#ffff00;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       id="path3356"
       sodipodi:sides="5"
       sodipodi:cx="642.85712"
       sodipodi:cy="60.933632"
       sodipodi:r1="234.66869"
       sodipodi:r2="117.33434"
       sodipodi:arg1="0.73372008"
       sodipodi:arg2="1.3620386"
       inkscape:flatsided="false"
       inkscape:rounded="0"
       inkscape:randomized="0"
       d="m 817.14284,218.0765 -149.9688,-42.35596 -119.91142,99.52848 -6.06,-155.71751 -131.71187,-83.286549 146.22351,-53.88276 38.509,-151.002391 96.4311,122.416128 155.51175,-10.038061 -86.62581,129.540089 z"
       inkscape:transform-center-x="15.028686"
       inkscape:transform-center-y="-7.6292184" />
  </g>
</svg>



set/get SVG attributes::

    element['attribute'] = value
    value = element['attribute']

The Drawing object also includes a defs section, add elements to the defs
section by::

    drawing.defs.add(element)

"""
import io
import os.path
import lxml.etree as ET
from lxml import etree, objectify
from svgwrite.elementfactory import factoryelements
from base import BaseElement

class SvgLoader(object):
    """ This is the SVG drawing represented by the top level *svg* element.

    A drawing consists of any number of SVG elements contained within the drawing
    element, stored in the *elements* attribute.

    A drawing can range from an empty drawing (i.e., no content inside of the drawing),
    to a very simple drawing containing a single SVG element such as a *rect*,
    to a complex, deeply nested collection of container elements and graphics elements.
    """
    def __init__(self, **extra):
        """
        :param string filename: filesystem filename valid for :func:`open`
        :param 2-tuple size: width, height
        :param keywords extra: additional svg-attributes for the *SVG* object

        Important (and not SVG Attributes) **extra** parameters:

        :param string profile: ``'tiny | full'`` - define the SVG baseProfile
        :param bool debug: switch validation on/off

        """
        super(SvgLoader, self).__init__(**extra)

    """
      Load elements from svg file
    """
    def load(self, dwg, filename):
        if os.path.isfile(filename):
            self.emptyDrawing(dwg)
            self.doLoad(dwg, filename)

    def emptyDrawing(self, dwg):
        """ Get the XML representation as `ElementTree` object.

        :return: XML `ElementTree` of this object and all its subelements

        """
        dwg.attribs = dict()
        dwg.elements = list()
        dwg._stylesheets = []

    def doLoad(self, dwg, filename):
        print 'begin load'
        parser = etree.XMLParser(remove_blank_text=True, ns_clean=True, no_network=True, load_dtd=False, dtd_validation=False, recover=True)
        tree = etree.parse(filename, parser)
        root = tree.getroot()
        currentNode = root
        self.namespaces = root.nsmap
        
        dwg.attribs['xmlns'] = "http://www.w3.org/2000/svg"
        for key in self.namespaces:
            if key is not None:
                dwg.attribs['xmlns:' + key] = self.namespaces[key]
        
        for key in root.attrib:
            dwg.attribs[key] = root.attrib[key]
        
        for child in root.getchildren():
            elem = self.doLoadItem(child)
            dwg.add(elem)
        
        print 'end load'

    def loadPrefixNamespace(self, url):
        result = ""
        for key in self.namespaces:
            value = self.namespaces[key]
            if value == url:
              result = key
              break
        return result

    def processAttrs(self, node):
        result = dict()
        for key in node.attrib:
            idx = key.rfind('}')
            keyname = key[(idx+1):] if (idx > -1) else key
            prefixUrl = key[1:idx] if (idx > -1) else ""
            print("prefixUrl")
            print(prefixUrl)
            print("namespaces")
            print(self.namespaces)
            prefix = self.loadPrefixNamespace(prefixUrl)
            print("prefix")
            print(prefix)
            prefix = prefix + ":" if len(prefix) > 0 else ""
            newkey = prefix + keyname
            value = node.attrib[key]
            result[newkey] = value
        
        return result

    def doLoadItem(self, node):
        result = None
        print("child")
        print(node.attrib)
        tagname = str(node.tag)
        idx = tagname.rfind('}')
        tagname = tagname[(idx+1):] if (idx > -1) else tagname
        print("tagname")
        print(tagname)
        args = []
        kwargs = self.processAttrs(node)
        print("node.attrib")
        print(kwargs)
        
        if tagname in factoryelements:
            result = factoryelements[tagname](*args, **kwargs)
            print("result.attribs")
            print(result.attribs)
        else:
            result = CustomElement(tagname, *args, **kwargs)
            #result.elementname = tagname
        #result.debug = False

        for attr in result.attribs:
            if attr in kwargs:
                result.attribs[attr] = kwargs[attr]

        for child in node.getchildren():
            subitem = self.doLoadItem(child)
            result.add(subitem)

        return result


class CustomElement(BaseElement):

    def __init__(self, tag, **extra):
        super(CustomElement, self).__init__(**extra)
        self.elementname = tag

