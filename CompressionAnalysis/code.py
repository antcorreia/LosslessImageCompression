
import bz2
import lzma
import deflate
import time

#bzip2
print("bz2")

with open("egg.bmp",'rb') as f:
    original_data = f.read()
    f.close()

print ('Original     :', len(original_data))

start_time = time.time()
with bz2.open("egg.bz2", "wb") as f:
    # Write compressed data to file
    unused = f.write(original_data)
print("--- %s seconds ---" % (time.time() - start_time))

f = open("egg.bz2")
f.seek(0,2)
size = f.tell()
print ('Compressed   :', size)

start_time = time.time()
with bz2.open("egg.bz2", "rb") as f:
    # Decompress data from file
    content = f.read()
    ff = open("egg_bzip2.bmp", "wb")
    ff.write(original_data)
    ff.close()


print("--- %s seconds ---" % (time.time() - start_time))
print ('Decompressed :', len(content))


#lzma
print("lzma")
with open("egg.bmp",'rb') as f:
    original_data = f.read()
    f.close()

print ('Original     :', len(original_data))

start_time = time.time()
with lzma.open("egg.xz", "wb") as f:
    # Write compressed data to file
    u = f.write(original_data)
print("--- %s seconds ---" % (time.time() - start_time))

f = open("egg.xz")
f.seek(0,2)
size = f.tell()
print ('Compressed   :', size)

start_time = time.time()
with lzma.open("egg.xz", "rb") as f:
    # Decompress data from file
    content = f.read()
    ff = open("egg_lzma.bmp", "wb")
    ff.write(original_data)
    ff.close()

print("--- %s seconds ---" % (time.time() - start_time))
print ('Decompressed :', len(content))

#deflate
print("deflate")

with open("egg.bmp",'rb') as f:
    original_data = f.read()
    f.close()

print('Original     :', len(original_data))

start_time = time.time()
a = deflate.gzip_compress(original_data)
print("--- %s seconds ---" % (time.time() - start_time))

print ('Compressed   :', len(a))

f = open("egg.def", "wb")
# Write compressed data to file
un = f.write(a)
f.close()

f =  open("egg.def", "rb")
# Write compressed data to file
comp = f.read()
f.close()

start_time = time.time()
b = deflate.gzip_decompress(comp)

f = open("egg_def.bmp", "wb")
# Write decompressed data to file
p = f.write(b)
f.close()

print("--- %s seconds ---" % (time.time() - start_time))
print ('Decompressed :', len(content))
