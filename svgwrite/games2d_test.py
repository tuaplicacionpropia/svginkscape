#! /usr/bin/python
# -*- coding: utf-8 -*-

import svgwrite

dwg = svgwrite.Drawing('/root/test.svg', profile='full')
dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2)))
dwg.save()
