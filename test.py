
"""
Class SystemOparations
moduleauthor:: 
:platform: Unix, Windows
:synopsis: System oparations context probe.

"""
import os
import psutil
import logging
import win32serviceutil
import time
import pywintypes

class SystemOperations():

    def __init__(self):
        self.os_type = os.name
        self.cwd = os.getcwd()
        self.root_win = ":"
        self.root_ux = ":"
        self.dict_srv = []
        self.dict_srv_curstate = []




    def win_checkServiceisRunning(self):
        """This function does something.

            :param deactiveate: Stop List of services True
            :type name: bool.
            :param state: false.
            :type state: bool.
            :returns:  Status name of services.
            :raises: Exception, Exception

            """

        for i in self.dict_srv:
            try:
                service = psutil.win_service_get(i)
                service = service.as_dict()
                data = {"name":str(service['name']),"State": str(service['status'])}
                logging.info("Service found :"+str(data))
            except Exception as ex:
                print(ex)
                logging.warning(ex)
            self.dict_srv_curstate.append(data)
        return self.dict_srv_curstate



    def win_StopService(self):
        """Stopping win Services.

                    :param : self Param  dict_srv
                    :type dict_srv: dict.
                    :returns:  Status (Stopped of services listed at dict_srv.
                    :raises: Exception, Exception

                    """

        for i in self.dict_srv:
            print(i)
            try:
                win32serviceutil.StopService(i)
                time.sleep(5)
                self.win_checkServiceisRunning()
                logging.info("Stopping Service " + str(i))
            except pywintypes.error as ex:
                print(ex)
                logging.warning(ex)

    def win_StartService(self):
        """Starting win Services list itaration backwards.
         :param : self Param  dict_srv
         :type dict_srv: dict.
         :returns:  Status (of services listed at dict_srv.
         :raises: Exception, Exception
         """

        for i in reversed(self.dict_srv):
            try:
                win32serviceutil.StartService(i)

                logging.info("Starting Service "+str(i))
                time.sleep(5)
                self.win_checkServiceisRunning()
            except pywintypes.error as ex:
                print(ex)
                logging.warning(ex)







