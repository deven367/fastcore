# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_docments.ipynb (unless otherwise specified).

__all__ = ['docments']

# Cell
from tokenize import tokenize,COMMENT
from ast import parse,FunctionDef
from io import BytesIO
from textwrap import dedent
from types import SimpleNamespace
from inspect import getsource,isfunction,isclass,signature,Parameter
from .basics import *

import re

# Cell
def _parses(s):
    "Parse Python code in string or function object `s`"
    return parse(dedent(getsource(s) if isfunction(s) else s))

def _tokens(s):
    "Tokenize Python code in string or function object `s`"
    if isfunction(s): s = getsource(s)
    return tokenize(BytesIO(s.encode('utf-8')).readline)

_clean_re = re.compile('^\s*#(.*)\s*$')
def _clean_comment(s):
    res = _clean_re.findall(s)
    return res[0] if res else None

def _param_locs(s, returns=True):
    "`dict` of parameter line numbers to names"
    body = _parses(s).body
    if len(body)!=1or not isinstance(body[0], FunctionDef): return None
    defn = body[0]
    res = {arg.lineno:arg.arg for arg in defn.args.args}
    if returns and defn.returns: res[defn.returns.lineno] = 'return'
    return res

# Cell
def _get_comment(line, arg, comments, parms):
    if line in comments: return comments[line].strip()
    line -= 1
    res = []
    while line and line in comments and line not in parms:
        res.append(comments[line])
        line -= 1
    return dedent('\n'.join(reversed(res))) if res else None

def _get_full(anno, name, default, docs):
    if anno==Parameter.empty and default!=Parameter.empty: anno = type(default)
    return AttrDict(docment=docs.get(name), anno=anno, default=default)

# Cell
def docments(s, full=False, returns=True):
    "`dict` of parameter names to 'docment-style' comments in function or string `s`"
    if isclass(s): s = s.__init__ # Constructor for a class
    comments = {o.start[0]:_clean_comment(o.string) for o in _tokens(s) if o.type==COMMENT}
    parms = _param_locs(s, returns=returns)
    docs = {arg:_get_comment(line, arg, comments, parms) for line,arg in parms.items()}
    if not full: return docs

    if isinstance(s,str): s = eval(s)
    sig = signature(s)
    res = {arg:_get_full(p.annotation, p.name, p.default, docs) for arg,p in sig.parameters.items()}
    if returns: res['return'] = _get_full(sig.return_annotation, 'return', Parameter.empty, docs)
    return res