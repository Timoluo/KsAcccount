import os
import psutil

def get_all_pid_name():
    pids = psutil.pids()
    print(os.name)
    for pid in pids:
        p = psutil.Process(pid)
        print('pid-%s,pname-%s' % (pid, p.name()))

def get_pid_from_name(pname):
    namelist=[]
    pids = psutil.pids()
    #print(os.name)
    for pid in pids:
        p = psutil.Process(pid)
        if p.name()==pname:
            print('pid-%s,pname-%s' % (pid, p.name()))
            namelist.append(pid)
    return namelist

    
def kill(pid):
    # 本函数用于中止传入pid所对应的进程
    if os.name == 'nt':
        # Windows系统
        cmd = 'taskkill /pid ' + str(pid) + ' /f'
        try:
            os.system(cmd)
            print(pid, 'successfully killed')
        except Exception as e:
            print(e)
    elif os.name == 'posix':
        # Linux系统
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print(pid, 'successfully killed')
        except Exception as e:
            print(e)
    else:
        print('Undefined os.name')
        pass