#!/home/sangjae.park/local/bin/python3.6                                                                                                                                                                                          
import time
import os
import shutil
import glob
import subprocess

from datetime import datetime

NORMAL_EXIT_CODE    = 0
TERMINATE_CODE      = 1
COMMAND_NOT_FOUND_CODE  = 127

class ProcessorLocal(object):
   def __init__(self, cmd_dict_i, config_i, post_proc_i):
      self.cmd_dict       = cmd_dict_i
      self.post_proc      = post_proc_i
    
      # Gen. server managing table
      self.server_subproc   = []
      self.server_req       = []
      self.max_core = config_i.get('LOCAL', 'MAX_CORE')
    
   def getIdle(self):
      while True:
         cur_running = len(self.server_subproc)
         if cur_running < int(self.max_core):
            return 0
         else:
            time.sleep(1)
            self.stripCompleteWork()
    

   def stripCompleteWork(self):
      # Strip complete work
      for idx, subproc in enumerate(self.server_subproc):
        proc_status = subproc.poll()
        if proc_status != None:
            subproc_pop = self.server_subproc.pop(idx)
            req_pop     = self.server_req.pop(idx)
            self.post_proc.postProcess(req_pop)
            subproc_pop.kill() # kill subprocess
            if proc_status == NORMAL_EXIT_CODE:
                print(f"\nSuccessfully Done {req_pop.getValue('REQ_NAME')}")
            elif proc_status == TERMINATE_CODE:
                print(f"\nTerminate {req_pop.getValue('REQ_NAME')}")
            elif proc_status == COMMAND_NOT_FOUND_CODE:
                print(f"\nCommand not found for {req_pop.getValue('REQ_NAME')}")
    
    
   def addNewWork(self, sub_proc_i, req_i):
      self.server_subproc.append(sub_proc_i)
      self.server_req.append(req_i)
    
   def printServerStatus(self):
      for subproc in self.server_subproc:
         print(f"{subproc.pid}({subproc.poll()}) ", end='')
      print('')

   def runReq(self, req_i):    
      req_cmd     = req_i.getCommand(self.cmd_dict)
      #req_cmd     += '&'

      p = subprocess.Popen(req_cmd,
                     shell=True,
                     executable='/bin/bash',
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     bufsize=-1)

      self.addNewWork(p, req_i)
      print(f"Local PC executes \"{req_cmd}\"")

      self.printServerStatus()
      time.sleep(1)

   def waitSubProc(self):
      print("[Processor] Waiting running sub-procs....")
      while True:
         n_running=0
         self.stripCompleteWork()
         n_running += len(self.server_subproc)
         if n_running == 0:
            break
         else:
            time.sleep(5)
