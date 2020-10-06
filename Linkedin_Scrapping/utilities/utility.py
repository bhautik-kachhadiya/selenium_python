from utilities.password import password
import time


class Xpaths():

    def get_submit(self):
        return "//form[contains(@method,'post')]//button[contains(@type,submit)]"

    def get_search_box(self):
        return "//header[contains(@id,'global-nav')]//input"

    def get_user_name(self):
        return "//span[contains(@class,'feed-shared-actor__name')]/span[contains(@dir,'ltr')]"

    def get_user_detail(self):
        return "//span[contains(@class,'feed-shared-actor__description')]/div[contains(@id,ember)]/span"

    def get_post_time(self):
        return "//span[contains(@class,'feed-shared-actor__sub-description')]/div[contains(@class,'feed-shared-text-view white-space-pre-wrap')]/span[1]"

    def get_text(self):
        return "//div[contains(@class,'feed-shared-text')]/span[contains(@class,'break-words')]/span"

    def get_sec_page(self):
        return "//ul/li[contains(@class,'artdeco-pagination__indicator')][2]"

    def get_num_of_page(self):
        return "//ul/li[contains(@class,'artdeco-pagination__indicator')][10]/button/span"

    def get_all_blocks(self):
        return "//ul[contains(@class,'search-results__list')]/li"


class Values():
    def get_site(self):
        return "https://www.linkedin.com/login"

    def get_user_name(self):
        return "bhtkkachhadiya@gmail.com"

    def get_password(self):
        return password

    def get_tag(self):
        return "#robot"

    def get_enter(self):
        return "u'\ue007'"


class Script():
    def scroll(self, driver):
        time.sleep(5)
        for i in range(10):
            time.sleep(4)
            driver.execute_script("window.scrollBy({top:1000,behavior:'smooth'})")
        time.sleep(5)
