import os
import zipfile
import glob

content = [
    "bin",
    "certifi",
    "idna"
]

def zip_dir(path, zip_file):
    #os.walk is walking the entire tree
    # root will change to all subfolders
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            print(file)
            #we are adding paths and files to the zip
            zip_file.write(os.path.join(root, file))

zip_file = zipfile.ZipFile("function.zip", 'w')

for path in content:
    print("path",path)
    if os.path.isdir(path):
        zip_dir(path, zip_file)
    else:
        zip_file.write(path)
zip_file.close()