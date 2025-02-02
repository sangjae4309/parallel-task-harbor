import time
import os
import shutil
import glob
import subprocess
  
from datetime import datetime
  
NORMAL_EXIT_CODE   = 0
SSH_EXIT_CODE   = 255


class ProcessorRemote(object):
    def __init__(self, cmd_dict_i, config_i, post_proc_i):
        self.cmd_dict       = cmd_dict_i
        self.post_proc      = post_proc_i

        # Gen. server managing table
        self.server_subproc = {}
        self.server_req     = {}
        self.server_limit   = {}
        self.server_user_name = {}
        self.server_port    = {}
        server_list = config_i.options('SERVER_LIST')
        for server_n in server_list:
            server_conf = config_i.get('SERVER_LIST', server_n).split(' ')
            self.server_limit[server_n]     = server_conf[0]
            self.server_user_name[server_n] = server_conf[1]
            self.server_port[server_n]      = server_conf[2]
        for server_n in server_list:
            self.server_subproc[server_n]   = []
            self.server_req[server_n]       = []

    def getIdleServer(self):
        # Return the least loaded server
        while True:
            ready_server_list = []
            for server in self.server_subproc:
                cur_running = len(self.server_subproc[server])
                if cur_running < int(self.server_limit[server]):
                    ready_server_list.append(server)
            if len(ready_server_list) == 0:
                # All server is fully working
                time.sleep(1)
                self.stripCompleteWork()
            else:
                min_load=100
                min_server=-1
                for server in ready_server_list:
                    cur_running = len(self.server_subproc[server])
                    if cur_running < min_load:
                        min_load = cur_running
                        min_server = server
                        return min_server


    def stripCompleteWork(self):
        # Strip complete work
        for key in self.server_subproc:
            for idx, subproc in enumerate(self.server_subproc[key]):
                #print(f"{key}: {subproc.poll}")
                proc_status = subproc.poll()
                if proc_status != None:
                    subproc_pop = self.server_subproc[key].pop(idx)
                    req_pop     = self.server_req[key].pop(idx)
                    self.post_proc.postProcess(req_pop)
                    subproc_pop.kill() # kill subprocess
                    if proc_status == NORMAL_EXIT_CODE:
                        print(f"\nSuccessfully Done {req_pop.getValue('REQ_NAME')}")
                    elif proc_status == SSH_EXIT_CODE:
                        print(f"\nssh connect fail for {req_pop.getValue('REQ_NAME')}")

    def addNewWork(self, server_n, sub_proc_i, req_i):
        self.server_subproc[server_n].append(sub_proc_i)
        self.server_req[server_n].append(req_i)
  
    def printServerStatus(self):
        for key in self.server_subproc:   
            print(key, end=': ')
            for subproc in self.server_subproc[key]:
                print(f"{subproc.pid}({subproc.poll()}) ", end='')
            print('')

    def runReq(self, req_i, server_n):    
        req_cmd     = req_i.getSSHCommand(self.cmd_dict)
        req_cmd     += '&'

        user_name   = self.server_user_name[server_n]
        server_port = self.server_port[server_n]
        p = subprocess.Popen(["ssh",
                        f"{user_name}@{server_n} -p{server_port}",
                        req_cmd],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        bufsize=0)

        self.addNewWork(server_n, p, req_i)
        print(f"{user_name}@{server_n} -p{server_port} \"{req_cmd}\"")

        self.printServerStatus()
        time.sleep(1)    

    def waitSubProc(self):
        print("[Processor] Waiting running sub-procs....")
        while True:
            n_running=0
            self.stripCompleteWork()
            for key in self.server_subproc:
                n_running += len(self.server_subproc[key])
            if n_running == 0:
                break
            else:
                time.sleep(5)
