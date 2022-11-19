from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep


def homework_select(driver) -> list:
    # module selecting
    module_form = driver.find_element(By.ID, 'module_id')
    module_list = list(map(lambda elem: elem.text, module_form.find_elements(By.TAG_NAME, "option")))[1:]

    print(" - Choose a module:")
    for i in range(len(module_list)):
        print(f"    {i + 1}. {module_list[i]}")

    while not (0 <= (block_index := int(input(" - Type number of selected element: ")) - 1) < len(module_list)):
        print("ERROR: Wrong value")
    Select(module_form).select_by_visible_text(module_list[block_index])
    sleep(1.5)

    # homeworks selecting
    lesson_form = driver.find_element(By.ID, 'lesson_id')
    lesson_list = list(map(lambda elem: elem.text, lesson_form.find_elements(By.TAG_NAME, "option")))[1:]

    print(" - Choose homeworks:")
    for i in range(len(lesson_list)):
        print(f"    {i + 1}. {lesson_list[i]}")

    homework_indexes = list(
        map(int, input(" - Enter numbers of the selected homeworks separated by a space: ").split()))
    return list(map(lambda index: lesson_list[index - 1], sorted(homework_indexes)))
