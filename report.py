# coding:utf-8
#!/usr/bin/env python
from Tkinter import *
import FileDialog
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import index
import copy
import deletelot

font = {'family' : 'serif',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : 11,
        }


class PareTo():
    def __init__(self):
        self.TH = ''
        self.AH = ''
        self.Pr = ''
        self.Mt = ''
        self.bin = list()
        self.sum = 0
        self.osr = 0
        self.tester = ''
        self.pkgt = ''

    def prt(self):
        print 'TestHouse:', self.TH
        print 'AssmeblyHouse:', self.AH
        print 'PRODUCT:', self.Pr
        print 'Mental:', self.Mt
        print 'Bin:', self.bin
        print 'Sum:', self.sum
        print 'OS:', self.osr


class TrdCht():
    def __init__(self):
        self.TH = ''
        self.AH = ''
        self.Pr = ''
        self.Mt = ''
        self.lot = list()
        self.yld = list()
        self.os = list()
        self.osBinNO = 8
        self.elsBinNo = list()
        self.elsBin = list()
        self.els = list()
        self.monthlot = ''
        self.yearlot = ''
        self.drawtype = 0  # 1:draw all;  2:draw year 3:draw 25
        self.total = 0
        self.pas = 0
        self.myld = 0
        self.osr = 0
        self.tester = ''
        self.pkgt = ''

    def prt(self):
        print 'TestHouse:', self.TH
        print 'AssmeblyHouse:', self.AH
        print 'PRODUCT:', self.Pr
        print 'Mental:', self.Mt
        print 'lot:', self.lot
        print 'yld', self.yld
        print 'os', self.os
        print 'osBinNO', self.osBinNO
        print 'elsBinNo', self.elsBinNo
        print 'elsBin', self.elsBin
        print 'els', self.els
        print 'monthlot', self.monthlot
        print 'yearlot', self.yearlot
        print 'drawtype:', self.drawtype
        print 'total:', self.total
        print 'pass:', self.pas
        print 'myld:', self.myld
        print 'osRate:', self.osr
        print 'tester:', self.tester
        print 'pkgt:', self.pkgt


class summry():
    def __init__(self):
        self.prName = list()
        self.qty = list()
        self.yld = list()
        self.title = ''
        self.tester = ''

    def pt(self):
        print 'prName', self.prName
        print 'qty', self.qty
        print 'yld', self.yld
        print 'title', self.title
        print 'tester', self.tester

def GetBinList(_file):
    _binList = list()
    with open(_file, 'rb') as _listfile:
        _r = csv.reader(_listfile)
        for _row in _r:
            if _row[0] != 'Product':
                _binList.append(_row)
    return _binList


def GetPareTo(_file, _binListFile, _thismonth):
    _binList = GetBinList(_binListFile)
    _alPareTo = list()
    with open(_file, 'rb') as _f:
        _reader = csv.reader(_f)
        for _row in _reader:
            if _row[index.TestHouse] != 'TestHouse' and _row[index.TestHouse] and _row[index.Month] == _thismonth:
                _onePareTo = PareTo()
                _onePareTo.TH = _row[index.TestHouse]
                _onePareTo.AH = _row[index.AssmeblyHouse]
                _onePareTo.Pr = _row[index.PRODUCT]
                _onePareTo.Mt = _row[index.mental]
                _done = 0
                for _rbinlist in _binList:
                    if _row[index.PRODUCT] == _rbinlist[0]:
                        _done = 1
                        for _i in xrange(35):
                            _onePareTo.bin.append((_rbinlist[_i + 1], int(_row[index.BIN1 + _i])))
                        _onePareTo.tester = _rbinlist[36]
                        _onePareTo.pkgt = _rbinlist[37]
                if _done == 0:
                    for _i in xrange(35):
                        _onePareTo.bin.append((index.bin_name[_i], int(_row[index.BIN1 + _i])))
                    _onePareTo.tester = 'unknow'
                    _onePareTo.pkgt = 'unknow'
                _alPareTo.append(_onePareTo)
    return _alPareTo


def HeBing(_alPareTo):
    _l = len(_alPareTo)
    # print 'shuliang:', _l
    # print 'before hebing:'
    # for _i in xrange(_l ):
    #     print 'NO.%02d' % (_i + 1)
    #     _alPareTo[_i].prt()
    _d = list()
    for _i in xrange(_l):
        _m = _l - _i - 1
        # print 'm = %02d' % _m,
        for _j in xrange(_m):
            if _alPareTo[_m].TH == _alPareTo[_j].TH \
                    and _alPareTo[_m].AH == _alPareTo[_j].AH \
                    and _alPareTo[_m].Pr == _alPareTo[_j].Pr \
                    and _alPareTo[_j].Mt == _alPareTo[_m].Mt:
                # print 'j = %02d' % _j,
                for _k in xrange(35):
                    _alPareTo[_j].bin[_k] = (_alPareTo[_j].bin[_k][0], _alPareTo[_j].bin[_k][1] + _alPareTo[_m].bin[_k][1])
                _d.append(_m)
                break
        # print ' '
    for _i in _d:
        del _alPareTo[_i]

    for _i in xrange(len(_alPareTo)):
        for _j in xrange(35):
            _alPareTo[_i].sum += _alPareTo[_i].bin[_j][1]
    # print 'after hebing:'
    # print 'shuliang:', len(_alPareTo)
    # for _i in xrange(len(_alPareTo)):
    #     print 'NO.%02d' % (_i + 1)
    #     _alPareTo[_i].prt()

    return _alPareTo


def getdata(_month, _all_pare_to):
    # if month[5] != 1:
    #     shanggeyue = str(int(month) - 1)
    # else:
    #     shanggeyue = str(int(month) - 89)
    qunian = str(int(_month) - 100)
    alTrdCht = list()

    for i in xrange(len(_all_pare_to)):
        oneTrdCht = TrdCht()
        oneTrdCht.TH = _all_pare_to[i].TH
        oneTrdCht.AH = _all_pare_to[i].AH
        oneTrdCht.Pr = _all_pare_to[i].Pr
        oneTrdCht.Mt = _all_pare_to[i].Mt
        oneTrdCht.tester = _all_pare_to[i].tester
        oneTrdCht.pkgt = _all_pare_to[i].pkgt
        # sort by Bin
        lb = _all_pare_to[i].bin
        _all_pare_to[i].bin = sorted(lb, key=lambda lb : lb[1], reverse=True)
        # print alPareTo[i].bin
        for j in xrange(35):
            isos = _all_pare_to[i].bin[j][0][len(_all_pare_to[i].bin[j][0])-3:len(_all_pare_to[i].bin[j][0])]
            if isos == ':OS' or isos == ':os' or isos == 'o\s' or isos == 'O\S' or isos == 'O/S' or isos == 'o/s':
                if _all_pare_to[i].sum:
                    oneTrdCht.osr = float(_all_pare_to[i].bin[j][1]) / _all_pare_to[i].sum
                else:
                    print 'sum=0!'
                    # alPareTo[i].prt()
                tmpBinNo = _all_pare_to[i].bin[j][0][3:5]
                if tmpBinNo[1] == ':':
                    oneTrdCht.osBinNO = int(tmpBinNo[0])
                else:
                    oneTrdCht.osBinNO = int(tmpBinNo)
            if _all_pare_to[i].bin[j][1] > int(_all_pare_to[i].sum * 0.002)\
            and _all_pare_to[i].bin[j][0][3:5] != '1:'\
            and isos != ':OS' and isos != ':os' and isos != 'o\s' and isos != 'O\S' and isos != 'O/S' and isos != 'o/s':
                oneTrdCht.elsBin.append(_all_pare_to[i].bin[j][0])
                tmpBinNo = _all_pare_to[i].bin[j][0][3:5]
                if tmpBinNo[1] == ':':
                    tmpBinNo = int(tmpBinNo[0])
                else:
                    tmpBinNo = int(tmpBinNo)
                oneTrdCht.elsBinNo.append(tmpBinNo)
        # oneTrdCht.prt()
        alTrdCht.append(oneTrdCht)

    for i in xrange(len(alTrdCht)):
        with open('alq.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                s = 0
                if row[0] != 'TestHouse'\
                and alTrdCht[i].TH == row[index.TestHouse] \
                and alTrdCht[i].AH == row[index.AssmeblyHouse]\
                and alTrdCht[i].Pr == row[index.PRODUCT]\
                and alTrdCht[i].Mt[0] == row[index.mental][0]:
                    for x in row[index.BIN1:index.BIN35]:
                        s += int(x)
                    alTrdCht[i].lot.append(row[index.LotNo])
                    alTrdCht[i].yld.append(row[index.Yield])
                    alTrdCht[i].os.append(float(row[index.BIN1 + alTrdCht[i].osBinNO - 1]) / s)
                    # print row[index.LotNo], 'is', row[index.PRODUCT]
                    for elsbin in alTrdCht[i].elsBinNo:
                        alTrdCht[i].els.append(float(row[index.BIN1 + elsbin - 1]) / s)
                    if alTrdCht[i].yearlot == '' and row[index.Month] == qunian:
                        alTrdCht[i].yearlot = row[index.LotNo]
                    if alTrdCht[i].monthlot == '' and row[index.Month] == _month:
                        alTrdCht[i].monthlot = row[index.LotNo]
        if not alTrdCht[i].yearlot:
            alTrdCht[i].drawtype = 1
        else:
            t25 = 0
            for lt in alTrdCht[i].lot:
                if lt == alTrdCht[i].yearlot and len(alTrdCht[i].lot) - t25 > 24:
                    alTrdCht[i].drawtype = 2
                    while alTrdCht[i].lot[0] != alTrdCht[i].yearlot:
                        alTrdCht[i].lot.pop(0)
                        alTrdCht[i].yld.pop(0)
                        alTrdCht[i].os.pop(0)
                        for ei in xrange(len(alTrdCht[i].elsBinNo)):
                            alTrdCht[i].els.pop(ei)
                    break
                t25 += 1
            if len(alTrdCht[i].lot) == t25:
                alTrdCht[i].drawtype = 3
                while len(alTrdCht[i].lot) > 25:
                    alTrdCht[i].lot.pop(0)
                    alTrdCht[i].yld.pop(0)
                    alTrdCht[i].os.pop(0)
                    for ei in xrange(len(alTrdCht[i].elsBinNo)):
                        alTrdCht[i].els.pop(ei)
    return alTrdCht

def getm(data, month):
    for dt in data:
        with open('./%s/VendorLot.csv' % month) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[index.n_Assembly] == dt.AH and row[index.n_TestHouse] == dt.TH and row[index.n_Product] == dt.Pr and row[index.n_WireType] == dt.Mt:
                    dt.total += int(row[index.n_Total])
                    dt.pas += int(row[index.n_Pass])
            if dt.total:
                dt.myld = float(dt.pas) / dt.total
    return data

def getsmry(_month, _smry):
    _alsmry = list()
    for _tster in _smry:
        _onesmry = summry()
        _onesmry.title = '%s %s/%s yield summary' % (_tster, _month[:4], _month[-2:])
        _onesmry.prName = map(lambda x:x[index.s_Name], _smry[_tster])
        _onesmry.yld = map(lambda x:x[index.s_Yield], _smry[_tster])
        _onesmry.qty = map(lambda x:x[index.s_Qty], _smry[_tster])
        _onesmry.tester = _tster
        _alsmry.append(_onesmry)
    return _alsmry


def drawsmry(_month, _smry):
    for _onesmry in _smry:
        j = len(_onesmry.prName)
        if j < 15:
            fs = 10
        elif j < 20:
            fs = 9
        elif j < 25:
            fs = 8
        else:
            fs = 7

        fig = plt.figure(figsize=(10, 6))
        fig.patch.set_alpha(0.)
        plt.axes([0.15, 0.2, 0.7, 0.6])

        xs = np.arange(len(_onesmry.prName)) + 0.5

        rects = plt.bar(np.arange(len(_onesmry.qty)) + 0.1, _onesmry.qty, color='#66CCFF')
        plt.ylabel('Quantity(kea)')
        plt.axis([0, len(_onesmry.yld), 0, 1000])
        plt.title(_onesmry.title, fontsize=11)
        m = max(_onesmry.qty)
        for rect in rects:
            h = rect.get_height()
            if h > 1000:
                h = 1000
            plt.text(rect.get_x() + rect.get_width()*0.5, h + m*0.01, '%2.1f' % (float(rect.get_height())),  fontsize=fs, ha='center', va='bottom')
        plt.xticks(xs, _onesmry.prName, rotation=20, ha='right', va='top', fontsize=fs)
        plt.twinx()

        plt.plot(xs, _onesmry.yld, color='k')
        plt.ylabel('Yield(%)')
        m = int(min(_onesmry.yld) * 5 - 400)/5*5
        if m < 0:
            m = 0
        plt.axis([0, len(_onesmry.yld), m, 100])
        for i, j in zip(xs, _onesmry.yld):
            plt.annotate('%2.2f' % j, xy=(i, j-(100-m)/20.), color='k', fontsize=fs, ha='center', va='bottom')

        # plt.show()
        plt.savefig('./%s/%s/summary.png' % (_month, _onesmry.tester))
        print 'file summary.png saved in ./%s/%s/' % (_month, _onesmry.tester)

def pt_main(month):
    if not os.path.exists('./'+month+'/VendorLot.csv'):
        raw_input("Can't find ./%s/VendorLot.csv, press Enter to Exit" % month)
        exit()
    all_pare_to = GetPareTo('alq.csv', 'binList.csv', month)
    # all_pare_to = all_pare_to[:10]
    all_pare_to = HeBing(all_pare_to)
    all_pare_to_cpy = copy.deepcopy(all_pare_to)
    # sort by Bin
    for i in xrange(len(all_pare_to)):
        lb = all_pare_to[i].bin
        all_pare_to[i].bin = sorted(lb, key=lambda lb: lb[1], reverse=True)

    for i in xrange(len(all_pare_to)):
        # # bin name tai chang, jia \n
        # for bi in xrange(35):
        #     if len(alPareTo[i].bin[bi]) > 18:
        #         alPareTo[i].bin[bi] = alPareTo[i].bin[bi][0:15] + '\n' + alPareTo[i].bin[bi][14:len(alPareTo[i].bin[bi])]
        val = list()
        print 'NO.%03d' % i
        # alPareTo[i].prt()
        for j in xrange(35):
            if all_pare_to[i].bin[j][1] == 0:
                break
            val.append(all_pare_to[i].bin[j][1])
        fei0 = len(val)
        fig = plt.figure(figsize=(10, 6))
        fig.patch.set_alpha(0.)
        plt.axes([0.1, 0.2, 0.8, 0.6])
        rects = plt.bar(np.arange(fei0), val)
        plt.ylabel('Quantity')
        plt.title('%s(%s)\n Teszt:%s   Assmebly:%s   Month:%s\n Quantity(Lot):%d' % (all_pare_to[i].Pr, all_pare_to[i].Mt, all_pare_to[i].TH, all_pare_to[i].AH, month, all_pare_to[i].sum), fontsize=11)
        for j in xrange(35):
            if all_pare_to[i].bin[j][1] == 0:
                break
        if j < 15:
            font['size'] = 10
        elif j < 20:
            font['size'] = 9
        elif j < 25:
            font['size'] = 8
        else:
            font['size'] = 7
        # print 'j=', j
        # print 'size=', font['size']
        b = list()
        for k in xrange(j):
            b.append(all_pare_to[i].bin[k][0])
        plt.xticks(np.arange(j)+0.4, b, rotation=20, ha='right', va='top', fontsize=font['size'] - 1)
        for rect in rects:
            h = rect.get_height()
            if h > 0:
                plt.text(rect.get_x() + rect.get_width() * 0.01, h+all_pare_to[i].sum*0.01, '%2.1f' % (float(h)/all_pare_to[i].sum * 100), fontdict=font)
        # plt.show()
        st = ''
        for c in all_pare_to[i].AH:
            if c == '|':
                c = 'or'
            st += c
        all_pare_to[i].AH = st
        filename = '%s_%s_%s_%s_%s_PareTo.png' % (all_pare_to[i].Pr, all_pare_to[i].AH, all_pare_to[i].TH, all_pare_to[i].Mt, month)
        if not os.path.exists('./%s/%s/' % (month, all_pare_to[i].tester)):
            os.mkdir('./%s/%s/' % (month, all_pare_to[i].tester))
        plt.savefig('./%s/%s/' % (month, all_pare_to[i].tester) + filename)
        print 'file %s saved in ./%s/%s/\n' % (filename, month, all_pare_to[i].tester)
        plt.close()
    # smry = ['Product', 'pkgType', 'AH', 'TH', 'Mental', 'Qty', 'Yield', 'OS', 'tester', 'Name', '\n']
    smry = dict()
    data = getdata(month, all_pare_to_cpy)
    data = getm(data, month)
    clr = ['g', 'b', 'm', 'y', 'c', '#66CCFF', '#D09A67', '#98729B', '#200454', 'k']
    no = 0
    for dt in data:  # [:5]:
        # if dt.total:
        print 'NO.%03d' % no
        no += 1
        tar = np.array([])
        for i in xrange(len(dt.lot)):
            tar = np.append(tar, 99.5)
        # dt.prt()
        print 'lot:', len(dt.lot)
        if len(dt.lot) > 30:
            fz = 6
        elif len(dt.lot) > 25:
            fz = 7
        elif len(dt.lot) > 20:
            fz = 8
        elif len(dt.lot) > 15:
            fz = 9
        elif len(dt.lot) > 10:
            fz = 10
        else:
            fz = 11
        if dt.elsBin:
            npelsb = np.array([])
            for b in dt.els:
                npelsb = np.append(npelsb, b * 100)
            npelsb.shape = (len(npelsb)/len(dt.elsBin), len(dt.elsBin))
            lstelsb = list()
            for i in xrange(len(dt.elsBin)):
                lstelsb.append(npelsb[:, i])
        fig = plt.figure(figsize=(10, 6))
        fig.patch.set_alpha(0.)
        npyld = np.array([])
        npos = np.array([])
        x = np.arange(len(dt.lot))
        for i in xrange(len(dt.yld)):
            npyld = np.append(npyld, float(dt.yld[i]))
            npos = np.append(npos, float(dt.os[i]) * 100)
        plt.axes([0.1, 0.18, 0.8, 0.64])
        plt.ylabel('Yield(%)')
        plt.title('%s(%s)\n Test:%s   Assmebly:%s   Month:%s \nQuantity(Vdr.Lot):%d   Yield:%s' % (dt.Pr, dt.Mt, dt.TH, dt.AH, month, dt.total, str(dt.myld*100)[:6]) + '%  ' + 'OS:%s' % str(dt.osr*100)[:5] + '%', fontsize=11)
        tmp = list()
        tmp.append(dt.Pr)
        tmp.append(dt.pkgt)
        tmp.append(dt.AH)
        tmp.append(dt.TH)
        tmp.append(dt.Mt)
        tmp.append(float('%.3f' % (dt.total/1000.0)))
        tmp.append(float('%2.2f' % (dt.myld*100)))
        tmp.append(float('%2.2f' % (dt.osr*100)))
        tmp.append(dt.tester)
        tmp.append('%s' % dt.Pr+'_'+dt.AH+'_'+dt.TH+'_'+dt.Mt)
        tmp.append('\n')
        if dt.tester in smry:
            smry[dt.tester].append(tmp)
        else:
            smry[dt.tester] = [tmp]
        plt.xticks(np.arange(len(dt.lot)), dt.lot, rotation=23, ha='right', va='top', fontsize=fz)
        if min(npyld) > 98:
            mi = 90
        elif min(npyld) > 90:
            mi = min(npyld) * 5 - 400
        elif min(npyld) > 50:
            mi = min(npyld) * 2 - 100
        else:
            mi = 0
        plt.axis([0, len(dt.lot) - 1, mi, 100])
        plt.plot(npyld, linewidth=1.5, color='k', label='Yield')
        if len(dt.yld) < 35:
            for i, j in zip(x, npyld):
                if i-len(dt.yld)/60.0 > 0:
                    plt.annotate('%2.2f' % j, xy=(i-len(dt.yld)/60.0, j-(100-mi)/30.), fontsize=fz, color='k')
                else:
                    plt.annotate('%2.2f' % j, xy=(i, j-0.4), fontsize=fz, color='k')
        plt.plot(tar, '--', linewidth=0.5, color='r')
        plt.legend(bbox_to_anchor=(0., 1., 1., 0.), borderaxespad=0., loc=3, fontsize=9)
        plt.twinx()
        plt.ylabel('Bin(%)')
        plt.plot(npos, linewidth=1, color='r', label='OS')
        plt.legend(bbox_to_anchor=(1., 1.), borderaxespad=0., loc=4, fontsize=9)
        if dt.elsBin:
            mx = max(np.max(npos), np.max(npelsb))
        else:
            mx = np.max(npos)
        if mx > 2:
            mx *= 1.5
        else:
            mx = 3
        plt.axis([0, len(dt.lot) - 1, 0, mx])
        if len(dt.yld) < 35:
            for i, j in zip(x, npos):
                if i-len(dt.yld)/60.0 > 0:
                    plt.annotate('%1.3f' % j, xy=(i-len(dt.yld)/60.0, j), fontsize=fz-1, color='r')
                else:
                    plt.annotate('%1.3f' % j, xy=(i, j), fontsize=fz-1, color='r')
        if dt.elsBin:
            plt.axis([0, len(dt.lot) - 1, 0, mx], 'off')
            ci = 0
            for elb in lstelsb:
                cj = ci % 5
                plt.plot(elb, linewidth=1, color=clr[cj], label=dt.elsBin[ci])
                if len(dt.yld) < 30:
                    for i, j in zip(x, elb):
                        if i-len(dt.yld)/60.0 > 0:
                            plt.annotate('%1.3f' % j, xy=(i-len(dt.yld)/60.0, j), fontsize=fz-1, color=clr[ci])
                        else:
                            plt.annotate('%1.3f' % j, xy=(i, j), fontsize=fz-1, color=clr[ci])
                if ci == 5:
                    lgdfz = 6
                elif ci > 5:
                    lgdfz = 4
                else:
                    lgdfz = 8
                plt.legend(bbox_to_anchor=(1., 1.), borderaxespad=0., loc=4, fontsize=lgdfz)
                ci += 1
        monx = 0
        if dt.monthlot:
            for lti in xrange(len(dt.lot)):
                if dt.lot[lti] == dt.monthlot:
                    monx = lti
        if monx:
            plt.axvline(x=monx - 0.5, ymin=0, ymax=1, hold=None, color='g', linewidth=2)
        else:
            plt.axvline(x=0, ymin=0, ymax=1, hold=None, color='g', linewidth=2)
        plt.grid()
        # plt.show()
        st = ''
        for c in dt.AH:
            if c == '|':
                c = 'or'
            st += c
        dt.AH = st
        filename = '%s_%s_%s_%s_%s_TrendChart.png' % (dt.Pr, dt.AH, dt.TH, dt.Mt, month)
        if not os.path.exists('./%s/%s/' % (month, dt.tester)):
            os.mkdir('./%s/%s/' % (month, dt.tester))
        plt.savefig('./%s/%s/' % (month, dt.tester) + filename)
        print 'file %s saved in ./%s/%s/\n' % (filename, month, dt.tester)
        plt.close()
    print '\n'
    for tster in smry:
        st = smry[tster]
        smry[tster] = sorted(st, key=lambda st:st[index.s_Qty], reverse=True)
    alsmry = getsmry(month, smry)
    drawsmry(month, alsmry)

    with open('./%s/summary.csv' % month, 'w') as f:
        pr = ['Product', 'pkgType', 'AH', 'TH', 'Mental', 'Qty', 'Yield', 'OS', 'tester', 'Name', '\n']
        for x in pr:
            f.write(str(x))
            if x != '\n':
                f.write(',')
        for tster in smry:
            for pr in smry[tster]:
                for x in pr:
                    f.write(str(x))
                    if x != '\n':
                        f.write(',')


    print 'file summary.csv saved in ./%s' % month


    print 'Done!\nPress Enter to exit...'
    raw_input()



if __name__ == '__main__':
    if not os.path.exists('./alq.csv'):
        raw_input("Can't find alq.csv, press Enter to Exit")
        exit()
    if not os.path.exists('./binList.csv'):
        raw_input("Can't find binList.csv, press Enter to Exit")
        exit()
    month = raw_input("input month... \ne.g., 201408\n")
    deletelot.main()
    pt_main(month)