import unittest
import datetime
from main import process_matrix_mult


data0 = ''
data1 = ''
with open('file0.txt', 'r') as f:
	data0 = f.read()

with open('file1.txt', 'r') as f:
	data1 = f.read()

start = datetime.datetime.now()
x = process_matrix_mult((data0, data1))
end = datetime.datetime.now()

print('done in', end - start)

print(x)
