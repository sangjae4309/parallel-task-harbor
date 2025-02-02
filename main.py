## Built-in Pacakges
import time
import argparse
import configparser
import datetime
import subprocess

## local defined packages
from src import ParseConfigure, Request, ProcessorLocal, ProcessorRemote


# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
            description='Parallel Task Management')
    parser.add_argument('-c', '--configfile', action='store',
                    dest='configfile', help=' configuration file')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(args.configfile)

    parse_conf_o = ParseConfigure(config)
    path_dict   = parse_conf_o[0]
    cmd_dict    = parse_conf_o[1]
    sim_dict    = parse_conf_o[2]
    pre_proc    = parse_conf_o[3]
    post_proc   = parse_conf_o[4]
    remote_enable = parse_conf_o[5]

    processor = None
    if remote_enable:
        processor = ProcessorRemote(cmd_dict, config, post_proc) 
    else:
        processor = ProcessorLocal(cmd_dict, config, post_proc) 

    # StepX. generate request instances
    for t_test in sim_dict:
        pre_proc.generateRequest(t_test, sim_dict[t_test])

    i=0
    total_nreq = pre_proc.getReqNum()
    while True:
        n_req = pre_proc.getReqNum()
        if n_req==0: break
        req_tmp = pre_proc.pullRequest()
        if remote_enable:
            server_n = processor.getIdleServer();
            pre_proc.modifyPrior(req_tmp)
            processor.runReq(req_tmp, server_n)
        else:
            processor.getIdle(); # locker
            pre_proc.modifyPrior(req_tmp)
            processor.runReq(req_tmp)
        i+=1
        print(f"{i}/{total_nreq}")
    processor.waitSubProc() # wait all subprocesses to be ended

if __name__ == "__main__":
    main()
