import os
import filecmp

os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip_shared/fluo_data')
path = os.getcwd()
print(path)

listdir = os.listdir(path)
listdir.sort()
print(listdir)

l_iter = iter(listdir)
f1 = next(l_iter)
while f1 != 'end':
    f2 = next(l_iter, 'end')
    if f2 == 'end':
        break
    f1_dir = os.path.join(path, f1)
    f2_dir = os.path.join(path, f2)
    result = filecmp.cmp(f1_dir, f2_dir, shallow = False)
    if result == False:
        f1 = f2
    if result == True:
        os.remove(f2)
        print(str(f2) + ' is removed')
        f1 = next(l_iter, 'end')
    print(f1)

