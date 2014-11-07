import pareTo
import trendChart
import summary

p, month = pareTo.main()
trd = trendChart.main(p, month)
summary.main(trd, month)
