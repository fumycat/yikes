import csv
import operator

def parse_nvprof_log(filename):
    with open(filename, 'r') as file:
        csvr = csv.reader(file, delimiter=',')
    
        next(csvr) # skip ===
        next(csvr)
        next(csvr)

        head_names = next(csvr)
        head_units = next(csvr)

        head = list(map(operator.add, head_names, [f'({i})' for i in head_units]))

        result = []

        for row in csvr:
            result.append({head[i]: e for i, e in enumerate(row)})

        return result

def parse_output(filename, tt):
    cxtype = int if tt == 'int' else float
    with open(filename, 'r') as file:
        return [cxtype(i) for i in file.read().split()]
