import time
from selenium import webdriver
from utilities.utility import Xpaths, Values, Script
from traverser import Traverser
import mysql.connector
from datetime import date as dt

xpath = Xpaths()
val = Values()
script = Script()


class RunTest():
    user_names = []
    users_detail = []
    post_times = []
    post_text = []
    all_data = []

    def test(self):

        driver = webdriver.Chrome()
        driver.implicitly_wait(1000)
        driver.maximize_window()
        driver.get(val.get_site())

        self.login(driver)

        time.sleep(4)
        search = driver.find_element_by_xpath(xpath.get_search_box())

        search.send_keys(val.get_tag())
        search.send_keys(u'\ue007')
        script.scroll(driver)


        user_list = driver.find_elements_by_xpath(xpath.get_user_name())
        user_detail = driver.find_elements_by_xpath(xpath.get_user_detail())
        post_time = driver.find_elements_by_xpath(xpath.get_post_time())
        post_text = driver.find_elements_by_xpath(xpath.get_text())

        self.save_user_names(user_list, user_detail, post_time, post_text)
        self.store_in_single()

        # self.show_data()
        self.db_saver()

        # flushing datastructures after storing in database
        RunTest.user_names = []
        RunTest.users_detail = []
        RunTest.post_times = []
        RunTest.post_text = []
        RunTest.all_data = []
        time.sleep(3)
        page_2 = driver.find_element_by_xpath(xpath.get_sec_page())
        page_2.click()
        time.sleep(3)
        url_with_page = driver.current_url

        total_page = driver.find_element_by_xpath(xpath.get_num_of_page()).text

        traverser = Traverser(driver, url_with_page, total_page)
        traverser.test()

    def login(self, driver):
        user_name = driver.find_element_by_id('username')
        user_name.send_keys(val.get_user_name())
        password_box = driver.find_element_by_id('password')
        password_box.send_keys(val.get_password())

        submit = driver.find_element_by_xpath(xpath.get_submit())
        submit.click()

    def save_user_names(self, user_list, user_detail, post_time, post_text):

        for i in user_list:
            RunTest.user_names.append(i.text)

        # FILLING EMPTY SPACES
        if len(user_detail) < len(user_list):
            req = len(user_list) - len(user_detail)
            for i in range(len(user_detail), len(user_detail) + req):
                user_detail.append('null')

        for i in user_detail:
            RunTest.users_detail.append(i.text)

        for i in post_time:
            RunTest.post_times.append(str(i.text).strip())

        # FILLING EMPTY SPACES
        if len(post_text) < len(user_list):
            req = len(user_list) - len(post_text)
            for i in range(len(user_detail), len(post_text) + req):
                post_text.append('null')

        for i in post_text:
            RunTest.post_text.append(str(i.text).strip())

    def store_in_single(self):
        for i in range(len(RunTest.user_names)):
            RunTest.all_data.append(
                [RunTest.user_names[i], RunTest.users_detail[i], RunTest.post_times[i], RunTest.post_text[i]])

    def show_data(self):
        for i in RunTest.all_data:
            for j in i:
                print(j)
            print("-------------------------------")

    def db_connector(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='my_database',
            port=3303
        )
        self.cur = self.conn.cursor()
        print('CONNECTION SUCCESSFUL WITH DATABASE')
        return self.conn, self.cur

    def db_saver(self):
        print("CONTROL CAME INTO DB SAVER")
        table_name = val.get_tag()[1::]
        conn, curr = self.db_connector()
        curr.execute("""DROP TABLE IF EXISTS """ + table_name)
        print('TABLE DROPPED SUCCESSFULLY')
        curr.execute(
            """create table """ + table_name + """(id int NOT NULL AUTO_INCREMENT,user_name text,profession text ,
            posted_time text,post_text text,entry_date DATE,PRIMARY KEY (id))""")
        print('TABLE CREATED SUCCESSFULLY')
        for i in RunTest.all_data:
            curr.execute(
                """insert into """ + table_name + """(user_name,profession,posted_time,post_text,entry_date) values (
                %s,%s,%s,%s,%s)""",
                (
                    str(i[0]).strip(), str(i[1]).strip(), str(i[2]).strip(), str(i[3]).strip(), dt.today()
                ))

        conn.commit()
        print('DATA COMMITTED SUCCESSFULLY...........')


chrome_test = RunTest()
chrome_test.test()
