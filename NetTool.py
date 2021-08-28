import telnetlib
import re

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

    def ReadDataFromHand(self):
        if self.HandSocket != None:
            data = self.HandSocket.read_very_eager()
            if data != b'':
                try:
                    splitted = re.split(r'/', data.decode('utf-8'))
                    # 0 - hy, 1 - hz, 2 - wy, 3 - hy

                    a1 = float(splitted[0]) / 10
                    a2 = float(splitted[2]) / 10
                    a3 = float(splitted[3]) / 10
                    rot = float(splitted[1]) * -3
                    a4 = float(splitted[4])
                    a5 = float(splitted[5])
                    return (a1,2,3, rot, a4, a5)
                except:
                    pass



if __name__ == "__main__":
    NT = NetTool("192.168.137.35", "192.168.137.247")
    print(NT.GetSockets())