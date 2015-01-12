import os
from hashlib import md5

def hash_file(path,bs=4096):
    print "starting hash_file()"
    md5sum=md5()
    with open(path, 'rb') as f:
        while True:
            chunk=f.read(bs)
            if not chunk:
                break
            md5sum.update(chunk)
        return md5sum.hexdigest()

def dup_sizes(base_dir='.'):
    print "starting dup_sizes()"
    results = {}
    counter=0

    for root, dirs, files in os.walk(base_dir):
        path=filter(os.path.isfile,(os.path.join(root,f) for f in files))
        print str(path)
        print counter
        counter+=1
        for p in path:
            size= str(os.path.getsize(p))
            if size in results:
                results[size].append(p)
            else:
                results[size]=[p]
    return (val for key, val in results.items() if len(val) >1)

def dup_hashes(sizes):
    print "starting dup_hashes()"
    dups=[]
    for e in sizes:
        hashes ={}
        for p in e:
            md5sum=hash_file(p)
            if md5sum in hashes:
                dups.append(p)
            else:
                hashes[md5sum]= p
    return dups

def find_dups(base_dir='.'):
    print "starting find_dups()"
    sizes = dup_sizes(base_dir)
    return dup_hashes(sizes)

delFiles =open('__deletedfiles__.txt', 'w')
root=os.getcwd()
counter=0

for file_ in find_dups(root):
    try:
        print "deleting file"
        counter+=1
        delFiles.write(str(file_)+'\n')
        os.remove(file_)
    except:
        pass

delFiles.write(str(counter))
delFiles.close()
print "finishes"