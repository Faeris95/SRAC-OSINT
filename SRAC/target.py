import re
import os

from SRAC.utility.utility import Colors


class BadNameException(Exception):
    pass


class Target():
    def __init__(self, new, domain=None):
        self.new = new
        self.path = ""
        self.modules = []
        self.data = {}
        if new:
            self.defined = False
            self.domain = ""
            self.name = ""
        else:
            if not domain:
                raise BadNameException
            self.add_domain(domain)
            self.load_data()
        
    def __str__(self):
        return self.name

    def add_domain(self, domain):
        regex = re.search(r"(([a-z]+)\.([a-z]+)$)", domain)
        if regex:
            self.domain = regex.group(1)
            self.name = regex.group(2)
            self.defined = True
            self.load_data()
        else:
            print("set domain require a domain name")

    def remove(self):
        self.domain = ""
        self.name = ""
        self.data = {}
        self.path = ""
        self.defined = False

    def is_defined(self):
        return self.defined

    def is_new(self):
        return self.new

    def load_data(self):
        self.path = os.path.realpath(__file__)[:-9] + "data/" + self.domain +"/"

    def add_module(self, module):
        if type(module) == list or type(module) == tuple:
            for mod in module:
                self.modules.append(mod+"(self.target)")
                print("[+] %s module is loaded" % (mod))
        else:
            self.modules.append(module+"(self.target)")
            print("[+] %s module is loaded" % (module))

    def get_path(self):
        return self.path

    def set_data(self, data, module):
        self.data[module] = data

    def get_data(self):
        return self.data

    def show_data(self):
        if not self.data:
            print("Nothing to show yet")
            return
        if self.new:
            for item in self.data:
                dataTmp = self.data[item]
                print("%s ### [%s] ###%s" % (Colors.B, item, Colors.N))
                for it in dataTmp:
                    print("  ### [%s] ###" % (it))
                    if type(dataTmp[it]) == list:
                        if not dataTmp[it]:
                            print("   None")
                        for i in dataTmp[it]:
                            print("   [+] %s" % (i))
                    else:
                        if not dataTmp[it]:
                            print("   None")
                        for i in dataTmp[it]:
                            print("   [+] %s:%s" % (i, dataTmp[it][i]))
        else:
            for item in self.data:
                dataTmp = self.data[item]
                print("%s ### [%s] ###%s" % (Colors.B, item, Colors.N))
                for state in dataTmp:
                    if state == "new":
                        for it in dataTmp[state]:
                            print("  ### [New %s] ###" % (it))
                            if type(dataTmp[state][it]) == list:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[+] %s%s" % (Colors.G, i, Colors.N))
                            else:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[+] %s:%s%s" % (Colors.G, i, dataTmp[state][it][i], Colors.N))
                    elif state == "unchanged":
                        for it in dataTmp[state]:
                            print("  ### [Unchanged %s] ###" % (it))
                            if type(dataTmp[state][it]) == list:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[X] %s%s" % (Colors.N, i, Colors.N))
                            else:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[X] %s:%s%s" % (Colors.N, i, dataTmp[state][it][i], Colors.N))
                    elif state == "removed":
                        for it in dataTmp[state]:
                            print("  ### [Removed %s] ###" % (it))
                            if type(dataTmp[state][it]) == list:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[-] %s%s" % (Colors.R, i, Colors.N))
                            else:
                                if not dataTmp[state][it]:
                                    print("   None")
                                for i in dataTmp[state][it]:
                                    print("   %s[-] %s:%s%s" % (Colors.R, i, dataTmp[state][it][i], Colors.N))
