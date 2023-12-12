import concurrent.futures
import multiprocessing
import os
cpu_cores = multiprocessing.cpu_count()
def run_command(command):
    os.system(command)
    return

with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
    for auto_by in os.listdir('auto_by'):
            future= executor.submit(run_command,'python auto_by/'+auto_by)
            print('running ' + auto_by)
