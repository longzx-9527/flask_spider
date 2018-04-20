# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-20 11:01:06
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from markdown.extensions import Extension
from markdown.util import etree
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor


##预处理器
class CodePreprocessor(Preprocessor):
    def run(self, lines):
        # return lines
        new_lines = []
        flag_in = False
        for line in lines:
            if line[:3] == '```':
                line = line.lstrip('```')
                if flag_in:
                    flag_in = False
                else:
                    flag_in = True

            if flag_in:
                line = '     ' + line

            new_lines.append(line)
        return new_lines


##后置处理器
class CodePostprocessor(Postprocessor):
    def run(self, text):
        return text
        # t_list = []
        # codeIn = False
        # for line in text.split('\n'):
        #     t_list.append(line)
        # return '\n'.join(t_list)


##扩展主体类


class CodeExtension(Extension):
    def __init__(self, configs={}):
        self.config = configs

    def extendMarkdown(self, md, md_globals):
        ##注册扩展，用于markdown.reset时扩展同时reset
        md.registerExtension(self)

        ##设置Preprocessor
        codepreprocessor = CodePreprocessor()
        #print md.preprocessors.keys()
        md.preprocessors.add('codepreprocessor', codepreprocessor,
                             '<normalize_whitespace')

        ##设置Postprocessor
        codepostprocessor = CodePostprocessor()
        #print md.postprocessors.keys()
        md.postprocessors.add('codepostprocessor', codepostprocessor,
                              '>unescape')
