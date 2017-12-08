#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  tuaplicacionpropia
# Purpose: svg examples
# Created: 06.12.2017
# Copyright (C) 2017, Tu aplicación propia
# License: MIT License

print 'hola'

import svgwrite

print "dos"

def use(name):
    dwg = svgwrite.Drawing(name, profile='full', debug=False)
    dwg.add(dwg.line((0, 0), (1000, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
    dwg.add(dwg.text('Test', insert=(0, 500.2)))
    dwg.saveas("/home/jmramoss/HD1/PROYECTOS/apps/svgwrite/examples/test4.svg")

print "tres"

if __name__ == '__main__':
    use("/home/jmramoss/HD1/PROYECTOS/apps/svgwrite/examples/test.svg")
    print "fin"
