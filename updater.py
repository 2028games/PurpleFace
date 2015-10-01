#! /usr/bin/env python
import os
import urllib
import urllib2
import shutil
import zipfile


try:
    f = open("version", "r")
    cur_version = int(f.read())
except:
    cur_version = 0
    
zip_url = "https://github.com/2028games/PurpleFace/archive/master.zip"
new_version_url = "https://raw.githubusercontent.com/2028games/PurpleFace/master/version"
local_zip = "new_version.zip"


def main():
    try:
        print("Checking for updates...")
        response = urllib2.urlopen(new_version_url)
        new_version = int(response.read())
        if new_version <= cur_version:
            print("PurpleFace is up to date! Goodbye.")
            return 0
        
        print("PurpleFace will now update to the newest version (Version Code: {})".format(new_version))
        print("Please wait while downloading the new version...")
        urllib.urlretrieve(zip_url, local_zip)
        print("New version downloaded. Installing...")
        with zipfile.ZipFile(local_zip, "r") as local_zipfile:
            for member in local_zipfile.infolist():
                extract_path = member.filename
                if "updater.py" not in extract_path:         
                    local_zipfile.extract(member)
                    new_path = extract_path.split(os.sep, 1)[1]
                    if os.path.isfile(new_path):
                        os.remove(new_path)
                    if os.path.isfile(extract_path):
                        os.rename(extract_path, new_path)
                    
        shutil.rmtree("PurpleFace-master")
        os.remove(local_zip)
        print("Done! Bye.")
        
        return 0
    
    except urllib2.URLError, IOError:
        print("A connection error occured. Try again later.")
        return 1
    """except:
        print("An unspecified error occured. Try again later.")
        return 1"""
        
if __name__ == "__main__":
    main()
        
        
        
