# coding:utf-8
"""
生成summary.csv和每位工程师的summary图表
"""

import index
import pareTo
import trendChart
import deletelot
import os
import matplotlib.pyplot as plt
import numpy as np



class Summry():
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


def getsmry(_month, _smry):
    """
    从TrendChart Dict生成用于Summary图的所有数据
    :param _month: 本月份
    :param _smry: TrendChart Dict
    :return: 所有Smry图组成的List
    """
    _alsmry = list()
    for _tster in _smry:
        _onesmry = Summry()
        _onesmry.title = '%s %s/%s yield summary' % (_tster, _month[:4], _month[-2:])
        _onesmry.prName = map(lambda x: x[index.s_Name], _smry[_tster])
        _onesmry.yld = map(lambda x: x[index.s_Yield], _smry[_tster])
        _onesmry.qty = map(lambda x: x[index.s_Qty], _smry[_tster])
        _onesmry.tester = _tster
        _alsmry.append(_onesmry)
    return _alsmry


def smry_dict(_data):
    """
    输入TrendChart的所有数据，注意是含有总数和良率的。生成一个Dict，按照工程师名字排序后返回。
    :param _data: 所有的TrendChart组成的List
    :return: TrendChart Dict
    """
    smry = dict()
    for dt in _data:
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
    # 以工程师名字排序
    for tster in smry:
        st = smry[tster]
        smry[tster] = sorted(st, key=lambda x: x[index.s_Qty], reverse=True)
    return smry


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
        if not os.path.exists('./%s/%s/' % (_month, _onesmry.tester)):
            os.mkdir('./%s/%s/' % (month, _onesmry.tester))
        plt.savefig('./%s/%s/summary.png' % (_month, _onesmry.tester))
        print 'file summary.png saved in ./%s/%s/' % (_month, _onesmry.tester)


def save_summary(_smry, _month):
    """
    将Smry Dict存到summary.csv中
    :param _smry: Smry Dict
    :param _month: 本月份
    """
    with open('./%s/summary.csv' % _month, 'w') as f:
        pr = ['Product', 'pkgType', 'AH', 'TH', 'Mental', 'Qty', 'Yield', 'OS', 'tester', 'Name', '\n']
        for x in pr:
            f.write(str(x))
            if x != '\n':
                f.write(',')
        for tster in _smry:
            for pr in _smry[tster]:
                for x in pr:
                    f.write(str(x))
                    if x != '\n':
                        f.write(',')

    print 'file summary.csv saved in ./%s' % _month


def main(_data, _month):
    """
    外部调用这个函数，会画图
    :param _data: 所有TrendChart数据
    :param _month:本月份
    """
    _smd = smry_dict(_data)
    _alsmry = getsmry(_month, _smd)
    drawsmry(_month, _alsmry)
    save_summary(_smd, _month)
    raw_input('All Summary Done!\nPress Enter to Exit.')

if __name__ == "__main__":
    '''
    跑PareTo和TrendChart拿数据，不画图。只画Summary图。
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
    data = trendChart.getdata(month, p, 'alq.csv')
    data = trendChart.getm(data, month)
    smd = smry_dict(data)
    alsmry = getsmry(month, smd)
    drawsmry(month, alsmry)
    save_summary(smd, month)
    raw_input('All Summary Done!\nPress Enter to Exit.')