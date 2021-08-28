import telnetlib


class NetTool:
    PORT = 23

    MainSocket = None
    HandSocket = None

    def __init__(self, addr1, addr2):
        self.addr1 = addr1
        self.addr2 = addr2

    def GetSockets(self):
        try:
            self.MainSocket = telnetlib.Telnet(self.addr1, self.PORT)
        except:
            self.MainSocket = None
            print("Error while connecting to main robot.")
        try:
            self.HandSocket = telnetlib.Telnet(self.addr2, self.PORT)
        except:
            self.HandSocket = None
            print("Error while connecting to hand.")

        return (self.MainSocket, self.HandSocket)



if __name__ == "__main__":
    NT = NetTool("192.168.137.35", "192.168.137.247")
    print(NT.GetSockets())