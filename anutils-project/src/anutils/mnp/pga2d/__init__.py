import re
import clifford as cl
import numpy as np

def blade_key_to_tex(blade_key):
    match = re.match(r'([a-zA-Z]+)([0-9]+)?', blade_key)
    if not match: return blade_key
    var, index = match.groups()
    tex = f'\\mathbf{{{var}}}'
    tex += f'_{{{index}}}' if index else ''
    return tex
    

def build_tex_format_for_layout(layout, precision=1):
    def tex_func(mv):
        float_fmt = f'{{:0.{precision}f}}'.format
        if type(mv) in (float, np.float32, np.float64): return float_fmt(mv)
        if type(mv) is not cl.MultiVector: return str(mv)
        terms = [
            (coeff < 0.0, f'{"" if (blade_key != "" and np.isclose(abs(coeff), 1.0, atol=0.1**precision)) else float_fmt(abs(coeff))}{blade_key_to_tex(blade_key)}')
            for coeff, blade_key
            in zip(mv.as_array(), layout.blades.keys()) 
            if not np.isclose(abs(coeff), 0, atol=0.1**precision)
        ]
        if len(terms) == 0: return float_fmt(0)
        operations = [ ('-' if terms[0][0] else '')+terms[0][1] ] 
        operations += sum([[ '-' if neg else '+', term ] for neg, term in terms[1:]], [])
        return ' '.join(operations)
    return tex_func


def box_coords(dim):
    binaries = [ f'{{:0{dim}b}}'.format(i) for i in range(2**dim) ]
    coords = np.array([ list(map(float, b)) for b in binaries ])
    return coords - 0.5*np.ones(dim)


fct = factorial = np.vectorize(lambda n: np.arange(1,n+1).prod(), otypes=(int,))
npr = n_permute_r = np.vectorize(lambda n, r: fct(n)//fct(n - r), otypes=(int,))
ncr = n_choose_r = np.vectorize(lambda n, r: npr(n, r)//fct(r), otypes=(int,))

def numpy_array_to_tex_matrix(array, type=''):
    def n2s(num):
        if np.isclose(num, 0):
            return '0'
        else:
            return '{:0.1f}'.format(num)
    return '\\begin{' + type + 'matrix}' \
        + '\\\\\n'.join(' & '.join(map(n2s, row)) for row in array) \
        + '\\end{' + type + 'matrix}'

# Generic formulas for layouts
ptwc_formula = lambda O, I, dirs: lambda p: np.array([ p[a]*(a)[a] for a in (I*dirs) ]) / p[O]
point_formula = lambda O, I, dirs: lambda *args: O + I*np.dot(args, dirs)