import sys
import os

def main():
    if len(sys.argv) > 1:
        start = int(sys.argv[1])
    else:
        print "Invalid Args"
        return 1
    
    if len(sys.argv) > 2:
        step = int(sys.argv[2])
    else:
        step = 1
        
    i = start
    while True:
        location = "level" + str(i).zfill(2) + ".tmx"
        if os.path.exists(location):
            f = open(location, "r")
            content = f.read()
            f.close()
            content = content.replace("Level " + str(i), "Level " + str(i + 1))
            f = open(location, "w")
            f.write(content)
            f.close()
            print('File %s was fixed' % location)
            i += step
        else:
            return 0;
        
        
if __name__ == "__main__":
    main()
         
            