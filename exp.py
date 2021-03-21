#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from trial_func import *


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)
# A: expand, B: shrink, C: large, D: small
myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152', '2560*1440'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
resolution = ok_data[3]

w, h = resolution.split('*')
w = int(w)
h = int(h)

df = generate()
df_tr = generate()
df['pix_w'] = w
df['pix_h'] = h
a = 3*w / 20.
b = h / 12.
results = {
    'id': [], 'CE': [], 'rt': []
    }


win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0])

# Confirm button
ok = visual.TextStim(win, text=u"确认", pos=(0, -3*h/8), height=h / 36)
ok_shape = visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2)
ok_shape.vertices = [[-0.5 * a, -5 * b], [-0.5 * a, -4 * b], [0.5 * a, -4 * b], [0.5 * a, -5 * b]]
buttons = [ok, ok_shape]
# 时间间隔
t_trial = {'t_fix': 0.5}
# 文本
txt = [visual.TextStim(win, font='MicroSoft Yahei') for i in range(3)]
txt[0].height = 64 * h / 720
txt[0].pos = [-w/5, h / 4]
txt[1].height = 64 * h / 720
txt[1].pos = [-w/16, h / 4-100 * h / 720]
txt[2].height = 48 * h / 720
txt[2].pos = [-w/4,-h/16]
text = visual.TextStim(win, height=64 * h / 720, pos=(-w/4, 0))
# 注视点
fix = visual.ImageStim(win, image="img/fix.png", size=64 * h / 720)
# 指导语
# pic = visual.ImageStim(win, size=(w, h))
# slider
# 指导语
while True:
    #for i in range(2):
        #pic.image = 'img/introduction_%s.png' % (i + 1)
        #pic.draw()
        #win.flip()
        #event.waitKeys(keyList=['space'])
        #event.clearEvents()
    text.text = '按【空格键】 进入决策实验练习'
    text.draw()
    win.flip()
    key = event.waitKeys(keyList=['space', 'escape'])
    if 'space' in key:
        event.clearEvents()
        break
    event.clearEvents()
# training
clk = core.Clock()
myMouse = event.Mouse()
for i in range(8):
    x = df_tr.loc[i, 'x1']
    y = df_tr.loc[i, 'x2']
    slider = visual.Slider(win, pos=(0, -3*h/16), size=(3*w/4, h / 18), granularity=0, style='rating',
                           ticks=list(np.arange(6)*int((x-y)/5)+y), labels = list(np.arange(6)*int((x-y)/5)+y))
    slider.marker.setColor([-1, 200 * 2 / 255 - 1, 1], 'rgb')
    flag = 1
    while flag==1:
        re = trial(i, win, df_tr, clk, slider, buttons, txt, myMouse=myMouse)
        win.flip()
        core.wait(0.2)
        check = gamble_trial(i, win, df, re['CE'])
        if check:
            flag = 0
        else:
            text.text = '与最低金额冲突！请重新选择'
            text.draw()
        win.flip()
        core.wait(0.5)

text.text = '按【空格键】进入正式实验'
text.draw()
win.flip()
key = event.waitKeys(keyList=['space', 'escape'])

clk.reset()
for i in range(len(df)):
    if i in (np.array([1, 2, 3, 4]) * 33 - 1):
        text.text = '休息一下（20s后可按空格键继续）'
        text.draw()
        win.flip()
        core.wait(20)
        key = event.waitKeys(keyList=['space', 'escape'])
    x = df.loc[i, 'x1']
    y = df.loc[i, 'x2']
    slider = visual.Slider(win, pos=(0, -3*h/16), size=(3*w/4, h / 18), granularity=0, style='rating',
                           ticks=list(np.arange(6)*int((x-y)/5)+y), labels = list(np.arange(6)*int((x-y)/5)+y))
    slider.marker.setColor([-1, 200 * 2 / 255 - 1, 1], 'rgb')
    re = trial(i, win, df, clk, slider, buttons, txt, myMouse=myMouse)
    win.flip()
    core.wait(0.5)

text.text = "本试次结束，请呼叫主试"
text.draw()
win.flip()
core.wait(3)
win.close()
core.quit()