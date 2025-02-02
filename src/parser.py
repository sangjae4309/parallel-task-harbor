import importlib
import random
from datetime import datetime

def ParseConfigure(config):
    # PATH
    path_dict_o     = {}
    path_list       = config.options('PATH')
    for path_name in path_list:
        path_dict_o[path_name] = config.get('PATH', path_name)

    # CMD_LIST
    cmd_dict_o      = {}
    cmd_list        = config.options('CMD_LIST')
    for cmd_n in cmd_list:
        cmd_dict_o[cmd_n] = {}
        cmd_params = config.get('CMD_LIST', cmd_n).split(' ')
        for i in range(len(cmd_params)):
            cmd_dict_o[cmd_n][cmd_params[i]] = 0  # init nothing

    # SIM_LIST
    sim_dict_o      = {}
    sim_list        = config.options('SIM_LIST')
    param_list      = config.get('CONFIG_OPT', '--sim_params').split(' ')
    for name_sim in sim_list:
        sim_dict_o[name_sim] = {} # dict in dict
        sim_params = config.get('SIM_LIST', name_sim).split(' ')
        print(f"Parsing {sim_params}")
        for i in range(len(sim_params)):
            sim_dict_o[name_sim][param_list[i]] = sim_params[i]

    # Dynamic import
    # TODO: what is happening? analyze under 2-lines
    remote_enable   = int(config.get('CONFIG_OPT', '--remote_enable'))
    pre_proc_str    = config.get('CONFIG_OPT', '--pre_proc')
    post_proc_str   = config.get('CONFIG_OPT', '--post_proc')
    PreProcessor    = getattr(importlib.import_module(pre_proc_str)
                     , 'PreProcessor')
    PostProcessor   = getattr(importlib.import_module(post_proc_str)
                     , 'PostProcessor')

    # Get current time to use it as a key
    time_obj = datetime.now()
    curr_key = time_obj.strftime('%Y%m%d_%H%M')
    # Append_mode list
    pre_proc_o      = PreProcessor(path_dict_o)
    post_proc_o     = PostProcessor(curr_key)   

    return [path_dict_o, cmd_dict_o, sim_dict_o,
            pre_proc_o, post_proc_o, remote_enable] 
