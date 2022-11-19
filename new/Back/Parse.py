from Handlers.misc import *
from selenium import webdriver


class App:
    def __init__(self, data):
        self.driver = webdriver.Chrome()
        self.data = data
        self.output = {}

    def auth(self):
        try:
            # authorization form
            login_input = self.driver.find_element(By.XPATH, '//*[@id="email"]')
            passwd_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')

            # sending login and password
            login_input.send_keys(self.data.login)
            passwd_input.send_keys(self.data.password)
            sleep(.5)

            # get and press auth button
            auth_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[4]/button')
            auth_button.click()
            print(" - Authorization successfully done")
            sleep(2)
        except Exception as ex:
            print(ex)
            print(" - Authorization failed")

    def get_data(self) -> list:
        self.driver.get(url="https://api.100points.ru/student_homework/index?status=passed&email=&name=&course_id=36&module_id=&lesson_id=")
        self.auth()
        homework_names_list = homework_select(driver=self.driver)

        # receiving homework data (name, url)
        output = []
        for name in homework_names_list:
            lesson_form = self.driver.find_element(By.ID, 'lesson_id')
            Select(lesson_form).select_by_visible_text(name)
            sleep(.5)

            find_btn = self.driver.find_element(By.CSS_SELECTOR, '.card-footer>button')
            find_btn.click()
            sleep(.5)

            output.append({
                'name': name,
                'url': self.driver.current_url
            })
        self.close()
        return output

    def parse(self, homework_index):
        current_homework = self.data.homeworks[homework_index]
        self.driver.get(current_homework['url'])
        sleep(.5)

        # try to auth
        self.auth()
        sleep(.5)

        # preparing return dictionary
        for level in ["Базовый уровень", "Средний уровень", "Сложный уровень"]:
            self.output[f"{current_homework['name']} - {level}"] = {}

        pages_cnt = int(self.driver.find_element(By.CSS_SELECTOR, ".pagination>li:nth-last-child(2)>a").text)

        # check all pages
        for pressed in range(pages_cnt):
            # check all homeworks
            table_rows = self.driver.find_elements(By.CLASS_NAME, 'odd')
            for i in range(len(table_rows)):
                row = table_rows[i]
                difficulty_level = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)>div:last-child>small>b').text
                student_name = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)>div:first-child').text
                preview_button = row.find_element(By.CSS_SELECTOR, 'td:first-child>a')

                preview_button.click()
                sleep(.5)

                result = self.driver.find_elements(By.CLASS_NAME, 'card-body')[0].\
                    find_element(By.CSS_SELECTOR, ".row>div:last-child").text.split()[-1][:-1]

                try:
                    self.output[f"{current_homework['name']} - {difficulty_level}"][self.data.students_list.index(student_name) + 1] = result
                except ValueError:
                    print(" - Error in students list, please check values and fix it")
                    print(student_name)
                    print(self.data.students_list)

                self.driver.back()
                table_rows = self.driver.find_elements(By.CLASS_NAME, 'odd')

            if pressed != pages_cnt - 1:
                next_btn = self.driver.find_element(By.CSS_SELECTOR, ".pagination>li:last-child>a")
                next_btn.click()
                sleep(.5)

        self.close()

    def close(self):
        self.driver.close()
        self.driver.quit()
