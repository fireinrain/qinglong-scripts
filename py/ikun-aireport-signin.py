# -------------------------------
# cron "30 4 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('ikuuu机场签到')
# 注册地址：https://ikuuu.me/auth/register?code=lzQE


import requests, json, re, os


def main():
    users = os.environ.get('ikun_airport_users')
    users_list = users.split("|")
    for user in users_list:
        session = requests.session()
        # 配置用户名（一般是邮箱）
        # 格式: emial:pass|email:pass


        login_url = 'https://ikuuu.me/auth/login'
        check_url = 'https://ikuuu.me/user/checkin'
        info_url = 'https://ikuuu.me/user/profile'

        header = {
            'origin': 'https://ikuuu.art',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        email = user.split(":")[0]
        passwd = user.split(":")[1]
        data = {
            'email': email,
            'passwd': passwd
        }
        content = None
        try:
            print('进行登录...')
            response = json.loads(session.post(url=login_url, headers=header, data=data).text)
            print(response['msg'])
            # 获取账号名称
            info_html = session.get(url=info_url, headers=header).text
            #     info = "".join(re.findall('<span class="user-name text-bold-600">(.*?)</span>', info_html, re.S))
            #     print(info)
            # 进行签到
            result = json.loads(session.post(url=check_url, headers=header).text)
            print(result['msg'])
            content = result['msg']
            # 进行推送
        except Exception as e:
            content = f'{user}签到失败: {e}'
            print(content)
        # import notify
        # notify.send("ikun机场签到", content)


if __name__ == '__main__':
    main()
