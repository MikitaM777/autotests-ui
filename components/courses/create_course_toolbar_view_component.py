from components.base_component import BaseComponent
from playwright.sync_api import Page
from elements.text import Text
from elements.button import Button
import allure


class CreateCourseToolbarViewComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = Text(page,"create-course-toolbar-title-text", "Title")
        self.create_course_button = Button(page,"create-course-toolbar-create-course-button", "Create course")

    @allure.step("Check visible create course toolbar")
    def check_visible(self, is_create_course_disabled=True):
        self.title.check_visible()
        self.title.check_have_text('Create course')
        self.create_course_button.check_visible()

        if is_create_course_disabled:
            self.create_course_button.check_disabled()
        if not is_create_course_disabled:
            self.create_course_button.check_enabled()


    def click_create_course_button(self):
        self.create_course_button.click()