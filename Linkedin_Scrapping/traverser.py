from utilities.utility import Script, Values, Xpaths
import time
from datetime import date as dt
import mysql.connector

script = Script()
xpath = Xpaths()
val = Values()


class Traverser():
    user_names = []
    users_detail = []
    post_times = []
    post_text = []
    all_data = []

    def __init__(self, driver, url, total_page):
        self.driver = driver
        self.url = url
        self.total_page = total_page

    def test(self):
        for i in range(2, int(self.total_page) + 1):
            # str1 = "https://www.linkedin.com/search/results/all/?keywords=%23robot&origin=GLOBAL_SEARCH_HEADER&page=2"
            new_url = self.url.replace('page=2', 'page=' + str(i))
            print(new_url)
            self.driver.get(new_url)
            time.sleep(3)

            driver = self.driver
            script.scroll(driver)

            user_list = driver.find_elements_by_xpath(xpath.get_user_name())
            user_detail = driver.find_elements_by_xpath(xpath.get_user_detail())
            post_time = driver.find_elements_by_xpath(xpath.get_post_time())
            post_text = driver.find_elements_by_xpath(xpath.get_text())

            self.save_user_names(user_list, user_detail, post_time, post_text)
            self.store_in_single()

            self.db_saver()

            print("SAVED AND COMMITTED DATA OF PAGE : "+str(i))

            """
            MAKING DATA STRUCTURE EMPTY AFTER STORING DATA INTO DATABASE,
            IN NEXT ITERATION, DATA OF NEW PAGE WILL BE STORED !!!
            """
            Traverser.user_names = []
            Traverser.users_detail = []
            Traverser.post_times = []
            Traverser.post_text = []
            Traverser.all_data = []

    def save_user_names(self, user_list, user_detail, post_time, post_text):
        for i in user_list:
            Traverser.user_names.append(i.text)

        # FILLING EMPTY SPACES
        if len(user_detail) < len(user_list):
            req = len(user_list) - len(user_detail)
            for i in range(len(user_detail), len(user_detail) + req):
                user_detail.append('null')

        for i in user_detail:
            Traverser.users_detail.append(i.text)

        for i in post_time:
            Traverser.post_times.append(str(i.text).strip())

        # FILLING EMPTY SPACES
        if len(post_text) < len(user_list):
            req = len(user_list) - len(post_text)
            for i in range(len(user_detail), len(post_text) + req):
                post_text.append('null')

        for i in post_text:
            Traverser.post_text.append(str(i.text).strip())

    def store_in_single(self):
        count = 0
        print("LENGTH OF USERNAMES : "+str(len(Traverser.user_names)))
        try:
            for i in range(len(Traverser.user_names)-1):
                count += 1
                print(i)
                Traverser.all_data.append(
                    [Traverser.user_names[i], Traverser.users_detail[i], Traverser.post_times[i], Traverser.post_text[i]])
            print('COUNT : '+str(count))
        except:
            pass
    def db_saver(self):
        print("CONTROL CAME INTO DB SAVER")
        table_name = val.get_tag()[1::]
        conn, curr = self.db_connector()

        for i in Traverser.all_data:
            curr.execute(
                """insert into """ + table_name + """ (user_name,profession,posted_time,post_text,entry_date) values (%s,%s,%s,%s,%s)""",
                (
                    str(i[0]).strip(), str(i[1]).strip(), str(i[2]).strip(), str(i[3]).strip(), dt.today()
                ))

        conn.commit()
        print('DATA COMMITTED SUCCESSFULLY...........')

    def db_connector(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'root',
            database = 'my_database',
            port = 3303
        )
        self.cur = self.conn.cursor()
        print('CONNECTION SUCCESSFUL WITH DATABASE')
        return self.conn,self.cur
