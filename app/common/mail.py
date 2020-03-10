
"""mail

mail module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
 

 
def mail(sender, password, receiver, from_, to_, subject, message):
    '''Send Mail # 发送邮件

        Usage: # 使用：
        mail('admin@baoai.co', 'xxxxxxxx', '703264459@qq.com', 'BaoAI', 'henry', 'email test title', 'email content...')

    Args:
        sender (str): Sender's mailbox , for example: 'admin@baoai.co'  # 发件人邮箱
        password (str): 'xxxxxxxx'  # Sender's mailbox password # 发件人邮箱密码
        receiver (str): '703264459@qq.com'  # Recipient mailbox # 收件人邮箱
        from_ (str) (str): Sender's nickname  # 发件人昵称
        to_ (str) (str): Sender's nickname  # 收件人昵称
        subject (str) (str): email's subject  # 邮件标题
        message (str) (str): email's content  # 邮件内容
        
    Returns:
        dict: result, For example: {'status':True, 'message':'Success'}
    '''
    try:
        msg = MIMEText(message,'plain','utf-8')
        msg['From'] = Header(from_,'utf-8')
        msg['To'] = Header(to_,'utf-8')
        msg['Subject'] = Header(subject,'utf-8')
 
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)  # SMTP server in sender's mailbox, general port is 25 # 发件人邮箱中的SMTP服务器，一般端口是25
        server.login(sender, password)  # the sender's mailbox account and password. # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, receiver, msg.as_string())  # the sender's mailbox account, the recipient's mailbox account, and the sending of mail. # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # Close the connection # 关闭连接
        return {'status':True, 'message':'Success'}
    except Exception as e:
        return {'status':False, 'message':"Failed: " + str(e)}


 