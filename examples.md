# Image File Structure

```
. (root)
├── 123456789 (subject_ID)
│   ├── 5555555 (accession_number)
│   │   ├── 2 (instance)
│   │   │   ├── 1234.dcm
│   │   │   ├── 1235.dcm
│   │   │   ├── 1236.dcm
│   │   ├── 3 (another instance)
```

# Setup file path

```python
from pathlib import Path

dcm_dir = Path("path/to/subject_ID/accession_number/")
#Use `dcm_dir = Path("~/path/to/dcm_dir/").expanduser()` #if need to expand '~'

# Check if dcm_dir exists
dcm_dir.exists() #True
```

The `dcm_dir` is the directory corresponding to the accession number.

# Checks

## Instance number check

```python
# For image of type '2'
dcm_instance(p / "2")

# For image of type '3'
dcm_instance(p / "3")
```

:white_check_mark:​ if the output above returns a triple `(<num>, <num>, 0)` where the first and second numbers are the same. For example, if `dcm_instance(<path>)` returned (187, 187, 0), this would pass the instance number check.

## Slice distance check

```python
dcm_slicedistance(dcm_dir)
```

:white_check_mark:​ if the output above yields $1$, then this session passes the slice distance.


# Convert a session from DICOM to NIFTI

The 'PosixPath' (from `pathlib`) is not understood, so the workaround is to use `os.fspath(p)`.

```python
import os

# Convert the entire dcm_dir
dcm2nii(src_root = os.fspath(dcm_dir), dst_root = os.fspath(dcm_dir / "nifti"))

# Convert just one image type, e.g. '2', from the dcm_dir
dcm2nii(src_root = os.fspath(dcm_dir / "2"), dst_root = os.fspath(dcm_dir / "nifti"))
```

# Generate QA report and Check instance number

There are some assumptions made about the file structure that caused trouble as is using the original `QA_tool.py`. Instances in my DICOM folder structure are not followed by additional subdirectories, such as 'DICOM' or 'secondary'. I made changes, but I still believe that a more agnostic method should be used. The other issue is that if it contains the dreaded .DS_Store or other files, it may throw an error.

Example using `fd` to get the unique image instance directories:

```bash
# Echo the parent directory of the discovered path -> sort, uniq
fd -e dcm -x echo {//} | sort | uniq
```

```python
p = Path("path/to/dcm_root") 
#p = Path("/Users/sami/Desktop/sample")

instanceN_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / "instance_num_check.csv"))
```

# Filter sessions with few slices but that pass instance number check

```python
filter_few_slices(csv_path = os.fspath(p / 'instance_num_check.csv'))
```

# Check slice distance on a batch of sessions and Generate QA Report

```python
sliceDis_fold(fold_root=os.fspath(p), save_csv_path=os.fspath(p / 'slice_dist_check.csv'))
```

# Convert a batch of sessions from DICOM to NifTI

```python
dcm2nii_project()
```