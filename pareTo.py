# coding:utf-8
"""
绘制Pareto
注释标注在对应代码的上一行
"""
import csv
import index
import matplotlib.pyplot as plt
import numpy as np
import os
import deletelot


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


def get_bin_list(_file):
    """
    读取binList.csv到一个List变量
    :param _file: binList.csv文件
    :return: 含有binList数据的List
    """
    _binList = list()
    with open(_file, 'rb') as _listFile:
        _r = csv.reader(_listFile)
        for _row in _r:
            # 第一行是标题，跳过不处理
            if _row[0] != 'Product':
                _binList.append(_row)
    return _binList


def he_bing(_all_pare_to):
    """
    将一个月所有的Lot中相同产品的合并，打开注释运行可检查结果。
    :param _all_pare_to:合并前所有的Lot
    :return: 合并后所有的Lot
    """
    print 'he bing...'
    _l = len(_all_pare_to)
    # print 'shuliang:', _l
    # print 'before hebing:'
    # for _i in xrange(_l):
    # print 'NO.%02d' % (_i + 1)
    # _alPareTo[_i].prt()
    _d = list()

    # 这一段太神奇，现在我自己也看不懂……
    # 反正就是一个On2的算法，找到重复的Lot，数据加到一个里面，然后删掉其余的Lot。
    for _i in xrange(_l):
        _m = _l - _i - 1
        # print 'm = %02d' % _m,
        for _j in xrange(_m):
            if _all_pare_to[_m].TH == _all_pare_to[_j].TH \
                    and _all_pare_to[_m].AH == _all_pare_to[_j].AH \
                    and _all_pare_to[_m].Pr == _all_pare_to[_j].Pr \
                    and _all_pare_to[_m].Mt == _all_pare_to[_j].Mt:
                # print 'j = %02d' % _j,
                for _k in xrange(35):
                    _all_pare_to[_j].bin[_k] = (_all_pare_to[_j].bin[_k][0],
                                                _all_pare_to[_j].bin[_k][1] + _all_pare_to[_m].bin[_k][1])
                _d.append(_m)
                break
                # print ' '
    for _i in _d:
        del _all_pare_to[_i]

    for _i in xrange(len(_all_pare_to)):
        for _j in xrange(35):
            _all_pare_to[_i].sum += _all_pare_to[_i].bin[_j][1]
    # print 'after hebing:'
    # print 'shuliang:', len(_alPareTo)
    # for _i in xrange(len(_alPareTo)):
    # print 'NO.%02d' % (_i + 1)
    # _alPareTo[_i].prt()
    print 'Gone!\n'
    return _all_pare_to


def get_pare_to(_file, _bin_list_file, _this_month):
    """
    获取pare to图表
    :param _file: alq.csv文件
    :param _bin_list_file:binList文件
    :param _this_month:
    :return:含有所有PareTo图所需要的数据的List
    """
    print 'Getting pareTo data...'
    _binList = get_bin_list(_bin_list_file)
    _allPareTo = list()
    with open(_file, 'rb') as _f:
        _reader = csv.reader(_f)
        for _row in _reader:
            # 第一行是标题，跳过不处理，只处理本月的Lot
            if _row[index.Month] == _this_month and _row[index.TestHouse] != 'TestHouse' and _row[index.TestHouse]:
                _onePareTo = PareTo()
                _onePareTo.TH = _row[index.TestHouse]
                _onePareTo.AH = _row[index.AssmeblyHouse]
                _onePareTo.Pr = _row[index.PRODUCT]
                _onePareTo.Mt = _row[index.mental]
                _done = None
                # 对于每一个Lot，都到binList里去找对应的Bin Name
                for _rbinlist in _binList:
                    if _row[index.PRODUCT] == _rbinlist[0]:
                        _done = True
                        for _i in xrange(35):
                            _onePareTo.bin.append((_rbinlist[_i + 1], int(_row[index.BIN1 + _i])))
                        _onePareTo.tester = _rbinlist[36]
                        _onePareTo.pkgt = _rbinlist[37]
                        break
                # 若在binList里没找到，则添加index中默认的Bin Name，Bin8为OS，其余Bin为noData
                if not _done:
                    for _i in xrange(35):
                        _onePareTo.bin.append((index.bin_name[_i], int(_row[index.BIN1 + _i])))
                    _onePareTo.tester = 'unknow'
                    _onePareTo.pkgt = 'unknow'
                _allPareTo.append(_onePareTo)
    print 'Done!\n'
    # 接下来将相同产品的Lot合并
    # 合并之后，_alPareTo中的每一个元素都是一张pareTo的源数据了
    he_bing(_allPareTo)
    return _allPareTo


def draw_pare_to(_all_pare_to, _month):
    """
    绘制所有的pareTo图，存到相应工程师的目录
    :param _all_pare_to: 所有的pareTo数据组成的List
    :param _month: 本月份，用于确定文件存放路径
    """
    # _all_pare_to = _all_pare_to[:3] # 取3个Debug
    # 将每张图按照Bin数量从高到低排序
    for _i in xrange(len(_all_pare_to)):
        _lb = _all_pare_to[_i].bin
        _all_pare_to[_i].bin = sorted(_lb, key=lambda x: x[1], reverse=True)
    for _i in xrange(len(_all_pare_to)):
        # _val是每个Bin的数量，也就是柱状图中每条柱子的高度
        # b是要写在x轴上的Bin Name list
        _val = list()
        _b = list()
        print 'NO.%03d' % _i
        for _j in xrange(35):
            # 数量非0的Bin才会画出来，找到第一个数量为0的就break
            if _all_pare_to[_i].bin[_j][1] == 0:
                break
            _val.append(_all_pare_to[_i].bin[_j][1])
            _b.append(_all_pare_to[_i].bin[_j][0])
        _fei0 = len(_val)

        fig = plt.figure(figsize=(10, 6))
        # 外框alpha值设为0，即透明
        fig.patch.set_alpha(0.)
        # 内框缩小，以防文字太长超出
        plt.axes([0.1, 0.2, 0.8, 0.6])
        _rects = plt.bar(np.arange(_fei0), _val)
        plt.ylabel('Quantity')
        plt.title('%s(%s)\n Teszt:%s   Assmebly:%s   Month:%s\n Quantity(Lot):%d' % (
            _all_pare_to[_i].Pr, _all_pare_to[_i].Mt, _all_pare_to[_i].TH, _all_pare_to[_i].AH, _month,
            _all_pare_to[_i].sum), fontsize=11)

        # 根据非0 Bin的数量计算出字体的大小，现在效果不太好，还可以再调调
        if _fei0 < 15:
            fontsize = 10
        elif _fei0 < 20:
            fontsize = 9
        elif _fei0 < 25:
            fontsize = 8
        else:
            fontsize = 7
        # print '_fei0=', _fei0
        # print 'size=', fontsize

        # 写x轴上的Bin Name，每个Bin Name以右上角为圆心逆时针旋转20度
        plt.xticks(np.arange(_fei0) + 0.4, _b, rotation=20, ha='right', va='top', fontsize=fontsize - 1)
        # 在每个柱子上方标注百分比
        for _rect in _rects:
            h = _rect.get_height()
            plt.text(_rect.get_x()+_rect.get_width()/2., h, '%2.1f' % (float(h) / _all_pare_to[_i].sum * 100),
                     fontsize=fontsize, ha='center', va='bottom')
        # plt.show()

        # |不能当文件名，所以要换掉
        st = ''
        for c in _all_pare_to[_i].AH:
            if c == '|':
                c = 'or'
            st += c
        _all_pare_to[_i].AH = st
        filename = '%s_%s_%s_%s_%s_PareTo.png' % (
            _all_pare_to[_i].Pr, _all_pare_to[_i].AH, _all_pare_to[_i].TH, _all_pare_to[_i].Mt, _month)
        if not os.path.exists('./%s/%s/' % (_month, _all_pare_to[_i].tester)):
            os.mkdir('./%s/%s/' % (_month, _all_pare_to[_i].tester))
        plt.savefig('./%s/%s/' % (_month, _all_pare_to[_i].tester) + filename)
        print 'file %s saved in ./%s/%s/\n' % (filename, _month, _all_pare_to[_i].tester)
        plt.close()


def main():
    """
    外部调用这个函数, 会画图
    :return:所有PareTo组成的List和本月份
    """
    if not os.path.exists('./alq.csv'):
        raw_input("Can't find alq.csv, press Enter to Exit")
        exit()
    if not os.path.exists('./binList.csv'):
        raw_input("Can't find binList.csv, press Enter to Exit")
        exit()
    month = raw_input("input month e.g., 201410\n")
    if not os.path.exists('./' + month + '/VendorLot.csv'):
        raw_input("Can't find ./%s/VendorLot.csv, press Enter to Exit" % month)
        exit()
    deletelot.main()
    p = get_pare_to('alq.csv', 'binList.csv', month)
    draw_pare_to(p, month)
    return p, month


if __name__ == '__main__':
    main()
    raw_input('All PareTo Done!\nPress Enter to Exit.')
