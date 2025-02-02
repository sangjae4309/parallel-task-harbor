# Parallel-Task-Harbor
Parallel-Task-Harbor is a Python-based parallel task automation tool designed to simplify the simulation of hundreds or thousands of different tasks simultaneously. 
It monitors server or workstation resources and dynamically allocates workloads to the least loaded system.

![Image](https://github.com/user-attachments/assets/8c1a3742-a061-4be0-8452-c8647af32138)

## Getting Started
Running this tool requires only `python3`.
```
apt-get install python3
```
Use your own configuration file. The example below is for reference; modify it to suit your specific workload.
```
python3 main.py -c sim_config/local_mat_mul.cfg
```

## Configuration File
The configuration is largely composed of 5 different parts.
- `[PATH]`: Specify the absolute path where parallel tasks will be executed, along with the temporary folder that will be duplicated for multiple cases.
- `[CONFIG_OPT]`: Set up different options.
- `[RESOURCE]`: Set up system's limitation and configurations
- `[CMD_LIST]`: Commands to be executed automatically
- `[SIM_LIST]`: List all the simulation cases you want to run

Let's deep dive into detail with an example script.<p>
<img width="412" alt="Image" src="https://github.com/user-attachments/assets/63f62442-039e-4361-8983-02c16cacbddb"/>
- `--remote_enable`: remote is enbaled so that the command is distributed across differnt servers thorugh `ssh` commands.
- `--sim_params`: It takes 2 argument from each item of `SIM_LIST`.
- `--pre_proc`, `--post-proc`: use a script located at `src/pre_proc/simple_mat_mul.py` as pre-processor and that of post-processor.

Rather than trying to understand everything at once, run the example and observe its behavior.


## Code Architecture
<img width="758" alt="Image" src="https://github.com/user-attachments/assets/6608ca78-88ad-4d07-8cea-0c8cdc258d12" /> <p>
The red-highlighted script can be replaced with the user's desired script. And redirect it by specifying in `--pre_proc` and `--post_proc` options.
