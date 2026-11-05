import sys, importlib
def load():
    out = {}
    for d, m in [('day1','full_data2'),('day2','data2'),('day3','data3'),('day4','data4'),('day5','data5'),('day6','data6'),('day7','data7'),('day8','data8'),('day9','data9'),('day10','data10'),('day11','data11'),('day12','data12'),('day13','data13'),('day14','data14')]:
        sys.path.insert(0, f'/home/claude/{d}')
        M = importlib.import_module(m)
        sys.path.pop(0)
        out[d] = dict(M.E)
        if hasattr(M,'OVER'): out[d+'_over'] = M.OVER
    return out
