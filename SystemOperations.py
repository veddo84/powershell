
import os
import psutil
import logging
import win32serviceutil
import time
import pywintypes
from classes.CheckRun import CheckRundeckRun

import requests
class SystemOperations(CheckRundeckRun):
    """
    Class: CheckRundeckRun
    moduleauthor:
    :platform: Unix, Windows
    :synopsis: System oparations context probe.
    """


    def __init__(self,check):
        self.klass = "SystemOperations"a
        self.dict_srv = check.dict_srv
        self.os_type = check.os_type
        self.root_win = check.root_win
        self.probe_root = check.probe_root
        self.possiblerun = check.possiblerun
        self.dict_srv_curstate = []
        #Eigene Variablen
        self.rndk_root=[]
        self.folder_list=[]




    def win_StopService(self):
        """Stopping win Services. dict_srv can be overwritten.

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
        dict_srv can be overwritten
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

    def create_rndk_root(self):
        """Creates rundeck root folder used later for script operation

        :param : NO
        :type
        :returns:  None
        :raises: OSError
        """

        for i in self.rndk_root:
            print(i)
            try:
                os.mkdir(i)
            except OSError as er:
                logging.warning(er)
            else:
                print("Successfully created the directory %s " % i)
                logging.info("Successfully created the directory %s " % i)

    def download_url(self,url, name):

        """Download files from Internet Save in C:/rundeck/tmp

        :param Url http where file can be downloaded
        :type String
        :param name Name of file that will be downloaded
        :returns:  None
        :raises: requests.HTTPError
        """
        try:
            r = requests.get(url, stream=True)
            with open("C:/rundeck_/tmp/"+str(name), 'wb') as fd:
                fd.write(r.content)
        except requests.HTTPError as er :
            print(er)
            logging.warning(er)


    def list_path(self,path):
        """Lists everything in a folder

        :param path to a Directory
        :type String
        :raises: OSError
        """
        #print("|----------------------- LIST ---------------------|")
        t=os.listdir(str(path))
        self.folder_list.append(t)
        #print(t)
        for i in t:
            t = os.path.getsize(path+"/"+i)
            #print(t)
