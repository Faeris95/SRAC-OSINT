from SRAC.modules.module import Module
from SRAC.utility.utility import Colors
import tweepy
import os
import subprocess
from datetime import datetime
from credentials import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret
from lxml import etree


class Twitter(Module):
    def __init__(self, target):
        super().__init__(target, "Twitter")
        self.say_hello()
        if self.twitter_auth():
            self.run_module()
        self.target = target
        self.say_goodbye()

    def twitter_auth(self):
        if twitter_consumer_key and twitter_consumer_secret and twitter_access_token and twitter_access_token_secret:
            try:
                auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
                auth.set_access_token(twitter_access_token, twitter_access_token_secret)
                self.api = tweepy.API(auth, wait_on_rate_limit=True)
            except tweepy.TweepError as err:
                print("%s%s : %s%s " % (Colors.R, err.message[0]['code'], err.message[0]['message'], Colors.N))
                print("%s[-]Skipping Twitter module%s" % (Colors.O, Colors.N))
            finally:
                return True
        else:
            return False

    def search_name(self):
        returned_names = []
        names = self.api.search_users(q=self.target_name, per_page=5, page=1)
        for i in range(0, 5):
            returned_names.append(names[i].screen_name)
        return returned_names

    def run_module(self):
        names = self.search_name()
        old_account = []
        pathToFile = ''
        if not os.path.isfile(self.target.get_path()+"TwitterOriginalData.xml"):
            pathToFile = self.target.get_path()+"TwitterOriginalData.xml"
            with open(pathToFile, 'w') as twitFile:
                twitFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                twitFile.write("""
                    <Twitter>
                    <Accounts>
                    """)
                for name in names:
                    twitFile.write("<name>%s</name>" % (name))
                twitFile.write("""
                    </Accounts>
                    </Twitter>""")
            data = {"Accounts": names}
            self.target.set_data(data, "Twitter")

        else:
            new_accounts = []
            removed_accounts = []
            unchanged_accounts = []

            pathToFile = self.target.get_path() + datetime.now().strftime("%d-%m-%y") + "-Twitter.xml"
            if os.path.isfile(pathToFile):
                subprocess.call(["rm", "-f", pathToFile])
            otree = etree.parse(self.target.get_path() + "TwitterOriginalData.xml")
            for account in otree.xpath("/Twitter/Accounts/name"):
                old_account.append(account.text)
            for a in names:
                if a in old_account:
                    unchanged_accounts.append(a)
                else:
                    new_accounts.append(a)
            for o in old_account:
                if o not in names:
                    removed_accounts.append(o)
            data = {"new": {"Accounts": new_accounts},
                    "unchanged": {"Accounts": unchanged_accounts},
                    "removed": {"Accounts": removed_accounts}}
            with open(pathToFile, 'w') as twitFile:
                twitFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                twitFile.write("<Twitter>")
                for name in names:
                    twitFile.write("<name>%s</name>" % (name))
                twitFile.write("</Twitter>")
            self.target.set_data(data, "Twitter")
