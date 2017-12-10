#! /usr/bin/python
'''
2dgames_shadow.py
An Inkscape effect for adding shadows.
'''

import inkex
import games2d_base

class Shadow(games2d_base.EffectGames2D):
  def __init__(self):
    games2d_base.EffectGames2D.__init__(self)

  #single.svg -> shadow.svg
  '''
    <path
       class="fil95"
       d="m 33.577094,20.283942 0,3.50785 0,1.48817 c 3.22438,0.92125 5.42121,1.87794 6.59049,2.87005 1.45274,1.31102 2.23227,2.90549 2.40943,4.81886 -0.1063,1.02755 -0.38976,2.01967 -0.85039,2.90549 -0.60235,1.09841 -1.34644,2.01966 -2.23226,2.76375 -0.92125,0.70866 -1.87794,1.24015 -2.90549,1.59448 -0.85038,0.28346 -1.87793,0.46062 -3.01178,0.53149 l 0,1.48817 0,0.85039 c 0,0.81495 -0.67322,1.45274 -1.45274,1.45274 l -1.24015,0 c -0.81495,0 -1.45274,-0.63779 -1.45274,-1.45274 l 0,-0.88582 0,-1.48818 c -1.45275,-0.14173 -2.62203,-0.42519 -3.57871,-0.77952 -1.09842,-0.38976 -2.0551,-0.99211 -2.83462,-1.70077 -0.81496,-0.74409 -1.45275,-1.52361 -1.87794,-2.37399 -0.2126,-0.4252 -0.38976,-0.88582 -0.56692,-1.41731 0.17716,-0.14174 0.38976,-0.24803 0.74408,-0.3189 l 4.57083,-0.53149 c 1.20471,-0.28346 1.8425,0 1.8425,0.88582 0,0.49606 0.24803,0.95668 0.63779,1.48817 0.24803,0.35433 0.60236,0.70866 1.06299,0.99212 l 0,-1.45274 0,-4.74799 0,-1.45274 c -2.0551,-0.60236 -3.54328,-1.09842 -4.46453,-1.55905 -0.99212,-0.49605 -1.87794,-1.27558 -2.62203,-2.37399 -0.63779,-0.92125 -0.99211,-2.01967 -1.09841,-3.25981 0.14173,-1.80708 0.88582,-3.36612 2.23226,-4.6417 1.34645,-1.34644 3.36611,-2.12596 5.95271,-2.37399 l 0,-0.56693 c 0,-0.81495 0.63779,-1.45274 1.45274,-1.45274 l 1.24015,0 c 0.77952,0 1.45274,0.63779 1.45274,1.45274 l 0,0.60236 c 2.33856,0.2126 4.14563,0.81495 5.45664,1.8425 0.99212,0.77953 1.77164,1.77164 2.2677,2.97636 -0.14173,0.10629 -0.31889,0.21259 -0.60236,0.28346 l -4.67712,0.70865 c -1.02755,0.17717 -1.20471,-0.49605 -1.34645,-0.74408 -0.17716,-0.38976 -0.35432,-0.67323 -0.49605,-0.85039 -0.17717,-0.17716 -0.35433,-0.35433 -0.60236,-0.53149 l 0,1.45274 z m 0,10.31093 0,1.45275 0,3.82674 0,1.48817 c 0.63779,-0.21259 1.13385,-0.53149 1.48817,-0.92125 0.46063,-0.53149 0.70866,-1.13385 0.70866,-1.77164 0,-0.24803 -0.0354,-0.49606 -0.1063,-0.70865 0.0709,-0.24803 0.1063,-0.49606 0.1063,-0.77952 0,-0.56693 -0.2126,-1.06299 -0.60236,-1.55905 -0.31889,-0.35432 -0.85038,-0.70865 -1.59447,-1.02755 z m -4.14563,-10.55896 0,-1.45274 c -0.38976,0.17716 -0.67323,0.38976 -0.88582,0.63779 -0.28347,0.35433 -0.4252,0.81495 -0.4252,1.31101 0,0.24803 0.0354,0.49606 0.1063,0.74409 -0.0709,0.2126 -0.1063,0.46062 -0.1063,0.70865 0,0.5315 0.14173,0.99212 0.46063,1.38188 0.17716,0.24803 0.46063,0.49606 0.85039,0.67322 l 0,-1.45274 0,-2.55116 z"
       id="path2475"
       inkscape:connector-curvature="0"
       style="clip-rule:evenodd;fill:#fef500;fill-rule:nonzero;image-rendering:optimizeQuality;shape-rendering:geometricPrecision;text-rendering:geometricPrecision" />

    <path
       class="fil95"
       d="m 33.969951,22.105371 0,3.50785 0,1.48817 c 3.22438,0.92125 5.42121,1.87794 6.59049,2.87005 1.45274,1.31102 2.23227,2.90549 2.40943,4.81886 -0.1063,1.02755 -0.38976,2.01967 -0.85039,2.90549 -0.60235,1.09841 -1.34644,2.01966 -2.23226,2.76375 -0.92125,0.70866 -1.87794,1.24015 -2.90549,1.59448 -0.85038,0.28346 -1.87793,0.46062 -3.01178,0.53149 l 0,1.48817 0,0.85039 c 0,0.81495 -0.67322,1.45274 -1.45274,1.45274 l -1.24015,0 c -0.81495,0 -1.45274,-0.63779 -1.45274,-1.45274 l 0,-0.88582 0,-1.48818 c -1.45275,-0.14173 -2.62203,-0.42519 -3.57871,-0.77952 -1.09842,-0.38976 -2.0551,-0.99211 -2.83462,-1.70077 -0.81496,-0.74409 -1.45275,-1.52361 -1.87794,-2.37399 -0.2126,-0.4252 -0.38976,-0.88582 -0.56692,-1.41731 0.17716,-0.14174 0.38976,-0.24803 0.74408,-0.3189 l 4.57083,-0.53149 c 1.20471,-0.28346 1.8425,0 1.8425,0.88582 0,0.49606 0.24803,0.95668 0.63779,1.48817 0.24803,0.35433 0.60236,0.70866 1.06299,0.99212 l 0,-1.45274 0,-4.74799 0,-1.45274 c -2.0551,-0.60236 -3.54328,-1.09842 -4.46453,-1.55905 -0.99212,-0.49605 -1.87794,-1.27558 -2.62203,-2.37399 -0.63779,-0.92125 -0.99211,-2.01967 -1.09841,-3.25981 0.14173,-1.80708 0.88582,-3.36612 2.23226,-4.6417 1.34645,-1.34644 3.36611,-2.12596 5.95271,-2.37399 l 0,-0.56693 c 0,-0.81495 0.63779,-1.45274 1.45274,-1.45274 l 1.24015,0 c 0.77952,0 1.45274,0.63779 1.45274,1.45274 l 0,0.60236 c 2.33856,0.2126 4.14563,0.81495 5.45664,1.8425 0.99212,0.77953 1.77164,1.77164 2.2677,2.97636 -0.14173,0.10629 -0.31889,0.21259 -0.60236,0.28346 l -4.67712,0.70865 c -1.02755,0.17717 -1.20471,-0.49605 -1.34645,-0.74408 -0.17716,-0.38976 -0.35432,-0.67323 -0.49605,-0.85039 -0.17717,-0.17716 -0.35433,-0.35433 -0.60236,-0.53149 l 0,1.45274 z m 0,10.31093 0,1.45275 0,3.82674 0,1.48817 c 0.63779,-0.21259 1.13385,-0.53149 1.48817,-0.92125 0.46063,-0.53149 0.70866,-1.13385 0.70866,-1.77164 0,-0.24803 -0.0354,-0.49606 -0.1063,-0.70865 0.0709,-0.24803 0.1063,-0.49606 0.1063,-0.77952 0,-0.56693 -0.2126,-1.06299 -0.60236,-1.55905 -0.31889,-0.35432 -0.85038,-0.70865 -1.59447,-1.02755 z m -4.14563,-10.55896 0,-1.45274 c -0.38976,0.17716 -0.67323,0.38976 -0.88582,0.63779 -0.28347,0.35433 -0.4252,0.81495 -0.4252,1.31101 0,0.24803 0.0354,0.49606 0.1063,0.74409 -0.0709,0.2126 -0.1063,0.46062 -0.1063,0.70865 0,0.5315 0.14173,0.99212 0.46063,1.38188 0.17716,0.24803 0.46063,0.49606 0.85039,0.67322 l 0,-1.45274 0,-2.55116 z"
       id="path16617"
       inkscape:connector-curvature="0"
       style="clip-rule:evenodd;fill:#808000;fill-rule:nonzero;image-rendering:optimizeQuality;shape-rendering:geometricPrecision;text-rendering:geometricPrecision" />

       d="m 33.577094,20.283942  -> d="m 33.969951,22.105371 
       id="path2475" -> id="path16617"
       style="fill:#fef500;" -> style="fill:#808000;"
  '''

  def _shadow (self, node):
    _clone = self._clone(node)
    self._autogenId(node)
    self._changeStyle(_clone, "fill", "#808000")
    self._translate(_clone, 0.5, 1.0)
    games2d_base._info(str(_clone))
    self._addPrevious(_clone, node)

  def effect(self):
    for id, node in self.selected.iteritems():
      if node.tag == inkex.addNS('path','svg'):
        self._shadow(node)
      else:
        self._shadow(node)
    #_info(str(self._getSelectedObject()))
    #self._shadow(self._getSelectedObject())
    #_error("HOLA3")

if __name__ == '__main__':
    e = Shadow()
    e.affect()