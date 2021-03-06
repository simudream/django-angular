# -*- coding: utf-8 -*-
import os
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers.templates import HtmlDjangoLexer
from pygments.lexers.web import JavascriptLexer
from pygments.formatters import HtmlFormatter

register = template.Library()


@register.simple_tag
def active(request, url):
    if request.path.startswith(reverse(url)):
        return 'active'
    return ''


@register.simple_tag
def pygments(filename):
    fqfn = os.path.abspath(os.path.join(settings.PROJECT_DIR, filename))
    #with file(fqfn) as f: #file() is removed in python 3.4 use open()
    #print("[error] ## failed to add %s" % fqfn)
    theFile = open(fqfn, 'r')
    with theFile as f:
        readlines = f.readlines()
    startfrom = 0
    prevline = True
    content = []
    for lno, line in enumerate(readlines):
        if 'start tutorial' in line:
            startfrom = lno + 1
        if 'end tutorial' in line:
            break
        if bool(line) and not line.isspace():
            content.append(line)
            prevline = True
        else:
            if prevline:
                content.append(line)
            prevline = False
    code = ''.join(content[startfrom:])
    if filename.endswith('.py'):
        lexer = PythonLexer()
    elif filename.endswith('.html'):
        lexer = HtmlDjangoLexer()
    elif filename.endswith('.js'):
        lexer = JavascriptLexer()
    return highlight(code, lexer, HtmlFormatter())
