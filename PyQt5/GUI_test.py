import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from instapy import InstaPy
import random
from ast import literal_eval
import re


# TODO disable all bottom when one activity is on
# TODO change save profile in SQL server
# TODO open firefox in GUI
# TODO show logs in GUI
# TODO get amount from user
# TODO need to make work with server >>>server side need to add <<<

# make all activity work form server side
# profile page need some change (get amount from user and more info)

# I Pick This Project To Learn QT and more Python
# to use this bot you need install instapy lib
# pip install instapy
# firefox and geckodriver is need to
# do not user your main instagram account some time instagram block you


# RE for username
# (?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)
# RE for hashtags
# (?:#)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)
# do_like make 10 for ea 1 amount


class Bot(QMainWindow):

    def __init__(self):
        super(Bot, self).__init__()
        self.dont_like = []
        self.ignore_list = []
        self.friend_list = []
        self.tags_list = []
        self.target_list = []
        self.Business_Target_list = []
        self.comments_list = []
        self.amount_like = None
        self.amount_follow = None
        self.amount_unfollow = None
        self.amount_mix = None

        self.session = None
        self.MainPage = loadUi("GuiQt/mainpage.ui")
        self.profile = loadUi("GuiQt/profile.ui")
        self.login_Page = loadUi("GuiQt/login.ui")
        self.live_Report = loadUi("GuiQt/LiveReport.ui")
        self.amount_page = loadUi("GuiQt/amount.ui")
        self.MainPage.show()
        self.bot_buttons()

    """ ************************************************************* """
    """ **************** all buttons is here !*********************** """

    def bot_buttons(self):
        self.main_page_button()
        self.profile_page_button()
        self.show_amount_button()

    def main_page_button(self):
        # TODO MainPage Button need to fix
        self.MainPage.likeB.clicked.connect(self.do_like)
        self.MainPage.followB.clicked.connect(self.do_follow)
        self.MainPage.unfollowB.clicked.connect(self.do_unfollow)
        self.MainPage.mixB.clicked.connect(self.do_mix)
        self.MainPage.commentsB.clicked.connect(self.do_comments)
        self.MainPage.startB.clicked.connect(self.start_bot)
        self.MainPage.stopB.clicked.connect(self.stop_bot)
        self.MainPage.endB.clicked.connect(self.end_bot)
        self.MainPage.profileB.clicked.connect(self.show_profile)
        # live_report not work
        self.MainPage.live_reportB.clicked.connect(self.show_report)

    def profile_page_button(self):
        # TODO profile page button here !
        self.profile.saveB.clicked.connect(self.save_profile)
        self.profile.applyB.clicked.connect(self.apply_profile)
        self.profile.closeB.clicked.connect(self.close_profile)
        self.profile.autoB.clicked.connect(self.auto_fill_profile)
        self.profile.amountB.clicked.connect(self.show_amount)

    def show_amount_button(self):
        self.amount_page.saveB.clicked.connect(self.save_amount)
        self.amount_page.closeB.clicked.connect(self.close_amount)
        self.amount_page.applyB.clicked.connect(self.apply_amount)
        self.amount_page.autoB.clicked.connect(self.auto_fill_amount)

    """ **************************** END ****************************** """

    """ ********************** mainPage activity ********************** """
    def login_bot(self):
        self.login_Page.show()
        self.login_Page.loginb.clicked.connect(self.make_session)

    def make_session(self):
        username = self.login_Page.username.text()
        password = self.login_Page.password.text()
        self.session = InstaPy(username=username,
                               password=password,
                               headless_browser=False,
                               disable_image_load=True,
                               show_logs=True)

        self.session.set_simulation(enabled=True)
        self.session.set_relationship_bounds(enabled=True,
                                             potency_ratio=None,
                                             delimit_by_numbers=True,
                                             max_followers=7500,
                                             max_following=3000,
                                             min_followers=25,
                                             min_following=25,
                                             min_posts=5)
        self.session.set_skip_users(skip_private=True,
                                    skip_no_profile_pic=False,
                                    skip_business=True, )
        self.session.login()
        self.close_login_page()
        return self.session

    def close_login_page(self):
        self.login_Page.hide()
        self.MainPage.show()

    def do_like(self):
        self.session.like_by_tags(self.tags_list,
                                  amount=int(self.amount_like/10),
                                  interact=True)

    def do_follow(self):
        self.session.follow_user_followers(self.target_list,
                                           amount=self.amount_follow,
                                           randomize=True,
                                           sleep_delay=random.randint(26, 38),
                                           interact=True)

    def do_unfollow(self):
        self.session.unfollow_users(amount=self.amount_unfollow,
                                    allFollowing=True,
                                    style="RANDOM",
                                    sleep_delay=random.randint(26, 38))

    def do_mix(self):
        self.session.set_user_interact(amount=self.amount_mix, randomize=True, percentage=100,
                                       media='Photo')
        self.session.set_do_like(enabled=True, percentage=98)
        self.session.set_do_comment(enabled=True, percentage=25)
        self.session.set_comments(self.comments_list, media='Photo')
        self.session.set_do_follow(enabled=True, percentage=80)

        number = random.randint(3, 5)

        if len(self.target_list) <= number:
            random_targets = self.target_list
        else:
            random_targets = random.sample(self.target_list, number)

        self.session.follow_user_followers(random_targets,
                                           amount=random.randint(5, 7),
                                           randomize=True,
                                           sleep_delay=random.randint(26, 38),
                                           interact=True)

    # TODO comments not work need to work (work in mix)
    # want get amount from user and do comments
    def do_comments(self):
        self.session.set_user_interact(amount=3, randomize=True, percentage=100,
                                       media='Photo')
        self.session.set_do_comment(enabled=True, percentage=100)
        self.session.set_comments(self.comments_list, media='Photo')

    def start_bot(self):
        self.login_Page.show()
        self.login_Page.loginb.clicked.connect(self.make_session)

    def end_bot(self):
        self.session.end(threaded_session=True)
        sys.exit(app.exec())

    def stop_bot(self):
        self.session.end(threaded_session=True)

    def show_profile(self):
        self.profile.show()

    # TODO live report not work need to fix
    # want to show the user activity report !
    def show_report(self):
        self.live_Report.show()

    """ **************************** END ****************************** """

    """ ********************** ProfilePage activity ******************* """

    def apply_profile(self):
        self.dont_like = self.profile.dontList.text()
        self.ignore_list = self.profile.ignoreList.text()
        self.friend_list = self.profile.friendList.text()
        self.tags_list = self.profile.tagsList.text()
        self.target_list = self.profile.targetList.text()
        self.Business_Target_list = self.profile.BtargetList.text()
        self.comments_list = self.profile.commentsList.text()

        self.dont_like = self.remove_white_space(self.dont_like.split(" "))
        self.ignore_list = self.remove_white_space(self.ignore_list.split(" "))
        self.friend_list = self.remove_white_space(self.friend_list.split(" "))
        self.tags_list = self.remove_white_space(self.tags_list.split(" "))
        self.target_list = self.remove_white_space(self.target_list.split(" "))
        self.Business_Target_list = self.remove_white_space(self.Business_Target_list.split(" "))

        # split(" ") is not work for comments need to remake it make it 2 space just for now
        self.comments_list = self.remove_white_space(self.comments_list.split("  "))

    def close_profile(self):
        self.profile.hide()
        self.MainPage.show()

    def save_profile(self):
        name = ['dont_like', 'ignore_list', 'friend_list', 'tags_list', 'target_list', 'Business_Target_list',
                'comments_list']

        data = [self.dont_like, self.ignore_list, self.friend_list, self.tags_list, self.target_list,
                self.Business_Target_list, self.comments_list]

        with open('profile info/profile.txt', 'w', encoding='utf-8') as f:
            info = dict(zip(name, data))
            f.write("%s" % info)

    def auto_fill_profile(self):
        # read info from text file and get it as list that is why i use self.lstr_to_nstr(str)
        # need find better way to read them as str
        with open('profile info/profile.txt', 'r', encoding='utf-8') as f:
            for lines in f:
                f.readline()

        info = literal_eval(lines)

        self.dont_like = info['dont_like']
        self.ignore_list = info['ignore_list']
        self.friend_list = info['friend_list']
        self.tags_list = info['tags_list']
        self.target_list = info['target_list']
        self.Business_Target_list = info['Business_Target_list']
        self.comments_list = info['comments_list']

        self.profile.dontList.setText(self.lstr_to_nstr(str(self.dont_like)))
        self.profile.ignoreList.setText(self.lstr_to_nstr(str(self.ignore_list)))
        self.profile.friendList.setText(self.lstr_to_nstr(str(self.friend_list)))
        self.profile.tagsList.setText(self.lstr_to_nstr(str(self.tags_list)))
        self.profile.targetList.setText(self.lstr_to_nstr(str(self.target_list)))
        self.profile.BtargetList.setText(self.lstr_to_nstr(str(self.Business_Target_list)))
        self.profile.commentsList.setText(self.lstr_to_nstr(str(self.comments_list)))


    """ **************************** END ****************************** """

    """ ********************** amountPage activity ******************* """

    def apply_amount(self):
        # check to just get int not more as 150 move for max
        self.amount_like = int(self.amount_page.like_amount.text())
        self.amount_follow = int(self.amount_page.follow_amount.text())
        self.amount_unfollow = int(self.amount_page.unfollow_amount.text())
        self.amount_mix = int(self.amount_page.mix_amount.text())


    def auto_fill_amount(self):
        with open('profile info/amount_info.txt', 'r', encoding='utf-8') as f:
            for lines in f:
                f.readline()

        info = literal_eval(lines)
        self.amount_like = int(info["like"])
        self.amount_follow = int(info["follow"])
        self.amount_unfollow = int(info["unfollow"])
        self.amount_mix = int(info["mix"])
        # need to change to int
        self.amount_page.like_amount.setText(str(self.amount_like))
        self.amount_page.follow_amount.setText(str(self.amount_follow))
        self.amount_page.unfollow_amount.setText(str(self.amount_unfollow))
        self.amount_page.mix_amount.setText(str(self.amount_mix))


    def show_amount(self):
        self.amount_page.show()

    def save_amount(self):
        amount_size = ["like", "follow", "unfollow", "mix"]

        data = [self.amount_like,
                self.amount_follow,
                self.amount_unfollow,
                self.amount_mix]

        with open('profile info/amount_info.txt', 'w', encoding='utf-8') as f:
            info = dict(zip(amount_size, data))

            f.write("%s" % info)


    def close_amount(self):
        self.amount_page.hide()
        self.profile.show()

    """ **************************** END ****************************** """

    """ ********************** other  function  ******************* """

    @staticmethod
    def remove_white_space(tag):
        while tag[-1] == "":
            del tag[-1]
            tag = tag
        while tag[0] == "":
            del tag[0]
            tag = tag
        return tag

    def lstr_to_nstr(self, lstr):
        strs = lstr
        nstr = re.sub(r'[?|$|.|!]', r'', strs)
        nestr = re.sub(r'[^a-zA-Z0-9 ]', r'', nstr)
        return nestr

    """ **************************** END ****************************** """







if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Bot()
    sys.exit(app.exec())
