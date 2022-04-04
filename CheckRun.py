
"""
Class CheckRundeckRun
moduleauthor:: 
:platform: Unix, Windows
:synopsis: Check if run is possible.

"""
import os
import psutil
import logging
import win32serviceutil
import time
import pywintypes


class CheckRundeckRun():

    def __init__(self):
        #self.date= time.
        self.os_type = os.name
        self.cwd = os.getcwd()
        self.drive = ['F',"D","C",""]
        self.root_win = ""
        self.root_ux = ""
        #prüfvariabeln is probe kann sysoparationen laufen.
        self.probe_root=None
        self.is_probe=None
        self.possiblerun=False
        #Services
        self.dict_srv = []
        self.dict_srv_curstate = []

    def colored(self,r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def used_drive(self):
        for d in self.drive:

            data=d+self.root_win
            path = os.path.exists(data)
            if path == True:
                self.is_probe=True
                self.probe_root = data
            else:
                self.is_probe = False
                self.probe_root= None
        self.isPossibleRun()

    def isPossibleRun(self):

        if self.is_probe == False:
            text = "You shall not pass \n No Probe found"
            self.possiblerun=False
            logging.warning(text)
            colored_text = self.colored(255, 0, 0, text)
            print(colored_text)
        elif self.is_probe == True:
            logging.info("Check was succesful !!")
            print("Check was succesful !!")
            self.possiblerun = True


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
                data = {"name": str(service['name']), "State": str(service['status'])}
                logging.info("Service found :" + str(data))
            except Exception as ex:
                print(ex)
                logging.warning(ex)
            self.dict_srv_curstate.append(data)
        return self.dict_srv_curstate











