from SRAC.modules.module import Module
import os
import subprocess
from SRAC.utility.utility import Colors
from datetime import datetime
from lxml import etree

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


class theHarvester(Module):
    def __init__(self, target):
        super().__init__(target, "theHarvester")
        self.path = ""
        self.say_hello()

        self.target = target
        self.loadTheHarvester()
        self.load_results(self.run_module())
        self.say_goodbye()

    def loadTheHarvester(self):
        self.path = os.path.realpath(__file__)
        self.path = self.path[:-3]

    def run_module(self):
        pathToFile = ''
        if not os.path.isfile(self.target.get_path()+"theHarvesterOriginalData.xml"):
            pathToFile = self.target.get_path() + "theHarvesterOriginalData.xml"
            subprocess.call([self.path + "/theHarvester.py", "-d", self.target.domain, "-b", "google", "-l", "500", "-f", pathToFile], stdout=DEVNULL, cwd=self.path)
        else:
            pathToFile = self.target.get_path() + datetime.now().strftime("%d-%m-%y") + "-theHarvester.xml"
            if os.path.isfile(pathToFile):
                subprocess.call(["rm", "-f", pathToFile])
            subprocess.call([self.path + "/theHarvester.py", "-d", self.target.domain, "-b", "google", "-l", "500", "-f", pathToFile], stdout=DEVNULL, cwd=self.path)
        print(Colors.N, end='')
        return pathToFile

    def load_results(self, pathToFile):
        otree = etree.parse(self.target.get_path() + "theHarvesterOriginalData.xml")
        odata = {}
        omails = []
        ohosts = {}

        for mail in otree.xpath("/theHarvester/email"):
            omails.append(mail.text)

        odata['mails'] = omails

        for host in otree.xpath("/theHarvester/host"):
            ohosts[host.getchildren()[0].text] = host.getchildren()[1].text

        odata['hosts'] = ohosts

        if self.target.is_new():
            self.target.set_data(odata, "theHarvester")
        else:
            otree = etree.parse(pathToFile)
            data = {}
            newMails = []
            newHosts = {}
            nmails = []
            removedMails = []
            removedHosts = {}
            unchangedHosts = {}
            unchangedMails = []
            nhosts = {}
            tree = etree.parse(pathToFile)

            for mail in tree.xpath("/theHarvester/email"):
                nmails.append(mail.text)

            for host in otree.xpath("/theHarvester/host"):
                nhosts[host.getchildren()[0].text] = host.getchildren()[1].text

            for mail in nmails:
                if mail in omails:
                    unchangedMails.append(mail)
                else:
                    newMails.append(mail)

            for mail in omails:
                if mail not in nmails:
                    removedMails.append(mail)

            for host in nhosts:
                if host in ohosts:
                    unchangedHosts[host] = nhosts[host]
                else:
                    newHosts[host] = nhosts[host]

            for host in ohosts:
                if host not in nhosts:
                    removedHosts[host] = ohosts[host]

            data = {
                    "new": {"hosts": newHosts,
                            "mails": newMails},
                    "unchanged": {"hosts": unchangedHosts,
                                  "mails": unchangedMails},
                    "removed": {"hosts": removedHosts,
                                "mails": removedMails}
                    }
            self.target.set_data(data, "theHarvester")
