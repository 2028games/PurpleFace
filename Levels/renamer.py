#! /usr/bin/env python
import os
import sys

def rename(location, step = 1):
	(name, extension) = os.path.splitext(location)
	new_name = name[0: -2] + str(int(name[-2: len(name)]) + step).zfill(2)
	new_location = new_name + extension
	if os.path.exists(new_location):
		rename(new_location, step)
		
	os.rename(location, new_location)
	print('renamed "%s" to "%s"' % (location, new_location))

def main():
	if len(sys.argv) > 1:
		location = sys.argv[1]
	else:
            print "Invalid Args"
            return 1
        
	if len(sys.argv) > 2:
            step = int(sys.argv[2])
        else:
            step = 1
	
	if step == 0:
		return 0
		
	if os.path.exists(location):
		rename(location, step)
		return 0
	else:
		print('file "%s" does not exist' % location)
		return 1
		
if __name__ == "__main__":
	main()