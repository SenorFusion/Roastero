# Standard Library Imports
import time, threading

# Local project imports
from ..tools.pid import *
from ..roaster_libraries.Recipe import Recipe

class Roaster:
    def __init__(self):
        self.currentTemp = 150      # Int in degrees Fahrenheit
        self.targetTemp = 0         # Int in degrees Fahrenheit
        self.sectionTime = 0        # Int in seconds
        self.totalTime = 0          # Int in seconds
        self.connected = False      # Determines if roaster is connected.
        self.p = 0.06
        self.i = 0.90
        self.d = 0.90

        # Thread control variables
        self.cont = True            # True or False, used to exit program
        self.threads = []           # A list used to keep track of threads

        # Recipe being used if not False
        self.recipe = False

    def run(self):
        # Start thread to communicate with the roasters serial connection.
        commThread = threading.Thread(target=self.comm, args=(1,))
        self.threads.append(commThread)
        commThread.daemon = True
        commThread.start()

        # Start thread to keep track of time.
        timerThread = threading.Thread(target=self.timer_thread, args=(2,))
        self.threads.append(timerThread)
        timerThread.setDaemon(True)
        timerThread.start()

        # Start a thread to control the thermostat of the roaster.
        thermostatThread = threading.Thread(target=self.thermostat_thread, args=(3,))
        self.threads.append(thermostatThread)
        thermostatThread.setDaemon(True)
        thermostatThread.start()

    def timer(self):
        # Count down during roast and cool phase.
        if(self.get_current_status() == 1 or self.get_current_status() == 2):
            time.sleep(1)
            self.totalTime += 1
            if(self.sectionTime > 0):
                self.sectionTime -= 1
            else:
                self.recipe.move_to_next_section()

        # When the roast is finished cooling, set roaster to idle.
        if(self.get_current_status() == 2 and self.sectionTime <= 0):
            self.idle()

    def set_section_time(self,time):
        self.sectionTime = time

    def get_section_time(self):
        return self.sectionTime

    def get_total_time(self):
        return self.totalTime

    def get_connection_status(self):
        return self.connected

    def timer_thread(self, threadNum):
        while(True):
            self.timer()

    def thermostat_thread(self, threadNum):
        self.p=PID(self.p, self.i, self.d)
        #p.setPoint(5.0)
        while(True):
            self.thermostat(self.p)

    def set_p(self, p):
        self.p.update_p(p)

    def set_i(self, i):
        self.p.update_i(i)

    def set_d(self, d):
        self.p.update_p(d)

    def set_total_time(self, time):
        self.totalTime = time

    def initialize(self):
        pass

    def get_current_temp(self):
        pass

    def get_target_temp(self):
        pass

    def set_target_temp(self):
        pass

    def idle(self):
        pass

    def get_current_status(self):
        pass

    def comm(self, threadNum):
        pass

    def thermostat(self):
        pass

    def pass_recipe_object(self, recipeObject):
        self.recipe = recipeObject

    def __del__(self):
        self.cont = False
        # self.threads[1].join()
