import threading
import os
import settings as settings

def run_command(command):
    os.system(command)
    return

# create a settings object
settings = settings.settings()
# initialize the settings object
settings.init()

current_directory = os.path.dirname(os.path.realpath(__file__))
upload_thread = threading.Thread(target=settings.upload_loop)
upload_thread.start()
for auto_by in os.listdir(current_directory + '\\auto_by'):
        if "auto_by" in auto_by and "image" in auto_by:
            # pass a reference to the settings object to the auto_by script so the auto_by script can pass values back to the settings object
            threading.Thread(target=run_command, args=('python ' + current_directory + '\\auto_by\\' + auto_by + ' ' + str(settings),)).start()
            print('running ' + auto_by)


