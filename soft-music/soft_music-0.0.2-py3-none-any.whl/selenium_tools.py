import logging
import random
import time
from time import sleep

import numpy as np
from selenium.common.exceptions import (NoSuchAttributeException,
                                        WebDriverException, NoSuchElementException,
                                        NoSuchFrameException, TimeoutException)
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.common.action_chains import ActionChains
from pipino.crawler.behaviors.behavior_exceptions import TooSlowScrollException
from pipino.ecs_crawler.pipino_log import log as logger
from pipino.crawler.nebular import dec

PIXELS_PER_DOWN_KEY = 51


def gen_selenium_find_method(ele_type, multiple=False, extra_maps=None):
    _ = 'elements' if multiple else 'element'
    d = {
        'class': 'class_name'
    }
    if isinstance(extra_maps, dict):
        d = dict(d, **extra_maps)
    return 'find_{}_by_{}'.format(_, d.get(ele_type, ele_type))


def random_sleep(minimum, scale):
    """sleeps for a random amount of time,
    with a min time of minimum seconds, and a long right tail.
    Capped at 15 seconds
    """
    sleep(min(rand_float(minimum, scale), 15))


def random_pageFinish(maximum, shape, scale):
    """Gets the max page to go to
    """
    return min(int(np.random.gamma(shape, scale, 1)[0]), maximum)


@dec.Deprecated('Please use helper.rand_float')
def rand_float(minimum, scale):
    return np.random.pareto(1) * scale + minimum


@dec.Deprecated('Please use helper.gen_selenium_find_method')
def find_one(driver, key):
    return getattr(driver, Bot.find_one_methods[key])


@dec.Deprecated('Please use helper.gen_selenium_find_method')
def find_many(driver, key):
    return getattr(driver, Bot.find_many_methods[key])


class Bot(object):
    find_one_methods = {
        'id': 'find_element_by_id',
        'class': 'find_element_by_class_name',
        'name': 'find_element_by_name',
        'css_selector': 'find_element_by_css_selector',
    }
    find_many_methods = {
        'id': 'find_elements_by_id',
        'class': 'find_elements_by_class_name',
        'name': 'find_elements_by_name',
        'css_selector': 'find_elements_by_css_selector'
    }

    def __init__(self, driver):
        self.driver = driver
        random.seed()

    def click_with_script(self, element):
        element = self.get_element(element)
        self.driver.execute_script("$(arguments[0]).click();", element)

    def type_keys(self, element, key_string):
        # TODO: decode or not?
        try:
            decoded_key_string = key_string.decode('utf8')
        except:
            decoded_key_string = key_string
        for char in decoded_key_string:
            element.send_keys(char)
            random_sleep(0.01, 0.01)

    def click_if_possible(self, element, multiple=False):
        if multiple:
            elements = self.get_elements(element)
            for elt in reversed(elements):
                if self.click_if_possible(elt):
                    return True
            return False
        try:
            element = self.get_element_if_necessary(element)
        except WebDriverException:
            return False
        try:
            element.click()
            return True
        except WebDriverException:
            return False

    def necessary_click(self, element, numb=0, retry=True):
        try:
            elements = self.get_elements(element)
            element = elements[numb]
            random_sleep(1.0, 0.2)
            element.click()
            return True
        except WebDriverException as e:
            logger.warning(e)
            if retry:
                logger.warning("necessary click for %s failed retrying " % str(element))
                sleep(2)
                self.necessary_click(element, numb, False)
            else:
                logger.warning("necessary click for %s failed  not retrying" % str(element))
                raise ValueError
        raise ValueError

    def get_element_if_necessary(self, elem):
        if isinstance(elem, dict):  # effectively overloads for 2 input types
            elem = self.get_element(elem)
        return elem

    def get_element(self, map_to_elt, count=0):
        for key, value in map_to_elt.items():
            try:
                elt = find_one(self.driver, key)(value)
                return elt
            except WebDriverException as e:
                if count == 0:
                    # logger.warning(str(map_to_elt) + ' failed.. Trying again' )
                    return self.get_element(map_to_elt, 1)
                else:
                    logger.debug(str(map_to_elt) + ' failed.')
                    raise
        raise ValueError

    def has_element(self, map_to_elt):
        for key, value in map_to_elt.items():
            try:
                elt = find_one(self.driver, key)(value)
                return True
            except WebDriverException as e:
                return False
        return False

    def get_elements(self, map_to_elts):
        for key, value in map_to_elts.items():
            try:
                elt = find_many(self.driver, key)(value)
                return elt
            except WebDriverException as e:
                logger.warning('{} {} failed'.format(e, map_to_elts))
                # logger.warning(e + str(map_to_elts) + ' failed')
                raise
        raise ValueError

    def get_page(self, url):
        try:
            self.driver.get(url)
        except (TimeoutException, Exception) as e:
            # logger.warning(e)
            logger.exception("Could not open {}".format(url))
            raise

    def switch_to_frame(self, map_to_frame):
        # self.driver.switch_to_frame(self.driver.find_element_by_class_name('cboxIframe'))
        self.driver.switch_to_frame(self.get_element(map_to_frame))

    def switch_to_default(self):
        self.driver.switch_to_default_content()

    def fill_bar(self, map_to_bar, term, submit=False, clear_first=True):
        search_bar = self.get_element_if_necessary(map_to_bar)
        if clear_first:
            search_bar.clear()
        self.type_keys(search_bar, term)
        if submit:
            random_sleep(0.5, 0.5)
            search_bar.send_keys(Keys.RETURN)
            random_sleep(3, .5)

    def type_and_delete_in_bar(self, map_to_bar):
        # This was written because of a quirk in Catho; it just types the letter "a"
        # and then clears it. Catho will not allow you to submit a search that has a default value otherwise.
        search_bar = self.get_element_if_necessary(map_to_bar)
        search_bar.clear()
        # TODO: check this "a"
        self.type_keys(search_bar, "a")
        self.type_keys(search_bar, Keys.BACKSPACE)

    def scroll_down_page(self, distance):
        pass

    def scroll_down_to_element(self, elem, two_paned_scroll='window', element=True, close_in=200, speed=1,
                               check_time=True, total_down=0, ret=False):
        #
        # We want to scroll down to elem but not scroll over
        # close_in is a number between 0 and 300 where 300-close_in is the minimum distance
        # between the top of the page and elem
        #
        try:
            elem = self.get_element_if_necessary(elem)
            total_needed = elem.location['y'] - 300
            starting_time = time.time()
            while total_down < total_needed:
                if (time.time() - starting_time) > 150 and check_time:
                    raise TooSlowScrollException
                action_num = random.random()
                if action_num < 0.01:
                    random_sleep(1.0, 0.1)
                elif action_num < 0.18:
                    random_sleep(0.5, 0.1)
                else:
                    if action_num > 0.95:
                        y_neg = True
                        distance = -rand_float(100, 10)
                    else:
                        y_neg = False
                        distance = rand_float(100, 10) * speed
                    distance = min(total_needed - total_down + close_in, distance)
                    self.smooth_scroll(0, int(abs(distance)), False, y_neg, two_paned_scroll, element)
                    total_down += distance
            if ret:
                return total_needed
        except WebDriverException as e:
            logger.warning(e)
            raise

    def object_scroll(self, element, total_distance):
        try:
            element = self.get_element_if_necessary(element)
            total_down = 0
            while total_down < total_distance:
                action_num = random.random()
                if action_num < 0.05:
                    random_sleep(1.5, 0.1)
                else:
                    if action_num < 0.95:
                        distance = rand_float(100, 10)
                    else:
                        distance = -rand_float(100, 10)
                    num_downs = int(distance / PIXELS_PER_DOWN_KEY)
                    self.down_key(element, num_downs)
                    total_down += num_downs * PIXELS_PER_DOWN_KEY
        except Exception as e:
            logger.warning(e)
            raise

    def smooth_scroll(self, x_dist, y_dist, x_neg, y_neg, two_paned_scroll='window', element=True):
        try:
            if two_paned_scroll != 'window':
                if element:
                    src_str = ''.join(['document.getElementById(\'', two_paned_scroll, '\')'])
                else:
                    src_str = ''.join(['document.getElementsByClassName(\'', two_paned_scroll, '\')[0]'])
            else:
                src_str = 'window'
            x_scroll = '.scrollBy(8,0);'
            y_scroll = '.scrollBy(0,8);'
            if x_neg:
                x_scroll = '.scrollBy(-8,0);'
            if y_neg:
                y_scroll = '.scrollBy(0,-8);'
            for i in range(x_dist // 8):
                self.driver.execute_script(src_str + x_scroll)
                random_sleep(0, 0.001)
            for i in range(y_dist // 8):
                self.driver.execute_script(src_str + y_scroll)
                random_sleep(0, 0.001)
        except WebDriverException as e:
            logger.warning(e)
            raise

    def down_key(self, element, num_times):
        if num_times > 0:
            for i in range(num_times):
                random_sleep(0.1, 0.01)
                element.send_keys(Keys.DOWN)
        else:
            for i in range(-num_times):
                random_sleep(0.1, 0.01)
                element.send_keys(Keys.UP)

    def paginate(self, next_page_button):
        next_page_button = self.get_element_if_necessary(next_page_button)
        random_sleep(1, 0.5)
        return self.click_if_possible(next_page_button)

    def random_finish(self):
        action_num = random.random()
        random_sleep(3, .5)

    def scroll_to_correct_country(self, retry=True):
        try:
            act = Actions(self.driver)
            element = self.driver.find_element_by_class_name('menu-primary')
            us_code = self.driver.find_element_by_id('1')
            act.move_to_element(element).wait(.5, 1).move_to_element(us_code).click().perform()
        except Exception as e:
            if retry:
                logger.warning("scroll to correct country failed... trying again")
                sleep(2)
                self.scroll_to_correct_country(retry=False)
            else:
                logger.warning("scroll to correct country failed... Not retrying")
                raise ValueError

    def click_option_contains(self, selection_box, text):
        for option in selection_box.find_elements_by_tag_name('option'):
            if text in option.text:
                return self.click_if_possible(option)
        logger.warning('Text not found in selection box!')


class ChromeBot(Bot):
    def __init__(self, driver):
        assert isinstance(driver, Chrome)
        super(ChromeBot, self).__init__(driver)


class FirefoxBot(Bot):
    def __init__(self, driver):
        assert isinstance(driver, Firefox)
        super(FirefoxBot, self).__init__(driver)


class Actions(ActionChains):
    def wait(self, minimum, scale):
        time_s = min(np.random.pareto(1) * scale + minimum, 2)
        self._actions.append(lambda: sleep(time_s))
        return self
