import datetime

class Log:
    def __init__(self, path, logName):
        self.log = f"{datetime.datetime.now()}::"
        self.path = path
        self.logName = logName

    def loging(self, fullLog):
        fileName = r"{0}\{1}".format(self.path,self.logName)
        logFile = open(fileName,"a+",encoding="utf-8")
        logFile.write(fullLog+"\n")
        logFile.close()

    def alert(self, log):
        self.log = f"{datetime.datetime.now()}::"
        alertLog = "ALERT::"
        alertLog += self.log + str(log)
        self.loging(alertLog)

    def info(self, log):
        self.log = f"{datetime.datetime.now()}::"
        infoLog = "INFO::"
        infoLog += self.log + str(log)
        self.loging(infoLog)

    def command(self,log):
        self.log = f"{datetime.datetime.now()}::"
        commandLog = "COMMAND::"
        commandLog += self.log + str(log)
        self.loging(commandLog)
