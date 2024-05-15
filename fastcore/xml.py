# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/11_xml.ipynb.

# %% auto 0
__all__ = ['xt', 'to_xml', 'Html', 'Head', 'Title', 'Meta', 'Link', 'Style', 'Body', 'Pre', 'Code', 'Div', 'Span', 'P', 'H1',
           'H2', 'H3', 'H4', 'H5', 'H6', 'Strong', 'Em', 'B', 'I', 'U', 'S', 'Strike', 'Sub', 'Sup', 'Hr', 'Br', 'Img',
           'A', 'Nav', 'Ul', 'Ol', 'Li', 'Dl', 'Dt', 'Dd', 'Table', 'Thead', 'Tbody', 'Tfoot', 'Tr', 'Th', 'Td',
           'Caption', 'Col', 'Colgroup', 'Form', 'Input', 'Textarea', 'Button', 'Select', 'Option', 'Label', 'Fieldset',
           'Legend', 'Details', 'Summary', 'Main', 'Header', 'Footer', 'Section', 'Article', 'Aside', 'Figure',
           'Figcaption', 'Mark', 'Small', 'Iframe', 'Object', 'Embed', 'Param', 'Video', 'Audio', 'Source', 'Canvas',
           'Svg', 'Math', 'Script', 'Noscript', 'Template', 'Slot']

# %% ../nbs/11_xml.ipynb 2
from .utils import *

import types
from functools import partial
from html import escape

# %% ../nbs/11_xml.ipynb 4
def _attrmap(o):
    o = dict(htmlClass='class', cls='class', klass='class', fr='for', htmlFor='for').get(o, o)
    return o.lstrip('_').replace('_', '-')

# %% ../nbs/11_xml.ipynb 5
def xt(tag:str, *c, **kw):
    "Create an XML tag structure `[tag,children,attrs]` for `toxml()`"
    if len(c)==1 and isinstance(c[0], types.GeneratorType): c = tuple(c[0])
    kw = {_attrmap(k):str(v) for k,v in kw.items()}
    return [tag.lower(),c,kw]

# %% ../nbs/11_xml.ipynb 6
_g = globals()
_all_ = ['Html', 'Head', 'Title', 'Meta', 'Link', 'Style', 'Body', 'Pre', 'Code',
'Div', 'Span', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Strong', 'Em', 'B',
'I', 'U', 'S', 'Strike', 'Sub', 'Sup', 'Hr', 'Br', 'Img', 'A', 'Link', 'Nav',
'Ul', 'Ol', 'Li', 'Dl', 'Dt', 'Dd', 'Table', 'Thead', 'Tbody', 'Tfoot', 'Tr',
'Th', 'Td', 'Caption', 'Col', 'Colgroup', 'Form', 'Input', 'Textarea',
'Button', 'Select', 'Option', 'Label', 'Fieldset', 'Legend', 'Details',
'Summary', 'Main', 'Header', 'Footer', 'Section', 'Article', 'Aside', 'Figure',
'Figcaption', 'Mark', 'Small', 'Iframe', 'Object', 'Embed', 'Param', 'Video',
'Audio', 'Source', 'Canvas', 'Svg', 'Math', 'Script', 'Noscript', 'Template', 'Slot']

for o in _all_: _g[o] = partial(xt, o.lower())

# %% ../nbs/11_xml.ipynb 9
def to_xml(elm, lvl=0):
    "Convert `xt` element tree into an XML string"
    if isinstance(elm, tuple): return '\n'.join(to_xml(o) for o in elm)
    if hasattr(elm, '__xt__'): elm = elm.__xt__()
    sp = ' ' * lvl
    if not isinstance(elm, list):
        if isinstance(elm, str): elm = escape(elm)
        return f'{elm}\n'

    tag,cs,attrs = elm
    stag = tag
    if attrs:
        sattrs = (f'{k}="{escape(str(v), quote=False)}"' for k,v in attrs.items())
        stag += ' ' + ' '.join(sattrs)
    
    if not cs: return f'{sp}<{stag}></{tag}>\n'
    res = f'{sp}<{stag}>\n'
    res += ''.join(to_xml(c, lvl=lvl+2) for c in cs)
    res += f'{sp}</{tag}>\n'
    return res
