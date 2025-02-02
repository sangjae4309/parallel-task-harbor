import os 

class Request(object):
    def __init__(self, req_dict_i, cp_dict_i):
        self.req_dict       = req_dict_i.copy()
        self.cp_dict        = cp_dict_i.copy()

    def getValue(self, key):
        if key not in self.req_dict:
            return 'N'
        return self.req_dict[key]

    def getCopyDict(self):
        return self.cp_dict

    def getCopyValue(self, key):
        return self.cp_dict[key]

    def getCommand(self, cmd_dict):
        cmd_dict_l = cmd_dict.copy()

        cmd = f"cd {self.getValue('TARGET_DIR')}"
        for cmd_key in cmd_dict:
            cmd += " &&"
            for arg_key in cmd_dict[cmd_key]:
                if arg_key in self.req_dict:
                    cmd_dict[cmd_key][arg_key] = self.getValue(arg_key)
                else:
                    cmd_dict[cmd_key][arg_key] = arg_key
                cmd += f" {cmd_dict[cmd_key][arg_key]}"
        #cmd += " exit;"
        return cmd

    def getSSHCommand(self, cmd_dict):
        cmd_dict_l = cmd_dict.copy()
        cmd = f"cd {self.getValue('TARGET_DIR')} &&"
        for cmd_key in cmd_dict:
            for arg_key in cmd_dict[cmd_key]:
                if arg_key in self.req_dict:
                    cmd_dict[cmd_key][arg_key] = self.getValue(arg_key)
                else:
                    cmd_dict[cmd_key][arg_key] = arg_key
                cmd += f" {cmd_dict[cmd_key][arg_key]}"
            cmd += " &&"
        cmd += " exit;"
        return cmd
