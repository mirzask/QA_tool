import pandas as pd
import pydicom
from pathlib import Path


"""
Unused libraries:
import nibabel as nib
import re
from glob import glob
from collections import Counter
"""


def mkdir(path):
    """
    Helper function to make directory using `pathlib.Path`
    """
    if not Path(path).exists():
        Path(path).mkdir(parents=True, exist_ok=True)


def dcm_instance(dcm_root):
    """
    Check instance numbers in a DICOM folder
    Does the instance number match the number of DICOMs in each session?
    Returns (<num1>, <num2>, <num3>)
    Valid: if <num1> == <num2> & <num3> == 0 (<num3> is the diff b/w num1 and num2)
    Invalid: if <num1> != <num2>, i.e. <num3> != 0
    """
    if Path(dcm_root).exists() == False:
        print("This folder does not exist. Please input an existing folder path.")
    dcm_list = list(Path(dcm_root).glob("**/*.dcm"))
    # dcm_list = glob(os.path.join(dcm_root, "*.dcm"))
    if len(dcm_list) == 0:
        print(
            "We were unable to find DICOM files in this root directory. Please review path and try again."
        )
    #slicePos = []
    instanceN = []
    for i in range(len(dcm_list)):
        ds = pydicom.dcmread(str(dcm_list[i]))
        # slicePos.append(ds.SliceLocation)
        instanceN.append(ds[0x20, 0x13].value)
    print("max and min of instanceN", max(instanceN), min(instanceN))
    return (
        len(instanceN),
        max(instanceN) - min(instanceN) + 1,
        max(instanceN) - min(instanceN) + 1 - len(instanceN),
    )


def dcm_slicedistance(dcm_root):
    """
    Calculate slice distance given a root directory
    """
    if Path(dcm_root).exists() == False:
        print("This folder does not exist. Please input an existing folder path.")
    dcm_list = list(Path(dcm_root).glob("**/*.dcm"))
    # dcm_list = os.listdir(dcm_root)
    # dcm_list = glob(os.path.join(dcm_root, "*.dcm"))
    ds_list = []
    # skipped_accession = []
    for i in range(len(dcm_list)):
        # ds = pydicom.dcmread(dcm_list[i])
        ds = pydicom.dcmread(str(dcm_list[i]))
        if hasattr(ds, "SliceLocation"):  # some images do not have 'SliceLocation'
            ds_list.append(ds.SliceLocation)
    #       else:
    #           skipped_accession.append(ds.AccessionNumber)

    #   print(f'The following accession numbers have missing "SliceLocation": {Counter(skipped_accession)}.')
    ds_sort = sorted(ds_list, reverse=True)
    res = 1
    for i in range(0, len(ds_sort) - 2):
        #print((ds_sort[i] - ds_sort[i + 1]), (ds_sort[i + 1] - ds_sort[i + 2]))
        if not abs(
            (ds_sort[i] - ds_sort[i + 1]) - (ds_sort[i + 1] - ds_sort[i + 2])
        ) < (ds_sort[0] - ds_sort[1]):
            res = 0
    return res


#dcm_slicedistance("/Users/sami/Desktop/test/")

def sliceDis_fold(fold_root, save_csv_path='slice_dist_check.csv'):
    """
    Arguments:
        - Root folder
        - Location and name to store CSV output
    Output csv file:
        - Instance number
        - If only one instance: single folder = 1 or 0 otherwise
        - distance_check: Output of `dcm_slicedistance` function calculated for each session
    """
    subj_list = [x.stem for x in Path(fold_root).iterdir() if x.is_dir()]
    sess, single_folder, diff = [], [], []
    for i in range(0, len(subj_list)):
        # if i > 3: break
        subj_path = Path(fold_root) / subj_list[i]
        sess_list = [x.stem for x in Path(subj_path).iterdir() if x.is_dir()]
        for j in range(len(sess_list)):
            sess.append(sess_list[j])
            #print("(i, j): ", i, j, sess_list[j])
            sess_path = subj_path / sess_list[j]
            instance_list = [x.stem for x in Path(sess_path).iterdir() if x.is_dir()]
            if len(instance_list) == 1:
                single_folder.append(1)
            else:
                single_folder.append(0)
            try:
                #same = dcm_slicedistance(sess_path + "/new_max/DICOM") # the DICOM files are under `new_max` and not `new_max/DICOM`
                same = dcm_slicedistance(sess_path / "new_max")
                diff.append(same)
            except:
                try:
                    same = dcm_slicedistance(sess_path / "file0/DICOM")
                    diff.append(same)
                except:
                    diff.append("")

                    print("dicom error")
    data = pd.DataFrame()
    data["sess"] = sess
    data["single_folder"] = single_folder
    data["distance_check"] = diff
    data.to_csv(save_csv_path, index=False)

sliceDis_fold("/Users/sami/Desktop/sample/")


def instanceN_fold(fold_root, save_csv_path="instance_num_check.csv"):  # instanceN_fold
    """
    Arguments:
        - Root folder
        - Location and name to store CSV output
    Output csv file:
        - instance number using header info
        - number of DICOM images for a particular session
        - difference b/w # of DICOM images and Instance number
            - Valid values are those <= 0 (?)
    """
    subj_list = [x.stem for x in Path(fold_root).iterdir() if x.is_dir()]
    sess, single_folder, instanceN, dicomN, diff = [], [], [], [], []
    for i in range(0, len(subj_list)):
        # if i > 30: break
        subj_path = Path(fold_root) / subj_list[i]
        sess_list = [x.stem for x in Path(subj_path).iterdir() if x.is_dir()]
        for j in range(len(sess_list)):
            sess.append(sess_list[j])
            # print("(i, j): ", i, j, sess_list[j])
            sess_path = subj_path / sess_list[j]
            instance_list = [x.stem for x in Path(sess_path).iterdir() if x.is_dir()]
            if len(instance_list) == 1:
                single_folder.append(1)
            else:
                single_folder.append(0)
            size_list = []
            for k in range(len(instance_list)):
                p = sess_path / instance_list[k]
                size_list.append(len(list(p.rglob("*.dcm"))))
                # print(sess_path / instance_list[k])
                # if (sess_path / instance_list[k] / "secondary").exists() and not (sess_path / instance_list[k] / "DICOM").exists():    # Unnecessary if not dealing with DICOM subdir
                #    (sess_path / instance_list[k] / "secondary").rename(sess_path / instance_list[k] / "DICOM")
                # size = len(os.listdir(sess_path + "/" + instance_list[k] + "/DICOM")) # There is no DICOM subdirectory, so this throws an error
                # size = len([x for x in  if x.is_dir()])
                # size_list.append(size)
            max_index = size_list.index(max(size_list))
            # break

            # Renames the dir with the greatest # of dcm image files
            (sess_path / instance_list[max_index]).rename(sess_path / "new_max")
            try:
                # inst_n, dicom_n, same = dcm_instance(sess_path + "/new_max/DICOM") # Again, there is no DICOM subdirectory, so this throws an error
                inst_n, dicom_n, same = dcm_instance(sess_path / "new_max")
                instanceN.append(inst_n)
                dicomN.append(dicom_n)
                diff.append(same)
            except:
                instanceN.append("")
                dicomN.append("")
                diff.append("")
                print("dicom error")
    data = pd.DataFrame()
    data["sess"] = sess
    data["single_folder"] = single_folder
    data["instanceN"] = instanceN
    data["dicomN"] = dicomN
    data["dicomN-instanceN"] = diff
    data.to_csv(save_csv_path, index=False)


# instanceN_fold("/Users/sami/Desktop/test/", "/Users/sami/Desktop/test/instance_num_check.csv")


def filter_few_slices(csv_path):
    """
    Filter to exclude sessions with few slices (less than 20) but that pass instance number check (dicomN - instanceN > 0).
    TODO: should we allow the thresholds to be user-definable parameters.
    """
    df = pd.read_csv(csv_path)
    auto_QA_result = []
    for i, item in df.iterrows():
        if item["dicomN-instanceN"] > 0 or item["instanceN"] < 20:
            auto_QA_result.append("bad")
        else:
            auto_QA_result.append("good")
    df["auto"] = auto_QA_result
    df.to_csv(csv_path, index=False)