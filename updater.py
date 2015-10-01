#! /usr/bin/env python
import os
import urllib
import urllib2
import shutil
import zipfile

# PurpleFace updater

# try to get current version
try:
    f = open("version", "r")
    cur_version = int(f.read())
except:
    cur_version = 0
    
zip_url = "https://github.com/2028games/PurpleFace/archive/master.zip"  # url for fetching zip from github
new_version_url = "https://raw.githubusercontent.com/2028games/PurpleFace/master/version"  # url of github version file
local_zip = "new_version.zip"  # location to save the zip


def main():
    try:
        # First get online version code
        print("Checking for updates...")
        response = urllib2.urlopen(new_version_url)
        new_version = int(response.read())
        if new_version <= cur_version:  # if up-tp-date
            print("PurpleFace is up to date! Goodbye.")
            return 0
        
        # else download new version
        print("PurpleFace will now update to the newest version (Version Code: {})".format(new_version))
        print("Please wait while downloading the new version...")
        urllib.urlretrieve(zip_url, local_zip)
        print("New version downloaded. Installing...")
        with zipfile.ZipFile(local_zip, "r") as local_zipfile:  # and extract every file to proper location
            for member in local_zipfile.infolist():
                extract_path = member.filename
                if "updater.py" not in extract_path:  # updater must not be updated!
                    local_zipfile.extract(member)  # extract in PurpleFace-master dir
                    parts = extract_path.split("/", 1)
                    if len(parts) < 2:
                        parts = extract_path.split("\\", 1)
                    new_path = parts[1]  # correct file location
                    if os.path.isfile(new_path):
                        os.remove(new_path)  # remove existing files
                    if os.path.isfile(extract_path):
                        os.rename(extract_path, new_path)  # and move new file to location
                    else:  # if its a dir
                        # try to make it if needed
                        try:
                            os.mkdir(new_path)
                        except:
                            pass
                    
        # delete leftovers
        shutil.rmtree("PurpleFace-master")
        os.remove(local_zip)
        print("Done! Bye.")
        
        return 0
    
    except urllib2.URLError, IOError:
        print("A connection error occured. Try again later.")
        return 1
    except:
        print("An unspecified error occured. Try again later.")
        return 1
        
if __name__ == "__main__":
    main()
