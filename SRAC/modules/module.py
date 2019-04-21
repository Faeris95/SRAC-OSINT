from SRAC.utility.utility import Colors


class Module():
    """
    Abstract Module class
    """

    def __init__(self, target, module_name):
        self.module_name = module_name
        self.target = target
        self.target_name = target.name
        self.data = {}

    def run_module(self, target):
        pass

    def load_previous(self):
        pass

    def srac_input(self, s="", prefix=""):
        print("%s" % s)
        if prefix:
            prefix = "[%s%s%s][%s%s%s]" % (Colors.G, self.target_name, Colors.N, Colors.B, prefix, Colors.N)
        choice = input("%s%s>>>%s " % (prefix, Colors.R, Colors.N))
        return choice

    def say_hello(self):
        print("%s module is scanning..." % (self.module_name))

    def say_goodbye(self):
        print("%s module is done" % (self.module_name))
