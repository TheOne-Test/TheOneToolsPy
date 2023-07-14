import time

import requests


class CommodityManage:

    def __init__(self, token):
        self.headers = {"Authorization": token, "Content-Type": "application/json;charset=UTF-8"}
        self.url = "https://qa-api.theone.art"

    def increase_sku(self, body, times):
        """
        添加库存
        :param body:
        :param times:
        :return:
        """
        url = self.url + "/goods/admin/commodity/increaseSku"
        count = 0
        while count < times:
            start = time.time()
            res = requests.post(url=url, headers=self.headers, json=body, verify=False)
            print(res.text)
            end = time.time()
            print("用时：", end - start, " 秒")
            count += 1
            print("第{0}次已完成".format(count))
            try:
                if int(body["amount"]) > 40000:
                    time.sleep(20)
                    print("sku数量超过4w，每次循环前sleep 20 秒")
            except Exception as e:
                print(e)

    def operation(self, commodityUuid, userId, commodityAmount):
        """
        补发
        :param commodityUuid:
        :param userId:
        :param commodityAmount:
        :return:
        """
        url = self.url + "/goods/admin/treasure/operation"
        body = {
            "commodityId": commodityUuid,
            "type": 1,
            "randomNumber": 0,
            "userId": userId,
            "commodityAmount": commodityAmount
        }
        res = requests.post(url=url, headers=self.headers, json=body, verify=False)
        assert res.json()["code"] == 200, "发放失败！！！！！！"
        return res.text

    def list_user(self, phone):
        """
        获取用户uuid
        :param phone:
        :return:
        """
        url = self.url + "/user/admin/user/listUser"
        body = {
            "pageCount": 1,
            "pageSize": 10,
            "phone": phone
        }
        try:
            res = requests.post(url=url, headers=self.headers, json=body, verify=False).json()
            user_uuid = res["data"]["records"][0]["uuid"]
            return user_uuid
        except Exception as e:
            raise e


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLoi4_mmI7ovokiLCJpYXQiOjE2ODg5ODg1NzMsImV4cCI6MTY4OTU5MzM3M30.gQioAsivkWdADuxKKhxucoVR1chB-ZOHaD518F1cCn7uWiilXuUdxqnE3N22nEk4ftaieJYMFsQQ1otcCBfZHw"
    # increase_sku_body = {
    #     "id": "c4ac0d2891bef9eecadfaa50dc940c50",
    #     "amount": "50000"
    # }

    cm = CommodityManage(token)
    # 添加库存
    # cm.increase_sku(increase_sku_body, 1)

    # count = 0
    # phone = 16170000430
    # while count < 1571:
    #     print(phone)
    #     # 查询用户uuid
    #     userId = cm.list_user(phone)
    #     # print(userId)
    #     # 批量给用户补发
    #     commodityUuid = "c4ac0d2891bef9eecadfaa50dc940c50"
    #     commodityAmount = 250
    #     res = cm.operation(commodityUuid, userId, commodityAmount)
    #     print(res)
    #     phone += 1
    #     count += 1
    #     time.sleep(0.5)
