#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import numpy as np

def trial(i, win, df, clk, slider, buttons, txt, myMouse=None):
    """
    Run a trial of given data
    Returns the values recorded

    Parameters
    ----------
    i : int
        trial number
    win : visual.Window
        windows created by psychopy
    df : pd.DataFrame
        Exp data contains gambles and conditions
    clk : core.Clock
        clock to record time
    slider:
        slider bar
    buttons: list
        list contains elements for buttons, [visual.TextStim, visual.ShapeStim]
    txt: list
        text stim, [visual.TextStim, visual.TextStim, visual.TextStim]
    myMouse: event.Mouse
        mouse object

    Returns
    -------
    result : list
    """
    if myMouse is None:
        myMouse = event.Mouse()
    p = df.loc[i, 'p']
    x = df.loc[i, 'x1']
    y = df.loc[i, 'x2']

    result = {
    }
    # w, h = win.size
    txt[0].text = "%s%%，%s元；%s%%，%s元" % (int(100 * p), int(x), 100-int(100 * p), int(y))
    #txt[0].text = "%s%%，%s元" % (int(100 * p), int(x))
    txt[1].text = "%s%%，%s元" % (100-int(100 * p), int(y))
    # txt[0].pos = (-len(txt[0].text)*64*h/720, h/4)
    # txt[1].pos = (-len(txt[1].text)*64*h/720, h/4-10*h/72)
    state = 'running'
    x1 = x
    y1 = y

    event.clearEvents()
    clk.reset()
    txt[2].text = u'你最低愿意换取多少元？'
    while True:
        if state == 'running':
            txt[0].draw()
            #txt[1].draw()
            txt[2].draw()
            slider.draw()
            win.flip()
            if slider.getRating() is not None:
                state = 'rating'
            key = event.getKeys(["escape"])
            if "escape" in key:
                state = "exit"
        elif state == 'rating':
            txt[0].draw()
            #txt[1].draw()
            slider.draw()
            buttons[1].draw()
            buttons[0].draw()
            ce = slider.getRating()
            t_p = slider.getRT()
            txt[2].text = u'你最低愿意换取:%s元' % np.round(ce, 1)
            txt[2].draw()
            if buttons[1].contains(myMouse):
                buttons[1].fillColor = [-1, -1, -1]
                buttons[1].opacity = 0.3
            else:
                buttons[1].fillColor = [0, 0, 0]
                buttons[1].opacity = 1
            win.flip()
            if myMouse.isPressedIn(buttons[1]):
                rt = clk.getTime()
                result['CE'] = ce
                result['rt'] = rt
                state = 'quit'
        elif state == "quit":
            win.flip()
            state = "running"
            break
        elif state == "exit":
            win.flip()
            win.close()
            core.quit()

    return result


def gamble_trial(i, win, df, ce):
    """
    Run a trial of given data
    Returns the values recorded

    Parameters
    ----------
    i : int
        trial number
    win : visual.Window
        windows created by psychopy
    df : pd.DataFrame
        Exp data contains gambles and conditions
    ce: int
        CE

    Returns
    -------
    result : list
    """
    p = df.loc[i, 'p']
    x = df.loc[i, 'x1']
    y = df.loc[i, 'x2']
    w, h = win.size
    result = {
    }
    txt = visual.TextStim(win, height=48 * h / 720, font='MicroSoft Yahei')
    loc = [-1,1]
    np.random.shuffle(loc)
    txt.text = "%s%%，%s元 %s%%，%s元" % (int(100 * p), int(x), 100-int(100 * p), int(y))
    txt.pos = (loc[0]*w/4, 0)
    txt.draw()
    txt.text = "%s元" % np.clip(int(ce)-1, 0, 1e4)
    txt.pos = (loc[1]*w/4, 0)
    txt.draw()
    win.flip()
    key = event.waitKeys(keyList=['f', 'j'])
    if 'f' in key:
        return loc[0] == -1
    elif 'j' in key:
        return loc[0] == 1
