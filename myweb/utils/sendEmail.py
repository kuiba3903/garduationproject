# 发送多种类型的邮件
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random


def generate_code():
    res1 = ""  # 创建变量res1用于存放随机生成的数字
    res2 = ""  # 创建变量res2用于存放随机生成的大写英文字母
    res3 = ""  # 创建变量res3用于存放随机生成的小写英文字母
    for i in range(2):  # 使用循环语句，控制随机选择数字、字母的次数，在这里可以修改随机生成每字母（数字）的次数来控制验证码的长度
        num = random.randint(0, 9)  # 创建变量num,用于存放从0到9之间随机抽取的数字
        res1 += str(num)  # 将两次随机生成的数字连接起来
        num = random.randint(65, 90)  # 创建变量num,用于存放大写字母A到Z之间随机抽取的数字
        res2 += str(chr(num))  # 将两次随机生成的大写字母连接起来
        num = random.randint(97, 122)  # 创建变量num,用于存放小写字母a到z之间随机抽取的数字
        res3 += str(chr(num))  # 将两次随机生成的小写字母连接起来
    string = str(res1 + res2 + res3)  # 创建变量string,用于存放随机生成的数字和字母
    return string


def sendemail(email_to, tpl):
    msg_from = '1372587239@qq.com'  # 发送方邮箱
    passwd = 'hdvfaigtadsyjieh'  # 就是QQ邮箱的授权码
    to = email_to  # 接受方邮箱
    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    code = generate_code()
    if tpl == "login":
        conntent = "您的登录验证码是 %s (60秒内有效)，请勿泄漏给他人。如非本人操作，请忽略本条消息。" % (code,)
        # 把内容加进去
        msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
        # 设置邮件主题
        msg['Subject'] = "登录账号"
        # 发送方信息
        msg['From'] = msg_from
        # 开始发送
        # 通过SSL方式发送，服务器地址和端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        # 开始发送
        s.sendmail(msg_from, to, msg.as_string())
        print("邮件发送成功")
    else:
        conntent = "您的注册验证码是 %s (60秒内有效)，请勿泄漏给他人。如非本人操作，请忽略本条消息。" % (code,)
        # 把内容加进去
        msg.attach(MIMEText(conntent, 'plain', 'utf-8'))
        # 设置邮件主题
        msg['Subject'] = "注册账号"
        # 发送方信息
        msg['From'] = msg_from
        # 开始发送
        # 通过SSL方式发送，服务器地址和端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        # 开始发送
        s.sendmail(msg_from, to, msg.as_string())
        # print("邮件发送成功")
    return code

if __name__ == "__main__":
    sendemail("2449559321@qq.com", 0)