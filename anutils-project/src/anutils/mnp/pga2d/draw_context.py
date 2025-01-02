from ipycanvas import Canvas
import numpy as np
import clifford as cl
from itertools import cycle

DEBUG_GUTTERS = 10

colors = [
    'black',
    'blue',
    'red',
    'purple',
    'orange'
]

class PGADrawContext:
    """
    Helper class for drawing PGA objects
    """
    def __init__(self, layout, blades, width=800, height=600, debug=False, scale=None):
        self.layout = layout
        self.blades = blades
        self.debug = debug
        self.scale = scale
        for key,blade in self.blades.items():
            setattr(self, key, blade)
        self.canvas = Canvas(width=width, height=height)
        self.canvas.layout.width = 'auto'
        self.canvas.layout.height = 'auto'
        self.ps_2_px = np.gcd(width, height)
        d = (DEBUG_GUTTERS if self.debug else 0.0)
        self.bounds = cl.array([
             self.e1 - d * self.e0,
            -self.e1 + (width - d) * self.e0,
             self.e2 - d * self.e0,
            -self.e2 + (height - d) * self.e0
        ])
        self.x_axis, self.y_axis = self.axes = cl.array([
            self.e1 - self.e0*width/2,
            self.e2 - self.e0*height/2
        ])
        self.origin = self.x_axis ^ self.y_axis
        if self.debug:
            self.canvas.stroke_line( d, 0, d, height )
            self.canvas.stroke_line( width - d, 0, width - d, height )
            self.canvas.stroke_line( 0, d, width, d )
            self.canvas.stroke_line( 0, height - d, width, height - d )
            for axis, color in zip(self.axes, ('green', 'red')):
                self._draw_line(axis, color=color)
            self.draw_circle(self.origin, radius=1)
            self._reference_motor()
        self.canvas.line_width = 3.0

    def _point_to_screen(self, p):
        e02 = self.e02
        e01 = self.e01
        e12 = self.e12
        u = np.array([ -p[e02], p[e01] ])
        return u / p[e12] * (self.ps_2_px if self.scale else 1.0)

    def _draw_circle(self, p, color='black', radius=5):
        if p == 0: return
        if p[self.e12] == 0: return
        x, y = self._point_to_screen(p)
        self.canvas.fill_style = color
        self.canvas.fill_circle(x, y, radius=radius)
        self.canvas.fill_style = 'black'

    def _draw_line_segment(self, p0, p1, color='black'):
        if p0[self.e12] == 0: return
        if p1[self.e12] == 0: return
        x0, y0 = self._point_to_screen(p0)
        x1, y1 = self._point_to_screen(p1)
        self.canvas.stroke_style = color
        self.canvas.stroke_line(x0, y0, x1, y1)
        self.canvas.stroke_style = 'black'

    def _draw_line(self, l, ref=None, color='black'):
        if l == 0: return
        ref = ref or self.e12
        intersects = l ^ self.bounds
        valid_intersects = [ i for i in intersects if i[self.e12] != 0 ]
        if len(valid_intersects) < 2: return
        valid_intersects.sort(key=lambda p: (ref & p).mag2())
        a, b = valid_intersects[0:2]
        self._draw_line_segment(a, b, color)

    def _reference_motor(self):
        g = (self.origin & self.e12)
        n = g | self.origin
        r = g | self.e12
        b = (n + r)/2
        if self.debug:
            self._draw_line(g, color='orange')
            self._draw_line(n, color='teal')
            self._draw_line(b, color='purple')
        return r*b

    def draw_circle(self, p, color='black', radius=5):
        q = self._reference_motor()
        s = ~q*p*q
        self._draw_circle(s, color=color, radius=radius)
        return self

    def draw_line(self, l, color='black'):
        q = self._reference_motor()
        x = ~q*l*q
        self._draw_line(x, ref=self.origin, color=color)
        return self

    def draw_polygon(self, clarray, color='black', line_width=1.0):
        for p in clarray:
            self.draw_circle(p, color, radius=1.0 + line_width)
        q = self._reference_motor()
        default_line_width = self.canvas.line_width
        self.canvas.line_width = line_width
        for p0, p1 in zip(clarray, np.roll(clarray, -1)):
            self._draw_line_segment(~q*p0*q, ~q*p1*q, color)
        self.canvas.line_width = default_line_width
        return self
        
    def draw(self, *ms, color='black', radius=5):
        for m, color in zip(ms, cycle(colors)):
            if m(1) != 0: self.draw_line(m(1), color)
            if m(2) != 0: self.draw_circle(m(2), color, radius)
        return self