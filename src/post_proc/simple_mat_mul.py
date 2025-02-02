import fcntl
import os
import shutil
import time

class PostProcessor(object):
    def __init__(self, currkey):
        self.name = "post-processor of DR Sim"
        self.currkey = currkey

    def postProcess(self, req_i):
        base_path       = req_i.getValue('BASE_PATH')
        target_dir      = req_i.getValue('TARGET_DIR')

        # Do what you want
        # e.g, mv file, remove file, extract data etc....
        f_result = open(f"{target_dir}/run.log", "r")
        data = f_result.readline()
        filename = f"{base_path}/mat_mul_{self.currkey}.log"
        with open(filename, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # Acquire exclusive lock
            #print("Lock acquired, writing...")
            f.write(data + "\n")
            time.sleep(2)  # Simulating long write operation
            fcntl.flock(f, fcntl.LOCK_UN)  # Release lock
            #print("Lock released.")
