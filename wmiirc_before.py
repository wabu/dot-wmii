import pygmi
from pygmi import fs
from pygmi.fs import *

class TagsExt(fs.Tags):
    def __init__(self, normcol=None, focuscol=None, noticecol=None):
        self.before = self.before_ = None
        super(TagsExt, self).__init__(normcol, focuscol)
        self.noticecol = None

    def focus(self, tag):
	if self.sel and self.sel.id not in self.ignore:
            self.before_ = self.before
            self.before = self.sel
        else:
            self.before = self.before_
        super(TagsExt, self).focus(tag)

    def nth(self, n):
        n -= 1
        tags = [t for t in fs.wmii.tags]
        if n < len(tags):
            return tags[n]
        else:
            return self.sel

    def set_urgent(self, tag, urgent=True):
        if urgent:
            col = self.noticecol or wmii.cache['noticecolors']
            self.tags[tag].button.colors = col

pygmi.Tags = fs.Tags = TagsExt

import wmiirc

class NoticeExt(wmiirc.Notice):
    def show(self, notice, urgent=True):
        super(NoticeExt, self).show(notice)
        self.colors = wmii.cache['noticecolors']

wmiirc.notice = NoticeExt()
