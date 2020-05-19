from QA_tool import *
from pathlib import Path

p = Path("/Users/sami/Desktop/test")

#instanceN_fold(fold_root='/Users/sami/Desktop/test', save_csv_path='/Users/sami/Desktop/sample/test.csv')
instanceN_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / "instance_num_check.csv"))

#sliceDis_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / 'slice_dist_check.csv'))