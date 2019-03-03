# coding=utf-8

from verb import Verb

import re

class Router(object):
    """
    路由封装
    支持`/a/b/<:id|int>` 这种形式
    """
    def __init__(self, group ="", url="", methods=None):
        self.group = group
        self.url = url
        if not methods:
            methods = [Verb.GET]
        if type(methods) is not list:
            methods = [methods]
        methods.sort()
        self.methods = methods
        self.complete_url = ("/" if self.group else "") + self.group + self.url
    
    @property
    def has_variable(self):
        return re.search(r"<:.*>", self.complete_url) is not None
    
    def __repr__(self):
        return "{}-{}".format(self.complete_url, self.methods)

    @property
    def router(self):
        return repr(self)

    def __hash__(self):
        return hash(self.router)
    
    def __eq__(self, other):
        """
        所谓的相等，是指能否在对方找到匹配条件, 先比较url, 再比较mthod
        """
        if self.has_variable or other.has_variable:
            url_splits = self.complete_url.split("/")
            other_splits = other.complete_url.split("/")
            if len(url_splits) != len(other_splits):
                return False
            for index in xrange(len(url_splits)):
                if re.match(r"<:.*>", url_splits[index]):
                    continue
                else:
                    if url_splits[index] == other_splits[index]:
                        continue
                    else:
                        if re.match(r"<:.*>", other_splits[index]):
                            continue
                        else:
                            return False
            else:
                # url匹配, 再比较method
                if set(self.methods).intersection(set(other.methods)):
                    return True
                else:
                    return False
        # 不存在变量
        if self.router == other.router:
            return True
        if self.complete_url == other.complete_url:
            if set(self.methods).intersection(set(other.methods)):
                return True
            return False   