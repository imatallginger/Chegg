import requests

def getLink(mail, link):
    f = open(r"C:\Users\Vusal\Desktop\Chegg BOT X\lib\bot\key.0", "r")
    secretkey = f.readline()
    f.close()

    a = requests.post("https://cheggbot.woosal.com/json.php", data={"mail":"{0}".format(mail),"soru":"{0}".format(link),"key":f"{secretkey}"})
    return a.text