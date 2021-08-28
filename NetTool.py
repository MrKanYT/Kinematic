import telnetlib


class NetTool:
    PORT = 0

    MainSocket = None
    HandSocket = None

    last_send = 0

    def __init__(self, addr1, addr2, port, c1, c2):
        self.addr1 = addr1
        self.addr2 = addr2
        self.PORT = port
        self.connectToMain = c1
        self.connectToHand = c2

    def GetSockets(self):
        if self.connectToMain:
            try:
                self.MainSocket = telnetlib.Telnet(self.addr1, self.PORT)
                print("Connected to main robot")
            except:
                self.MainSocket = None
                print("Error while connecting to main robot.")
        else:
            self.MainSocket = None

        if self.connectToHand:
            try:
                self.HandSocket = telnetlib.Telnet(self.addr2, self.PORT)
                print("Connected to hand")
            except:
                self.HandSocket = None
                print("Error while connecting to hand.")
        else:
            self.HandSocket = None

        return (self.MainSocket, self.HandSocket)



if __name__ == "__main__":
    NT = NetTool("192.168.137.35", "192.168.137.247")
    print(NT.GetSockets())