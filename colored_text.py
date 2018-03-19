# -*- coding: utf-8 -*-
"""
Colored text tool for RNN visualization
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


class ColoredText(object):
    """
    text: a sequence of characters
    vals: a float vector, (-1 , 1), The same length as text
    width: image width
    fontsize:
    fontname: nonproportional fontname
    disp_colorbar:

    TODO:Fix margins.The margins are correct only for width=1080 and fontsize=14.
    """
    def __init__(self, text, vals, width, fontsize,
                 fontname='Source Code Pro',
                 disp_colorbar=True):
        assert len(text) == len(vals)
        self.text = text
        self.vals = (vals + 1) / 2  # (-1,1) to (0, 1)
        self.figsize_x = width / 90
        self.fontsize = fontsize
        self.fontname = fontname
        self.disp_colorbar = disp_colorbar
        #
        self.font_w = fontsize
        self.font_h = 1.9 * self.font_w
        self.text_w = 0.95 * width
        self.cnt_oneline = int(self.text_w / self.font_w) - 1
        self.text_h = np.ceil(len(text) / self.cnt_oneline) * self.font_h

        if self.disp_colorbar:
            self.text_h += .7 * self.font_h
            self.height = self.text_h + 50
            self.text_bottom = 20 / self.height
        else:
            self.height = self.text_h + 30
            self.text_bottom = 0

        self.text_rh = self.text_h / self.height
        self.figsize_y = self.height / 90
        self.suptitle_y = 1 - 10 / self.height

        self.font_rw = self.font_w / self.text_w
        self.font_rh = self.font_h / self.text_h
        self.text_val = self.split(self.cnt_oneline)

    def split(self, cnt):
        text_val = [(self.text[i:i+cnt], self.vals[i:i+cnt])
                    for i in range(0, len(self.text), cnt)]
        return text_val

    def disp_one_line(self, ax, subtext, subvals, height):
        cl_s = cm.bwr(subvals)
        for i, (ch, cl) in enumerate(zip(subtext, cl_s)):
            ax.text(0.01 + i * self.font_rw, height, ch,
                    fontname=self.fontname,
                    fontsize=self.fontsize,
                    bbox={'facecolor': cl, 'edgecolor': cl,
                          'alpha': 0.8, 'pad': 1})
        return ax

    def display(self, title=None, savefile=None):
        fig = plt.figure(figsize=(self.figsize_x, self.figsize_y), dpi=90)
        if title is not None:
            fig.suptitle(title, y=self.suptitle_y, fontsize=self.fontsize + 2)

        # colored text
        ax = fig.add_axes([0.02, self.text_bottom, 0.97, self.text_rh])
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for j, (subtext, subvals) in enumerate(self.text_val):
            self.disp_one_line(ax, subtext, subvals,
                               1 - (j+0.6)*self.font_rh)
        if self.disp_colorbar:
            cax = fig.add_axes([0.02, self.text_bottom, 0.97, self.text_bottom])
            gradient = np.linspace(0, 1, 101)
            gradient = np.vstack((gradient, gradient))
            cax.imshow(gradient, aspect='auto', cmap=plt.get_cmap('bwr'))
            cax.set_xticks([0, 25, 50, 75, 100])
            cax.set_xticklabels(map(str, (cax.get_xticks() - 50) / 50))
            cax.get_yaxis().set_visible(False)

        if savefile is None:
            plt.show()
        else:
            plt.savefig(savefile)
        plt.close()


if __name__ == '__main__':
    from itertools import product
    SAVE = True
    savefile = None
    paramsgrid = product([10, 113, 375, 819],  # num of chars
                         [540, 1080],          # image width
                         [10, 14, 18],         # fontsize
                         [True, False])        # disp_colorbar

    for n, width, fontsize, disp_colorbar in paramsgrid:
        text = ''.join([str(i % 10) for i in range(n)])
        vals = (np.random.randn(n) / 5).clip(-1, 1)
        title = 'n:{:d} width:{:d} fontsize:{:d} cbar:{:d}'.format(
                   n, width, fontsize, disp_colorbar)
        if SAVE:
            savefile = 'img/' + title.replace(':', '').replace(' ', '_')
        ct = ColoredText(text, vals, width, fontsize,
                         disp_colorbar=disp_colorbar)
        ct.display(title=title, savefile=savefile)
