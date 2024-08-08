import pygame, psutil, time

class Main:
    def __init__(self):
        self.bandwithCounter = BandwithCounter()
        self.window = Window(5, ((0, 0, 0), (255, 255, 255)))
        self.loop()
    def loop(self):
        while True:
            self.bandwithCounter.process()
            self.window.process(self.bandwithCounter)
            pygame.display.flip()

class BandwithCounter:  
    def __init__(self):
        self.refreshRate = 0.5
        self.timer1 = time.perf_counter()
        self.timer2 = 0
        self.oldDataSent = 0
        self.oldDataRecv = 0
        self.totalDataSent = 0
        self.totalDataRecv = 0
        self.convertedDataSent = 0
        self.convertedTotalDataSent = 0        
        self.convertedDataRecv = 0
        self.convertedTotalDataRecv = 0
    def convertToGb(self, value):
        return value/1024./1024./1024.*8
    def getDataUsage(self):
        self.dataSent = psutil.net_io_counters().bytes_sent
        self.dataRecv = psutil.net_io_counters().bytes_recv
        if(self.oldDataSent != 0):
            self.totalDataSent += self.dataSent - self.oldDataSent
        if(self.oldDataRecv != 0):
            self.totalDataRecv += self.dataRecv - self.oldDataRecv
    def returnDataUsage(self):
        if(self.oldDataSent != 0):
            self.convertedDataSent = self.convertToGb(self.dataSent - self.oldDataSent)
            self.convertedDataSent = '%0.3f' % self.convertedDataSent
            self.convertedTotalDataSent = '%0.3f' % self.convertToGb(self.totalDataSent)
        if(self.oldDataRecv != 0):            
            self.convertedDataRecv = self.convertToGb(self.dataRecv - self.oldDataRecv)
            self.convertedDataRecv = '%0.3f' % self.convertedDataRecv
            self.convertedTotalDataRecv = '%0.3f' % self.convertToGb(self.totalDataRecv)
    def resetOldValue(self):
        self.oldDataSent = self.dataSent
        self.oldDataRecv = self.dataRecv
    def timerCheck(self):
        self.timer2 = time.perf_counter()
        if(self.timer2 - self.timer1 >= self.refreshRate):
            self.timer1 = time.perf_counter()
            self.timer2 = 0            
            return True
        else:
            return False
    def process(self):
        if(self.timerCheck()):
            self.getDataUsage()
            self.returnDataUsage()
            self.resetOldValue()
        
class Window:
    def __init__(self, scale, colorScheme):
        pygame.init()
        self.scale = scale
        self.colorScheme = colorScheme
        self.font1 = pygame.font.SysFont("Roboto", self.scale * 6)
        self.font2 = pygame.font.SysFont("Roboto", self.scale * 12)
        self.screen = pygame.display.set_mode((self.scale * 200, self.scale * 120)) 
        pygame.display.set_caption('Bandwith Counter')
        pygame.display.set_icon(pygame.image.load('icon.ico'))
    def display(self, bandwithCounter):
        self.screen.fill(self.colorScheme[1])
        self.screen.blit(self.font1.render('Q/W - change scale\nA/S - change refresh rate\nC - change theme', 1, self.colorScheme[0]), (self.scale * 134, self.scale * 98))
        self.screen.blit(self.font1.render(f'scale: {self.scale}\nrefresh rate: {round(bandwithCounter.refreshRate, 4)}s', 1, self.colorScheme[0]), ((self.scale * 2), (self.scale * 105)))
        self.screen.blit(self.font2.render(f'{bandwithCounter.convertedDataRecv}gb recieved', 1, self.colorScheme[0]), (self.scale * 2, self.scale * 2))
        self.screen.blit(self.font2.render(f'{bandwithCounter.convertedTotalDataRecv}gb total', 1, self.colorScheme[0]), (self.scale * 2, self.scale * 14))
        self.screen.blit(self.font2.render(f'{bandwithCounter.convertedDataSent}gb sent', 1, self.colorScheme[0]), (self.scale * 2, self.scale * 30))     
        self.screen.blit(self.font2.render(f'{bandwithCounter.convertedTotalDataSent}gb total', 1, self.colorScheme[0]), (self.scale * 2, self.scale * 42))   
    def process(self, bandwithCounter):
        for event in pygame.event.get():
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_q):
                    if(self.scale > 1):
                        self.__init__(self.scale - 1, self.colorScheme)
                if(event.key == pygame.K_w):
                    if(self.scale < 25):
                        self.__init__(self.scale + 1, self.colorScheme)
                if(event.key == pygame.K_a):
                    if(bandwithCounter.refreshRate > 0.2):
                        bandwithCounter.refreshRate -= 0.1
                if(event.key == pygame.K_s):
                    if(bandwithCounter.refreshRate < 9.9):
                        bandwithCounter.refreshRate += 0.1                        
                if(event.key == pygame.K_c):
                    if(self.colorScheme[0] == (0, 0, 0)):
                        self.colorScheme = ((255, 255, 255), (0, 0, 0))
                    else:
                        self.colorScheme = ((0, 0, 0), (255, 255, 255))
            if(event.type == pygame.QUIT):
                pygame.quit()
        self.display(bandwithCounter)


    
        
main = Main()

