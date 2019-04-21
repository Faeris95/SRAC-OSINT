#!/usr/bin/python3

from SRAC.utility.utility import Colors
from SRAC.framework import Engine

from credentials import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret
from credentials import shodan_username, shodan_password


def banner():
    print("""
                    , 
                ,.  | \\ 
               |: \\ ; :\\ 
               :' ;\\| ::\\ 
                \\ : | `::\\ 
                _)  |   `:`. 
              ,' , `.    ;: ; 
            ,' ;:  ;"'  ,:: |_ 
           /,   ` .    ;::: |:`-.__ 
        _,' _o\\  ,::.`:' ;  ;   . ' 
    _,-'           `:.          ;""\\, 
 ,-'                     ,:         `-;, 
 \\,                       ;:           ;--._ 
  `.______,-,----._     ,' ;:        ,/ ,  ,` 
         / /,-';'  \\     ; `:      ,'/,::.::: 
       ,',;-'-'_,--;    ;   :.   ,',',;:::::: 
      ( /___,-'     `.     ;::,,'o/  ,::::::: 
       `'             )    ;:,'o /  ;"-   -:: 
                      \\__ _,'o ,'         ,:: 
                         ) `--'       ,..:::: 
      %s-S.R.A.C-%s          ; `.        ,::::::: 
                          ;  ``::.    ::::::: 
                          %sAnthony CHAFFOT
                          Sébastien ROLLAND%s\n""" % (Colors.R,Colors.N,Colors.B,Colors.N))


def check_cred():
    if twitter_access_token and twitter_access_token_secret and twitter_consumer_key and twitter_consumer_secret:
        print("%s[+] Twitter credentials%s" % (Colors.G, Colors.N))
    else:
        print("%s[-] No Twitter credentials%s" % (Colors.R, Colors.N))
    if shodan_password and shodan_username:
        print("%s[+] Shodan credentials%s" % (Colors.G, Colors.N))
    else:
        print("%s[-] No Shodan credentials%s" % (Colors.R, Colors.N))


def srac():
    banner()
    check_cred()
    g = input("1. New target\n2. Run the daily scan\n3. Exit S.R.A.C\n")
    if g != "1" and g != "2":
        exit()
    elif g == "1":
        Engine(True)
    elif g == "2":
        Engine(False)


if __name__ == '__main__':
    srac()
