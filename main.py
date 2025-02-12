import sys
import telemetry_util

# you can download .csv files using "Export Data" (in upper right) from:
# 
# https://aztelemetrystage3.3dsystems.internal:3443/all-events

def main():
	path_csv = sys.argv[1]
	items = telemetry_util.read()
	# do things here
	return

if __name__ == "__main__":
	main()

