from QA_tool import *
from pathlib import Path

p = Path("/Users/sami/Desktop/test")
p_acc = p / "10291207324"
assert p_acc.exists() == True

# Slice distance check
assert dcm_slicedistance(p_acc) == 1

for x in p.iterdir() if x.is_dir():
    print(dcm_slicedistance(x))

[dcm_slicedistance(x) for x in p.iterdir() if x.is_dir()]

#instanceN_fold(fold_root='/Users/sami/Desktop/test', save_csv_path='/Users/sami/Desktop/sample/test.csv')
instanceN_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / "instance_num_check.csv"))

#sliceDis_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / 'slice_dist_check.csv'))