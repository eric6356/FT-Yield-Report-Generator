# coding:utf-8
"""
在alq.csv中追加本月Lot之后，需要删除跨月Lot的旧记录
本程序先把alq按照Lot名排序，找到连续2个Lot名相同，即删除前一个Lot，也就是上个月的Lot
时间格式化是为了便于之后按时间排序然后存回去
"""
import csv
import index


def main():
    # open('alq_bkp.csv', "wb").write(open('alq.csv', "rb").read())
    # print 'alq.csv备份在alq_bkp.csv'
    with open('alq.csv') as f:
        lreader = list()
        reader = csv.reader(f)
        for row in reader:
            lreader.append(list(row))

    # 按LotNo排序，便于查找
    sl = sorted(lreader, key=lambda lreader: lreader[index.LotNo])
    dei = list()
    for i in range(len(sl)):
        try:
            # 时间格式化，以便排序
            # yyyy-m-d h:mm -> yyyy-mm-dd hh:mm
            # print 'before formating:', sl[i][index.MeasureTime]
            if ord('0') > ord(sl[i][index.MeasureTime][6]) or ord(sl[i][index.MeasureTime][6]) > ord('9'):
                sl[i][index.MeasureTime] = sl[i][index.MeasureTime][:5] + '0' + sl[i][index.MeasureTime][5:]
            if ord('0') > ord(sl[i][index.MeasureTime][9]) or ord(sl[i][index.MeasureTime][9]) > ord('9'):
                sl[i][index.MeasureTime] = sl[i][index.MeasureTime][:8] + '0' + sl[i][index.MeasureTime][8:]
            if ord('0') > ord(sl[i][index.MeasureTime][12]) or ord(sl[i][index.MeasureTime][12]) > ord('9'):
                sl[i][index.MeasureTime] = sl[i][index.MeasureTime][:11] + '0' + sl[i][index.MeasureTime][11:]
        except Exception, e:
            print sl[i][index.MeasureTime]
            print e
        # print 'after formating:', sl[i][index.MeasureTime]

    for i in range(len(sl)-1):
        if sl[i][index.LotNo] == sl[i+1][index.LotNo]:
            # 记录需要被删除的Lot下标
            dei.append(i)
            print 'find over month Lot, old record deleted'
            print 'OLD\tLot:', sl[i][index.LotNo], 'Time:', sl[i][index.MeasureTime], 'Total:', sl[i][index.Total]
            print 'NEW\tLot:', sl[i+1][index.LotNo], 'Time:', sl[i+1][index.MeasureTime], 'Total:', sl[i+1][index.Total]

    # 从最大的index开始pop，全部pop掉
    for i in dei[::-1]:
        sl.pop(i)
    # 按时间排序后存回去
    sl = sorted(sl, key=lambda sl:sl[index.MeasureTime])
    writer = csv.writer(file('alq.csv', 'wb'))
    for row in sl:
        writer.writerow(row)

if __name__ == '__main__':
    main()
