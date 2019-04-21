from SRAC.target import Target
from SRAC.modules.twitter import Twitter
from SRAC.modules.theHarvester import theHarvester
from SRAC.utility.utility import Colors

import os
import subprocess


class Engine():
    """
    Implement the Engine logic
    """
    def __init__(self, new):
        if(new):
            self.target = Target(new)
        else:
            self.load_target()
        choice = 0
        while choice != "exit" or self.target.is_defined():
            choice = self.srac_input("", self.target)
            if choice == "help":
                self.help()
            elif choice == "show":
                if self.target.is_defined():
                    self.target.show_data()
                else:
                    print("You probably want to choose a target before asking for results..")
                    self.help()
            elif choice == "run":
                if not self.target.modules:
                    print("You have to load at least one module to run a scan")
                elif not self.target.is_new():
                    self.run_scan()
                elif self.target.is_defined():
                    if self.create_folder():
                        self.run_scan()
                else:
                    self.help_to_complete()
            elif "set" in choice:
                choice = choice.split(" ")
                if len(choice) < 3:
                    print("Not enough argument associated to %s" % (choice[0]))
                    continue
                if choice[1] == "domain":
                    self.target.add_domain(choice[2])
                else:
                    print("Unrecognized command associated to %s" % (choice[0]))
            elif choice == "exit":
                if self.target.is_defined():
                    self.target.remove()
                    choice = ""
            elif "load" in choice:
                if not self.target.is_new():
                    print("You can't load more module for an existant target")
                else:
                    choice = choice.split(" ")
                    if len(choice) > 1:
                        if choice[1] == "all":
                            self.target.add_module("theHarvester")
                            self.target.add_module("Twitter")
                        elif choice[1].lower() == "theharvester":
                            self.target.add_module("theHarvester")
                        elif choice[1].lower() == "twitter":
                            self.target.add_module("Twitter")
                        else:
                            print("Unrecognized module")
                    else:
                        print(" - theHarvester : hosts, IPs and mails discovering")
                        print(" - Twitter : 5 more significant Twitter accounts")
                        print(" - all : load all available modules")
            else:
                print("Unrecognized command")

    def create_folder(self):
        if not os.path.isdir(os.path.realpath(__file__)[:-9] + "data"):
            subprocess.call(["mkdir", os.path.realpath(__file__)[:-9] + "data"])
        if not os.path.isdir(self.target.get_path()):
            subprocess.call(["mkdir", self.target.get_path()], stderr=True)
        else:
            clean = self.srac_input("%s already exists, should I replace it ? (y/n)" % self.target.domain, self.target.name)
            if clean.lower() == 'y':
                subprocess.call(["rm", "-rf", self.target.get_path()])
                subprocess.call(["mkdir", self.target.get_path()], stderr=True)
            else:
                print("You probably want to do a daily scan then (choice n°2)")
                return 0
        return 1

    def load_target(self):
        path = os.path.realpath(__file__)
        path = path[:-13]
        results = subprocess.check_output(["ls", path+"/data/"]).decode("utf-8").rstrip("\n").split("\n")
        i = 1
        for result in results:
            print("[%s]%s>>>%s %s" % (i, Colors.B, Colors.N, result))
            i += 1
        nb = self.srac_input("")
        self.target = Target(False, results[int(nb)-1])
        results = subprocess.check_output(["ls", path+"/data/"+self.target.domain+"/"]).decode("utf-8").rstrip("\n").split("\n")
        results = [x.replace("OriginalData.xml", "") for x in results if "OriginalData" in x]
        self.target.add_module(list(x for x in results))

    def srac_input(self, s="", prefix=""):
        if(s):
            print("%s" % s)
        if(prefix):
            prefix = "[%s%s%s]" % (Colors.G, prefix, Colors.N)
        choice = input("%s%s>>>%s " % (prefix, Colors.R, Colors.N))
        return choice

    def define_target(self):
        p = self.srac_input("1. Moral entity\n2. Physical entity")
        if p == "1":
            self.target = Target(self.srac_input("Add a domain name"))

    def run_scan(self):
        print("Run scan on %s .. \n" % (self.target))
        for mod in self.target.modules:
            exec(mod)
        print("%s[+]Files are saved in %s%s" % (Colors.G, self.target.get_path(), Colors.N))

    def help(self):
        print("help : print this help message\nrun : run the scan")
        print("set")
        print(" - domain : change the domain name")
        print("show : results")
        print("load")
        print(" - theHarvester : hosts, IPs and mails discovering")
        print(" - Twitter : 5 more significant Twitter accounts")
        print(" - all : load all available modules")
        print("exit : return to main menu")

    def help_to_complete(self):
        print("set domain [domain_name]")



