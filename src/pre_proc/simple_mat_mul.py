import os
import sys  
import glob 

sys.path.append("../../")
from src import Request
from src.pre_proc.preprocessor import AbstractPreProcessor


class PreProcessor(AbstractPreProcessor):
    def __init__(self, path_dict):
        super().__init__()
        self.base_path  = path_dict['BASE_PATH']
        self.tmp_path   = path_dict['BASE_TMP']


    def generateRequest(self, t_test, sim_dict):
        base_req_name   = ""
        req_dict        = sim_dict.copy()
        cp_dict         = {}

        # check multi_idx
        req_dict['BASE_PATH']= self.base_path
        req_dict['BASE_TMP'] = self.tmp_path
        cp_dict['BASE_TMP']  = f"{self.tmp_path}/*"

        req_dict['REQ_NAME']    = f"{t_test}"
        req_dict['TARGET_SCENARIO'] = f"{t_test}"
        req_dict['TARGET_DIR']  = f"{self.base_path}/tmp_{t_test}"
        req = Request(req_dict, cp_dict)
        self.pushRequest(req)

    def modifyPrior(self, req_i):
        # Step0. make temporary folder
        target_dir = req_i.getValue('TARGET_DIR')
        os.chdir(self.base_path)
        self._removeOlder(target_dir) # remove older folder
        self.__makeNewDir(target_dir)

        # Step1. copy necessary files
        for key in req_i.getCopyDict():
            cp_ptn = req_i.getCopyValue(key)
            os.system(f"cp -r {cp_ptn} {target_dir}")

    def __makeNewDir(self, folder_name):
        if os.path.isdir(folder_name):
            print(f"[cmd] rm -rf the exsiting {folder_name}")
            os.system(f"rm -rf {folder_name}")
        print(f"mkdir {folder_name}")
        os.mkdir(folder_name)  
