from abc import *
import os
                                               
##  
class AbstractPreProcessor(metaclass=ABCMeta):
    def __init__(self):                                  
        self.base_path  = ""
        self.req_buffer = []
                                                        
    @abstractmethod
    def generateRequest(self, t_test, sim_dict):       
        return 0
    
    @abstractmethod
    def modifyPrior(self, req_i):
        return 0
    
    def getReqNum(self):
        return len(self.req_buffer)
                                   
    def pushRequest(self, req_i):
        self.req_buffer.append(req_i)
                                         
    def pullRequest(self):        
        return self.req_buffer.pop(0)
                                                
    # protected method                         
    def _removeOlder(self, folder_name):                 
        if os.path.isdir(folder_name):                 
            print(f"removing existing {folder_name}")  
            os.system(f"rm -rf {folder_name}")

    def _makeDir_no_rm(self, folder_name):      
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)        
            return True     
        return False
                          
    def _makeDir(self, folder_name):         
        if os.path.isdir(folder_name):      
            print(f"[cmd] rm -rf the exsiting {folder_name}")
            os.system(f"rm -rf {folder_name}")      
        os.mkdir(folder_name)
