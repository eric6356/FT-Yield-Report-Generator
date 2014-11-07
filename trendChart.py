# coding:utf-8
"""
绘制trendChart
需要先调用pareTo得到pareTo图的数据

原则1：
当一年内的批次数量超过25时，画一整年的所有Lot；
不足25时候向前追溯满25批；
若有史以来所有批次数量总和都不足25，则全部画出。

原则2：
OS Bin一定要画，其他Fail Bin超过0.2%的也要画。

原则3：
尽量标出数值，Lot太多看不清了就不标
"""

import csv
import index
import pareTo
import deletelot
import matplotlib.pyplot as plt
import numpy as np
import os


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


def getdata(_month, _all_pare_to, _filename):
    """
    获取trendChart的数据
    :param _month: 月份
    :param _all_pare_to:所有的pareTo数据，注意测试厂名不能改过。
    :param _filename:alq.csv
    :return: 所有trendChart数据组成的List
    """
    print 'Getting trendChart data from alq.scv...'
    # if month[5] != 1:
    # shanggeyue = str(int(month) - 1)
    # else:
    # shanggeyue = str(int(month) - 89)
    qunian = str(int(_month) - 100)
    _alTrdCht = list()

    for i in xrange(len(_all_pare_to)):
        _oneTrdCht = TrdCht()
        _oneTrdCht.TH = _all_pare_to[i].TH
        _oneTrdCht.AH = _all_pare_to[i].AH
        _oneTrdCht.Pr = _all_pare_to[i].Pr
        _oneTrdCht.Mt = _all_pare_to[i].Mt
        _oneTrdCht.tester = _all_pare_to[i].tester
        _oneTrdCht.pkgt = _all_pare_to[i].pkgt
        # sort by Bin
        lb = _all_pare_to[i].bin
        _all_pare_to[i].bin = sorted(lb, key=lambda _x: _x[1], reverse=True)
        # print alPareTo[i].bin
        for j in xrange(35):
            # 找到OS Bin，算出OS率，记下OS Bin号
            isos = _all_pare_to[i].bin[j][0][len(_all_pare_to[i].bin[j][0]) - 3:len(_all_pare_to[i].bin[j][0])]
            if isos == ':OS' or isos == ':os' or isos == 'o\s' or isos == 'O\S' or isos == 'O/S' or isos == 'o/s':
                # 算OS率
                if _all_pare_to[i].sum:
                    _oneTrdCht.osr = float(_all_pare_to[i].bin[j][1]) / _all_pare_to[i].sum
                else:
                    _all_pare_to[i].prt()
                    raw_input('sum=0!')
                # 记OS Bin号
                _tmpBinNo = _all_pare_to[i].bin[j][0][3:5]
                if _tmpBinNo[1] == ':':
                    _oneTrdCht.osBinNO = int(_tmpBinNo[0])
                else:
                    _oneTrdCht.osBinNO = int(_tmpBinNo)
            # 找到超过0.2%的非OS Bin
            if _all_pare_to[i].bin[j][1] > int(_all_pare_to[i].sum * 0.002) \
                    and _all_pare_to[i].bin[j][0][3:5] != '1:' \
                    and isos != ':OS' and isos != ':os' and isos != 'o\s' \
                    and isos != 'O\S' and isos != 'O/S' and isos != 'o/s':
                _oneTrdCht.elsBin.append(_all_pare_to[i].bin[j][0])
                _tmpBinNo = _all_pare_to[i].bin[j][0][3:5]
                if _tmpBinNo[1] == ':':
                    _tmpBinNo = int(_tmpBinNo[0])
                else:
                    _tmpBinNo = int(_tmpBinNo)
                _oneTrdCht.elsBinNo.append(_tmpBinNo)
        # _oneTrdCht.prt()
        _alTrdCht.append(_oneTrdCht)

    # 按照原则1，判断每个trendChart该怎么画
    for i in xrange(len(_alTrdCht)):
        with open(_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                s = 0
                if row[0] != 'TestHouse' \
                        and _alTrdCht[i].TH == row[index.TestHouse] \
                        and _alTrdCht[i].AH == row[index.AssmeblyHouse] \
                        and _alTrdCht[i].Pr == row[index.PRODUCT] \
                        and _alTrdCht[i].Mt[0] == row[index.mental][0]:
                    for x in row[index.BIN1:index.BIN35]:
                        s += int(x)
                    _alTrdCht[i].lot.append(row[index.LotNo])
                    _alTrdCht[i].yld.append(row[index.Yield])
                    _alTrdCht[i].os.append(float(row[index.BIN1 + _alTrdCht[i].osBinNO - 1]) / s)
                    # print row[index.LotNo], 'is', row[index.PRODUCT]
                    for elsbin in _alTrdCht[i].elsBinNo:
                        _alTrdCht[i].els.append(float(row[index.BIN1 + elsbin - 1]) / s)
                    if _alTrdCht[i].yearlot == '' and row[index.Month] == qunian:
                        _alTrdCht[i].yearlot = row[index.LotNo]
                    # monthlot是画绿竖线用的
                    if _alTrdCht[i].monthlot == '' and row[index.Month] == _month:
                        _alTrdCht[i].monthlot = row[index.LotNo]
        # yearlot没有，画全部
        if not _alTrdCht[i].yearlot:
            _alTrdCht[i].drawtype = 1
        # 下面一段比较复杂，2个月前写的，现在看不懂，反正是原则1来的
        else:
            t25 = 0
            for lt in _alTrdCht[i].lot:
                if lt == _alTrdCht[i].yearlot and len(_alTrdCht[i].lot) - t25 > 24:
                    _alTrdCht[i].drawtype = 2
                    while _alTrdCht[i].lot[0] != _alTrdCht[i].yearlot:
                        _alTrdCht[i].lot.pop(0)
                        _alTrdCht[i].yld.pop(0)
                        _alTrdCht[i].os.pop(0)
                        for ei in xrange(len(_alTrdCht[i].elsBinNo)):
                            _alTrdCht[i].els.pop(ei)
                    break
                t25 += 1
            if len(_alTrdCht[i].lot) == t25:
                _alTrdCht[i].drawtype = 3
                while len(_alTrdCht[i].lot) > 25:
                    _alTrdCht[i].lot.pop(0)
                    _alTrdCht[i].yld.pop(0)
                    _alTrdCht[i].os.pop(0)
                    for ei in xrange(len(_alTrdCht[i].elsBinNo)):
                        _alTrdCht[i].els.pop(ei)
    print 'Done!\n'
    # 返回按原则1选好的数据。
    return _alTrdCht


def getm(_data, _month):
    """
    根据VendorLot.csv，给本月所有的TrendChart数据加上总数和良率，画图和生成Summary都要用到
    :param _data: 所有的TrendChart组成的List，也就是getdata的返回值
    :param _month: 本月份
    :return: 加好数据之后的所有TrendChart
    """
    print 'Getting month data from VendorLot.csv...'
    for dt in _data:
        with open('./%s/VendorLot.csv' % _month) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[index.n_Assembly] == dt.AH \
                        and row[index.n_TestHouse] == dt.TH \
                        and row[index.n_Product] == dt.Pr \
                        and row[index.n_WireType] == dt.Mt:
                    dt.total += int(row[index.n_Total])
                    dt.pas += int(row[index.n_Pass])
            if dt.total:
                dt.myld = float(dt.pas) / dt.total
    print 'Done!\n'
    return _data


def draw_trend_chart(_all_trend_chart, _month):
    """
    绘制所有的trendChart图，存到相应工程师的目录
    :param _all_trend_chart: 所有trendChart数据组成的List
    :param _month: 本月份，用于确定文件存放路径
    """
    global npelsb
    _clr = ['g', 'b', 'm', 'y', 'c', '#66CCFF', '#D09A67', '#98729B', '#200454', 'k']
    # _no仅用于每次print序号
    _no = 0
    for _onecht in _all_trend_chart:
        print 'NO.%03d' % _no
        _no += 1
        # _tar用于画99.5%的target线
        _tar = np.array([99.5] * len(_onecht.lot))
        print 'lot:', len(_onecht.lot)
        # 根据数据量改字体，效果不太定好，可以再调调
        if len(_onecht.lot) > 30:
            fz = 6
        elif len(_onecht.lot) > 25:
            fz = 7
        elif len(_onecht.lot) > 20:
            fz = 8
        elif len(_onecht.lot) > 15:
            fz = 9
        elif len(_onecht.lot) > 10:
            fz = 10
        else:
            fz = 11
        # elsBin存在的话都要画出来，先取数据到numpy的数组
        if _onecht.elsBin:
            npelsb = np.array([])
            # 先按一维的全部append
            for b in _onecht.els:
                npelsb = np.append(npelsb, b * 100)
            # 然后变形成二维的
            npelsb.shape = (len(npelsb) / len(_onecht.elsBin), len(_onecht.elsBin))
            lstelsb = list()
            # 然后转成List的元素存到lstelsb回来
            for i in xrange(len(_onecht.elsBin)):
                lstelsb.append(npelsb[:, i])
        fig = plt.figure(figsize=(10, 6))
        # 外框alpha值设为0，即透明
        fig.patch.set_alpha(0.)
        # 准备良率序列和OS序列的数据到numpy数组
        npyld = np.array([])
        npos = np.array([])
        x = np.arange(len(_onecht.lot))
        for i in xrange(len(_onecht.yld)):
            npyld = np.append(npyld, float(_onecht.yld[i]))
            npos = np.append(npos, float(_onecht.os[i]) * 100)
        # 内框适当缩小，以防文字超出
        plt.axes([0.1, 0.18, 0.8, 0.64])
        plt.ylabel('Yield(%)')
        plt.title('%s(%s)\n Test:%s   Assmebly:%s   Month:%s \nQuantity(Vdr.Lot):%d   Yield:%s' % (
            _onecht.Pr, _onecht.Mt, _onecht.TH, _onecht.AH, _month, _onecht.total,
            str(_onecht.myld * 100)[:6]) + '%  ' + 'OS:%s' % str(_onecht.osr * 100)[:5] + '%', fontsize=11)
        # 写x轴上的Lot Name，每个Lot Name以右上角为圆心逆时针旋转23度
        plt.xticks(np.arange(len(_onecht.lot)), _onecht.lot, rotation=23, ha='right', va='top', fontsize=fz)
        # 根据Yield的最小值动态调整Yield轴的刻度范围
        if min(npyld) > 98:
            mi = 90
        elif min(npyld) > 90:
            mi = min(npyld) * 5 - 400
        elif min(npyld) > 50:
            mi = min(npyld) * 2 - 100
        else:
            mi = 0
        plt.axis([0, len(_onecht.lot) - 1, mi, 100])
        # 画Yield趋势线
        plt.plot(npyld, linewidth=1.5, color='k', label='Yield')
        # 小于30批就可以在图上标出Yield的数值
        if len(_onecht.yld) < 30:
            for i, j in zip(x, npyld):
                plt.annotate('%2.2f' % j, xy=(i, j), fontsize=fz, color='k', ha='center', va='top')
        # 画趋势线
        plt.plot(_tar, '--', linewidth=0.5, color='r')
        # 画Yield的图例
        plt.legend(bbox_to_anchor=(0., 1., 1., 0.), borderaxespad=0., loc=3, fontsize=9)

        # 切到另一个X轴
        plt.twinx()
        plt.ylabel('Bin(%)')
        # 画出OS趋势线
        plt.plot(npos, linewidth=1, color='r', label='OS')
        # 画出OS图例
        plt.legend(bbox_to_anchor=(1., 1.), borderaxespad=0., loc=4, fontsize=9)

        # 画其它的趋势线
        # 先根据其它趋势的最大值动态调整右边Y轴的刻度范围
        if _onecht.elsBin:
            mx = max(np.max(npos), np.max(npelsb))
        else:
            mx = np.max(npos)
        if mx > 2:
            mx *= 1.5
        else:
            mx = 3
        plt.axis([0, len(_onecht.lot) - 1, 0, mx])

        # 小于30批就可以在图上标出OS率的数值
        if len(_onecht.yld) < 30:
            for i, j in zip(x, npos):
                plt.annotate('%1.3f' % j, xy=(i, j), fontsize=fz, color='r', ha='center', va='bottom')

        # 画出其它超过0.2%的Bin
        if _onecht.elsBin:
            plt.axis([0, len(_onecht.lot) - 1, 0, mx], 'off')
            ci = 0
            for elb in lstelsb:
                # 10种颜色， 循环显示
                cj = ci % 10
                plt.plot(elb, linewidth=1, color=_clr[cj], label=_onecht.elsBin[ci])
                # 小于30批就可以在图上标出Yield的数值
                if len(_onecht.yld) < 30:
                    for i, j in zip(x, elb):
                        plt.annotate('%1.3f' % j, xy=(i, j), fontsize=fz - 1, color=_clr[cj], ha='center', va='bottom')
                # 调整右边图例的字体大小
                if ci == 5:
                    lgdfz = 6
                elif ci > 5:
                    lgdfz = 4
                else:
                    lgdfz = 8
                # 画右边图例
                plt.legend(bbox_to_anchor=(1., 1.), borderaxespad=0., loc=4, fontsize=lgdfz)
                ci += 1
        # 画绿线
        monx = 0
        if _onecht.monthlot:
            for lti in xrange(len(_onecht.lot)):
                if _onecht.lot[lti] == _onecht.monthlot:
                    monx = lti
        if monx:
            plt.axvline(x=monx - 0.5, ymin=0, ymax=1, hold=None, color='g', linewidth=2)
        else:
            plt.axvline(x=0, ymin=0, ymax=1, hold=None, color='g', linewidth=2)
        # 显示网格线
        plt.grid()
        # plt.show()

        # |不能当文件名，所以要换掉
        st = ''
        for c in _onecht.AH:
            if c == '|':
                c = 'or'
            st += c
        _onecht.AH = st
        filename = '%s_%s_%s_%s_%s_TrendChart.png' % (_onecht.Pr, _onecht.AH, _onecht.TH, _onecht.Mt, _month)
        if not os.path.exists('./%s/%s/' % (_month, _onecht.tester)):
            os.mkdir('./%s/%s/' % (_month, _onecht.tester))
        plt.savefig('./%s/%s/' % (_month, _onecht.tester) + filename)
        print 'file %s saved in ./%s/%s/\n' % (filename, _month, _onecht.tester)
        plt.close()
    print '\n'


def main(_pare_to, _month):
    """
    外部调用这个函数，会画图
    :param _pare_to: 所有PareTo的List
    :param _month: 本月份
    """
    _data = getdata(_month, _pare_to, 'alq.csv')
    _data = getm(_data, _month)
    draw_trend_chart(_data, _month)
    return _data


if __name__ == '__main__':
    '''
    跑PareTo拿数据，不画PareTo图。只画TrendChart图。
    '''
    if not os.path.exists('./alq.csv'):
        raw_input("Can't find alq.csv, press Enter to Exit")
        exit()
    if not os.path.exists('./binList.csv'):
        raw_input("Can't find binList.csv, press Enter to Exit")
        exit()
    month = raw_input('input month, e.g., 201410\n')
    if not os.path.exists('./'+month+'/VendorLot.csv'):
        raw_input("Can't find ./%s/VendorLot.csv, press Enter to Exit" % month)
        exit()
    deletelot.main()
    p = pareTo.get_pare_to('alq.csv', 'binList.csv', month)
    data = getdata(month, p, 'alq.csv')
    data = getm(data, month)
    draw_trend_chart(data, month)
    raw_input('All ChendChart Done!\nPress Enter to Exit.')