import collections
import datetime
import sys

def _make_column_names(tokens: list):
	table = str.maketrans("", "", " .[]()")
	columns = [ ]
	for s in tokens:
		s = s.translate(table)
		columns.append (s)
	return columns

def _map_bool(x: str):
	if x == "":
		return None
	elif x in [ "true", "True" ]:
		return True
	elif x in [ "false", "False" ]:
		return False
	else:
		assert False

# 02/05/2025 04:57:25
def _map_date(x: str) -> datetime.datetime:
	n = len(x)
	if n == 0:
		return None
	assert n == 19
	month = int(x[0:2])
	day = int(x[3:5])
	year = int(x[6:10])
	hour = int(x[11:13])
	minute = int(x[14:16])
	second = int(x[17:19])
	return datetime.datetime(year, month,day, hour, minute, second)

def _map_float(x: str):
	if x == "":
		return None
	if x.endswith (" %"):
		x = x[:-2]
	if x.endswith (" GB"):
		x = x[:-3]
	if x.find(",") > 0 and x.find(".") < 0:
		x = x.replace(",", ".")
	return float(x)

def _map_int(x: str):
	if x == "":
		return None
	return int(x)

# "0 hours 0 minutes 25 seconds 667 milliseconds" -> 25.667
def _map_time(x: str):
	if x == "":
		return None
	tokens = x.split(" ")
	n = len(tokens)
	assert n % 2 == 0
	out = 0.0
	for i in range(0, n, 2):
		key = tokens[i+1]
		value = tokens[i]
		if key == "hours":
			out += 3600.0 * float(value)
		elif key == "minutes":
			out += 60.0 * float(value)
		elif key == "seconds":
			out += 1.0 * float(value)
		elif key == "milliseconds":
			out += 0.001 * float(value)
		else:
			assert False
	return out

def _parse_csv(path: str):
	columns = None
	rows = [ ]
	with open(path, "rt") as csv:
		isHeader = True
		idx_bools = [ ]
		idx_dates = [ ]
		idx_floats = [ ]
		idx_ints = [ ]
		idx_times = [ ]
		for line in csv.readlines():
			line = line.strip()
			tokens = line.split("|")
			if isHeader:
				columns = _make_column_names(tokens)
				for key in [ "IsVirtual", "Is64bitOS", "Is64bitprocessor" ]:
					idx = columns.index(key)
					idx_bools.append(idx)
				for key in [ "Date" ]:
					idx = columns.index(key)
					idx_dates.append(idx)
				for key in [ "AvailablePhysicalMemory", "BuildSizeX", "BuildSizeY", "BuildSizeZ", "CPUUsage", "FreePhysicalMemory", "FreeVirtualMemory", "GPUUsage", "MemoryUsage", "MemoryUsageGB", "MinSupportHeight", "TotalPhysicalMemory" ]:
					idx = columns.index(key)
					idx_floats.append(idx)
				for key in [ "EndingNumTriangles", "FileSize", "Filecount", "GPUAdapterRAM", "IntegratedAdapterRAM", "NoofCores", "NoofThreads", "NumParts", "Subsessioncount", "StartingNumTriangles" ]:
					idx = columns.index(key)
					idx_ints.append(idx)
				for key in [ "Time", "TimeInCommand" ]:
					idx = columns.index(key)
					idx_times.append(idx)
				isHeader = False
			else:
				for idx in idx_bools:
					tokens[idx] = _map_bool(tokens[idx])
				for idx in idx_dates:
					tokens[idx] = _map_date(tokens[idx])
				for idx in idx_ints:
					tokens[idx] = _map_int(tokens[idx])
				for idx in idx_floats:
					tokens[idx] = _map_float(tokens[idx])
				for idx in idx_times:
					tokens[idx] = _map_time(tokens[idx])
				tokens = [ (None if x == "" else x) for x in tokens ]
				rows.append (tokens)
	return columns, rows

def create_histogram(l: list):
	count = { }
	for x in l:
		try:
			count[x] += 1
		except KeyError:
			count[x] = 1
	result = [ [ key, value ] for key, value in count.items() ]
	result = sorted(result, key=lambda x: -x[1])
	return result

def read(path: str):
	columns, rows = _parse_csv(path)
	Item = collections.namedtuple("Item", columns)
	items = [ Item (*row) for row in rows ]

"""
	# for figuring out types of columns
	row_complete = rows[0]
	n = len(columns)
	for row in rows:
		for i in range(n):
			if row_complete[i] == None and row[i] != None:
				row_complete[i] = row[i]
	item_complete = Item(*row_complete)
"""

	return items

