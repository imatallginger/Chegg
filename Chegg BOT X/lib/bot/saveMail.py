from simplegmail import Gmail
from bs4 import BeautifulSoup
from requests import get
from os import path, mkdir
from datetime import datetime as dt
from lib.bot.log import Log


def createFolder(qId):
    try:
        mkdir(qId)
        return 1
    except FileExistsError:
        return 0


def extractLink(plainMessage):
    messageList = plainMessage.split(
        '\n')
    link = messageList[1][:-1]
    return link


def findQuestionId(questionLink):
    trackidIndex = questionLink.rfind("?trackid")
    if trackidIndex == -1:
        lPure = questionLink
    else:
        lPure = questionLink[:trackidIndex]
    reverseLPure = lPure[::-1]
    reverseLPureQIndex = reverseLPure.find("q")
    reverseQId = lPure[::-1][:reverseLPureQIndex + 1]
    qId = reverseQId[::-1]
    return qId


class SaveMail:
    def __init__(self):
        self.start = dt.now()
        self.log = Log(r"C:\Users\woosal\Desktop\Chegg BOT X", "chegg.log")
        self.downloadMail()

    def downloadMail(self):
        gmail = Gmail()
        try:
            messages = gmail.get_unread_inbox()
            if len(messages) > 0:
                print(f"{len(messages)} new message")
                msg = messages[0]
                link = extractLink(msg.plain)
                print(f"Question link: {link}")
                self.log.info(f"INIT-3:DOWNLOAD_MAIL:{link}")
                qId = findQuestionId(link)
                print(qId)
                createFolder(r"C:\Users\woosal\Desktop\Chegg BOT X\Downloads\{0}".format(qId))
                fullPath = path.abspath(r"C:\Users\woosal\Desktop\Chegg BOT X\Downloads\{0}".format(qId))
                soup = BeautifulSoup(msg.html, 'html.parser')
                imgs = soup.find_all('img')
                urls = [img['src'] for img in imgs]
                for i in range(1, len(urls) - 1):
                    url = urls[i]
                    name = f"{fullPath}\image{i}.png"
                    try:
                        res = get(url)
                        file = open(name, "wb")
                        file.write(res.content)
                    except Exception as e:
                        self.log.alert(f"DOWNLOAD_MAIL:Exception:{e}")
                        pass

                try:
                    f = open(r"{0}\aplain.txt".format(fullPath), "a", encoding="utf-8")
                    f.write("".join(msg.plain.split("\n")[1:-13]))
                    f.close()
                except Exception as e:
                    self.log.alert(f"INIT-3:DOWNLOAD_MAIL:Exception:{e}")
                    pass
                downloadTime = dt.now() - self.start
                self.log.info(f"INIT-3:DOWNLOAD_MAIL:Mail_Downloaded:{qId}")
                print(dt.now())
                print(f"It took {downloadTime} seconds")
                msg.mark_as_read()
                self.log.info(f"INIT-3:DOWNLOAD_MAIL:Mail_Marked:{link}")
            else:
                pass
        except Exception as e:
            self.log.alert(f"INIT-3:DOWNLOAD_MAIL:Exception:{e}")
            pass
