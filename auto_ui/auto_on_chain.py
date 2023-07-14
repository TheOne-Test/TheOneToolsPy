import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from auto_on_chain_ele_location import *


class AutoOnChain:
    """
    自动上链
    """

    def __init__(self, driver):
        self.driver = driver

    def is_ele_present(self, value, by=By.XPATH):
        """
        判断元素是否存在
        :param value: 元素定位表达式
        :param by: 默认XPATH
        :return: 存在返回 True，不存在返回 False
        """
        try:
            time.sleep(2)
            self.driver.implicitly_wait(2)
            self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            return False
        return True

    def login(self, account, pwd):
        """
        登录
        :param account: 账号
        :param pwd: 密码
        :return:
        """
        self.driver.implicitly_wait(2)
        username = self.driver.find_element(by=By.XPATH, value=username_loc)
        username.send_keys(account)
        password = self.driver.find_element(by=By.XPATH, value=password_loc)
        password.send_keys(pwd)
        login = self.driver.find_element(by=By.XPATH, value=login_loc)
        login.click()
        if self.is_ele_present(login_loc):
            raise Exception("账号密码错误！！！")

    def search_commodity(self, commodity_uuid):
        """
        查询商品
        :param commodity_uuid: 商品UUID
        :return: 不存在抛出 NoSuchElementException 异常
        """
        self.driver.implicitly_wait(2)

        # 进入商品管理页面
        commodity_tab = self.driver.find_element(by=By.XPATH, value="//span[text()='商品']")
        commodity_tab.click()
        commodity_manage_tab = self.driver.find_element(by=By.XPATH, value="//li/span[text()='商品管理']")
        commodity_manage_tab.click()

        self.driver.implicitly_wait(2)

        # 输入商品uuid并查询
        commodity_uuid_input = self.driver.find_element(by=By.XPATH,
                                                   value="//input[@class='el-input__inner' and @placeholder='请输入商品UUID']")
        commodity_uuid_input.send_keys(commodity_uuid)
        search = self.driver.find_element(by=By.XPATH, value="//button/i[@class='el-icon-search']")
        search.click()

        self.driver.implicitly_wait(2)

        # 获取查询结果，根据是否有“查”按钮判断
        try:
            self.driver.find_element(by=By.XPATH, value="//i[@class='el-icon-refresh pointer']")
        except NoSuchElementException:
            raise NoSuchElementException("未搜索到指定商品，请检查商品UUID！！！")

    def on_chain(self):
        """
        上链
        :return:
        """
        self.driver.implicitly_wait(2)
        chain = self.driver.find_element(by=By.XPATH,
                                    value=chain_loc)
        self.driver.execute_script("arguments[0].click();", chain)
        self.driver.implicitly_wait(2)
        weiyi_radio = self.driver.find_element(by=By.XPATH, value="//span[text()='唯艺链（优先）']")
        self.driver.execute_script("arguments[0].click();", weiyi_radio)

        time.sleep(1)
        # 确定
        submit = self.driver.find_element(by=By.XPATH,
                                     value="//button[@class='el-button el-button--primary el-button--small']/span[text()='确 定']")
        self.driver.execute_script("arguments[0].click();", submit)

        # 确定上链
        self.driver.implicitly_wait(2)
        confirm = self.driver.find_element(by=By.XPATH, value="//span[text()='确定上链']")
        self.driver.execute_script("arguments[0].click();", confirm)

    def add_sku(self, sku_num):
        """
        添加库存
        :param sku_num: sku数量
        :return:
        """
        self.driver.implicitly_wait(2)
        # 添加库存
        add = self.driver.find_element(by=By.XPATH, value="//button[@title='增加sku']")
        self.driver.execute_script("arguments[0].click();", add)
        self.driver.implicitly_wait(2)
        # 输入数量
        self.driver.find_element(by=By.XPATH,
                            value="//input[@class='el-input__inner' and @placeholder='请输入数量']").send_keys(sku_num)
        # 确定
        submit = self.driver.find_element(by=By.XPATH,
                                     value="//div[@aria-label='商品增加sku']//following-sibling::span[text()='确 定']")
        self.driver.execute_script("arguments[0].click();", submit)
        time.sleep(3)

    def is_on_chaining(self):
        """
        检查是否在上链中
        :return:
        """
        self.driver.implicitly_wait(2)
        # 点击“查”，查看上链结果
        check = self.driver.find_element(by=By.XPATH,
                                    value=find_loc)
        self.driver.execute_script("arguments[0].click();", check)

        time.sleep(1)

        # 查看上链中的数量
        chaining_num = self.driver.find_elements(by=By.XPATH, value="//div[@class='line']")[1].text
        if chaining_num == "上链中数量：0":
            # 不存在上链中，关闭弹窗
            close = self.driver.find_element(by=By.XPATH, value="//span[text()='查看上链结果']/following-sibling::button")
            self.driver.execute_script("arguments[0].click();", close)
            return False
        return True

    def wait_for_chaining(self):
        """
        刷新上链结果
        :return:
        """
        # 查看上链中的数量
        chaining_num = self.driver.find_elements(by=By.XPATH, value="//div[@class='line']")[1].text
        start_time = time.time()
        while chaining_num != "上链中数量：0":
            print("当前正在上链中，继续等待～～～，", chaining_num)
            time.sleep(60)
            refresh_status = self.driver.find_element(by=By.XPATH, value="//span[text()='刷新上链状态']")
            self.driver.execute_script("arguments[0].click();", refresh_status)
            time.sleep(1)
            chaining_num = self.driver.find_elements(by=By.XPATH, value="//div[@class='line']")[1].text
            end_time = time.time()
            wait_time = int((end_time - start_time)//60)
            print("已等待时长：", wait_time, " 分钟")
            if wait_time > 30:
                raise Exception("已等待超过30分钟，请人为检查上链是否卡住了！！！")
        else:
            print("上链中数量为 0，上链结束，关闭弹窗")
            # 关闭弹窗
            close = self.driver.find_element(by=By.XPATH, value="//span[text()='查看上链结果']/following-sibling::button")
            self.driver.execute_script("arguments[0].click();", close)

    def refresh_status(self):
        """
        点击“⭕️”刷新状态
        :return:
        """
        self.driver.implicitly_wait(2)
        icon_refresh_pointer = self.driver.find_element(by=By.XPATH, value="//i[@class='el-icon-refresh pointer']")
        self.driver.execute_script("arguments[0].click();", icon_refresh_pointer)  # 该按钮的click会被拦截，使用js注入

    def auto_on_chain(self, sku_num=500, times=1):
        """
        自动上链
        :param sku_num:
        :param times:
        :return:
        """
        count = 0  # 已上链次数
        times = int(times)
        while count < times:
            # 先点击“查”，检查是否在上链中
            if self.is_on_chaining():
                print("==========存在正在上链中的sku，将等待此部分先完成上链再继续本次操作==========")
                # 如果在上链中就等待
                self.wait_for_chaining()
                print("==========历史上链中的sku已完成上链，继续本次操作==========")

            # 点击“⭕️”刷新
            self.refresh_status()
            # 如果有待上链的，点击“链”上链
            if self.is_ele_present(value=chain_loc):
                print("==========存在未上链的sku，会先将未上链的sku完成上链==========")
                self.on_chain()
                time.sleep(3)
                # 等待上链
                if self.is_on_chaining():
                    self.wait_for_chaining()
                    print("==========未上链的sku已完成上链==========")
            # 如果没有，增加库存，点击“⭕️”刷新，上链
            print("==========添加库存==========")
            self.add_sku(sku_num)
            self.refresh_status()
            print("==========上链==========")
            self.on_chain()
            count += 1
            time.sleep(3)
            # 等待上链
            if self.is_on_chaining():
                self.wait_for_chaining()
                print("==========第 {0} 次上链成功==========".format(count))
        print("～～～～～～～～～～～～～～～～上链结束～～～～～～～～～～～～～～～～")


if __name__ == '__main__':
    # wb = webdriver.Chrome()
    # wb.maximize_window()
    # wb.get("https://qa-cms.theone.art/")
    #
    # driver = AutoOnChain(wb)
    #
    # # 登录
    # driver.login("苏明辉", "XXX")
    # # 查询商品
    # driver.search_commodity("1ce23c9decb165eb09e57251de9ad0fb")
    # # 自动上链
    # driver.auto_on_chain(1)

    # 测试一：当前有未上链的 —— OK
    # 测试二：当前有正在上链中的 —— OK
    # 测试三：当前无未上链的、无上链中的 —— OK

    url = input("请输入CMS后台地址，默认值：“https://qa-cms.theone.art/”，按【Enter】跳过输入，即使用默认值：")
    if url == "":
        url = "https://qa-cms.theone.art/"
    print("url = ", url)

    while True:
        account = input("请输入CMS后台登录账号：")
        print("account = ", account)
        pwd = input("请输入CMS后台登录密码：")
        print("pwd = ", pwd)
        if pwd == "" or account == "":
            print("账号密码不可为空！！！")
            continue
        break

    while True:
        uuid = input("请输入上链商品的uuid：")
        if uuid == "":
            print("上链商品的uuid不可为空！！！")
            continue
        print("uuid = ", uuid)
        break

    sku_num = input("请输入每次上链数量（不大于500），默认“500”个，按【Enter】跳过输入，即使用默认值：")
    if sku_num == "":
        sku_num = 500
    print("sku_num = ", sku_num)

    sku_times = input("请输入上链次数，默认“1”次，按【Enter】跳过输入，即使用默认值：")
    if sku_times == "":
        sku_times = 1
    print("sku_times = ", sku_times)

    wb = webdriver.Chrome()
    wb.maximize_window()
    wb.get(url)
    driver = AutoOnChain(wb)

    # 登录
    driver.login(account, pwd)
    # 查询商品
    driver.search_commodity(uuid)
    # 自动上链
    driver.auto_on_chain(sku_num, sku_times)