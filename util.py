import csv
import pprint as pp
import random

# Pretty print
def print(data):
	pp.pprint(data)

# Read csv as array of map
def read_csv(filename):
	ret = []
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		fields = None
		for row in reader:
			if fields == None:
				fields = row
			else:
				item = {}
				for i in range(0, len(row)):
					item[fields[i]] = row[i]
				ret.append(item)
		csvfile.close()
	return ret

def write_csv(data, filename):
	with open(filename, 'w') as csvfile:
		writer = csv.writer(csvfile)
		fields = list(data[0].keys())
		writer.writerow(fields)
		for row in data:
			writer.writerow(list(row[x] for x in fields))
		csvfile.close()

# Pipe process data
def pipe(data, fns):
	if len(fns) == 0:
		return data
	fn = fns[0]
	return pipe(fn(data), fns[1:])

# Wrap function to traverse on array, return replacing value, return None to remove
def each(cb):
	def fn(arr):
		ret = []
		for x in arr:
			item = cb(x)
			if item != None:
				ret.append(item)
		return ret
	return fn

# Keep selected fields of each value in array
def select(fields):
	def fn(item):
		vitem = {}
		for f in fields:
			if type(f) == tuple:
				if f[0] in item:
					category = f[1:]
					f = f[0]
					source = item[f]
					val = (source, (category.index(source) + 1) if source in category else 0, len(category))
					vitem[f] = val
				else:
					vitem[f[0]] = None
			else:
				vitem[f] = item[f] if f in item else None
		return vitem
	return each(fn)

# Randomly sort array
def shuffle():
	def fn(arr):
		ret = arr[0:]
		random.shuffle(ret)
		return ret
	return fn

# Keep count ammount of random item in array
def randkeep(count):
	def fn(arr):
		if count > len(arr):
			return arr
		else:
			start = random.randint(0, len(arr) - count)
			return arr[start:start + count]
	return fn
	

# Make rows to arrays of number
def tensorize():
	def fn(item):
		ret = []
		for k in item.keys():
			v = item[k]
			if type(v) == tuple:
				for i in range(0, v[2] + 1):
					if v[1] == i:
						ret.append(1)
					else:
						ret.append(0)
			else:
				ret.append(v)
		return ret
	return each(fn)

# Split array to map of arrays
def split(route):
	def fn(arr):
		ret = {}
		for r in route.keys():
			ret[r] = pipe(arr, route[r])
		return ret
	return fn

