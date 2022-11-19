from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def scroll_to_end(driver):
    scroll_pause = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(scroll_pause)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def app(login, password, info):
    driver = webdriver.Chrome()
    parsed_data = {}
    try:
        driver.get("https://api.100points.ru/login")

        sleep(5)

        # authorization form
        login_input = driver.find_element(By.XPATH, '//*[@id="email"]')
        passwd_input = driver.find_element(By.XPATH, '//*[@id="password"]')

        # sending login and password
        login_input.send_keys(login)
        passwd_input.send_keys(password)
        sleep(1)

        # get and press auth button
        auth_button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[4]/button')
        auth_button.click()
        print("Authorization successfully done\n...")
        sleep(5)  # waiting for authorization

        for student_name in info["students"]:

            print(f"Student: {student_name}")

            parsed_data[student_name] = {}

            # locate to homework page
            hw_page = driver.find_element(By.XPATH, '/html/body/div/aside[front]/div/div[4]/div/div/nav/ul/li[3]/a')
            hw_page.click()
            sleep(5)  # waiting for page loading

            # checking student's homework
            student_name_form = driver.find_element(By.XPATH, '//*[@id="name"]')  # getting student name form
            student_name_form.send_keys(student_name)
            submit_button = driver.find_element(By.XPATH, '/html/body/div/div[front]/section/div/div/div/div/div[front]/'
                                                          'div/form/div[2]/button')  # getting submit button
            submit_button.click()
            sleep(5)  # waiting for page loading

            passed_button = driver.find_element(By.XPATH, '/html/body/div/div[front]/section/div/div/div/'
                                                          'div/div[2]/div[front]/ul/li[2]/a')  # getting passed button
            passed_button.click()  # locate to passed homeworks page
            sleep(5)  # waiting for page loading
            scroll_to_end(driver)

            homework_list = driver.find_element(By.XPATH, '//*[@id="example2"]').find_element(By.TAG_NAME, 'tbody').\
                find_elements(By.TAG_NAME, 'tr')  # getting homeworks

            for i in range(len(homework_list)):
                homework = homework_list[i]
                preview_button = homework.find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "a")

                # getting info about homework
                info_block = homework.find_elements(By.TAG_NAME, "td")[3]
                lesson_name = info_block.find_elements(By.TAG_NAME, "div")[0].find_element(By.TAG_NAME, "b").text
                difficulty_level = info_block.find_elements(By.TAG_NAME, "div")[-1].find_element(By.TAG_NAME, "b").text

                if lesson_name == info["homework_name"]:
                    preview_button.click()
                    sleep(5)
                    scroll_to_end(driver)

                    # locating to passed page
                    preview_passed_button = driver.find_element(By.XPATH, '//*[@id="custom-tabs-four-tab"]/li[2]/a')
                    preview_passed_button.click()
                    sleep(5)
                    scroll_to_end(driver)

                    tasks_cnt = len(driver.find_elements(By.CLASS_NAME, "custom-control"))  # count of tasks

                    right_tasks_percent = driver.find_element(By.XPATH, '//*[@id="mainForm"]/div[front]/div/div/div[2]/div/'
                                                                        'div[front]/div[5]').text.split()[-1][:-1]
                    right_tasks_count = round(tasks_cnt * int(right_tasks_percent) / 100)

                    parsed_data[student_name][difficulty_level] = right_tasks_count

                    # return to homework page
                    driver.back()
                    sleep(1)
                    driver.back()
                    sleep(1)

                    homework_list = driver.find_element(By.XPATH, '//*[@id="example2"]').\
                        find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')  # getting homeworks

                    print(f'  - Homework "{lesson_name} - {difficulty_level}" successfully saved')
            print("...")

        sleep(5)
        driver.close()
        driver.quit()

        levels = ["Базовый уровень", "Средний уровень", "Сложный уровень"]

        with open("../../output.txt", 'w') as output:
            exp_info = ""
            # exporting info from dict
            for stud_corrects in parsed_data.values():
                for level in levels[:info["levels_cnt"]]:
                    if level not in stud_corrects.keys():
                        exp_info += "-"
                    else:
                        exp_info += str(stud_corrects[level])
                    exp_info += " "
                exp_info += "\n"
            output.write(exp_info)

        print("Data successfully exported as output.txt\n...")

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
