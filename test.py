# coding = utf-8
import unittest
from selenium import webdriver
import time

class Test(unittest.TestCase):  # 继承至TestCase，表示这是一个测试用例类
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()

    @classmethod
    def tearDown(self):
        self.driver.close()

    # 测试播放歌曲
    def test(self):
        self.driver.get('http://127.0.0.1:8000/')
        print("打开音乐播放器页面成功")
        time.sleep(2)

        self.driver.find_element_by_id("play").click()
        print("播放歌曲成功")
        time.sleep(5)

        # 测试mode切换+切歌
        # 循环播放mode
        self.driver.find_element_by_id("prev").click()
        print("播放上一首歌成功")
        time.sleep(2)
        self.driver.find_element_by_id("next").click()
        print("播放下一首歌成功")
        time.sleep(2)
        # 单曲循环播放mode
        self.driver.find_element_by_id("mode").click()
        time.sleep(3)
        self.driver.find_element_by_id("next").click()
        print("单曲循环播放成功")
        time.sleep(3)
        # 随机播放mode
        self.driver.find_element_by_id("mode").click()
        time.sleep(3)
        self.driver.find_element_by_id("next").click()
        print("随机播放成功")
        time.sleep(3)

        # 搜索歌曲
        self.driver.find_element_by_id("search").send_keys("爱你")
        self.driver.find_element_by_id("search_button").click()
        print("搜索歌曲成功")
        time.sleep(2)
        self.driver.find_element_by_id("search").clear()

        # 测试暂停播放
        self.driver.find_element_by_id("play").click()
        print("暂停播放成功")
        time.sleep(2)


        # 测试跳转到表情识别页面
        # self.driver.find_element_by_id("jump").click()
        self.driver.get('http://127.0.0.1:8000/index_emotion/')
        print("跳转到表情识别页面成功")
        time.sleep(5)

        # 测试上传图片
        self.driver.find_element_by_name("file").send_keys('D:\\happy.jpg')
        self.driver.find_element_by_id("submit").click()
        print("上传表情成功")
        time.sleep(5)
        '''获取alert对话框'''
        alert = self.driver.switch_to_alert()
        '''添加等待时间'''
        time.sleep(2)
        '''获取警告对话框的内容'''
        print(alert.text)  # 打印警告对话框内容
        alert.accept()  # alert对话框属于警告对话框，我们这里只能接受弹窗
        time.sleep(5)
        alert2 = self.driver.switch_to_alert()
        alert2.accept()  # alert对话框属于警告对话框，我们这里只能接受弹窗
        time.sleep(5)


if __name__ == "__main__":
  unittest.main()

