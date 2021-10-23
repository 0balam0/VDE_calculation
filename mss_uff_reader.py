import pandas as pd
import numpy as np
class Cycle():
    def __init__(self):
        Ldir = r'./cycle/uff/' # location dir ufficial file
        self.name = ''
        self.File = {'name': '', 'dir':Ldir, 'f':None}
        self.info = {}

    def ReadGofastFile(self):
        self.readInfoGofast()
        self.readDataGofast()

    # metodi lettura txt
    def open(self, File = None):
        try:
            self.File['f'] = open(self.File['dir'] + self.File['name'])
        except:
            print('File non aperto!!!')

    def close(self):
        self.File['f'].close()

    def readline(self):
        return self.File['f'].readline()

    # metodi lettura file Gofast
    def searchGofastSection(self, filter = 'Info'):
        self.open()
        found = False
        for k,line in enumerate(self.File['f']):
            if '<'+filter+'>' in line:
                found = True
                break
        start = k
        for k,line in enumerate(self.File['f']):
            if '</'+filter+'>' in line:
                found = True
                break
        stop = k
        self.close()
        return start, stop

    def readInfoGofast(self):
        start, stop = self.searchGofastSection(filter='Info')
        self.open()
        for i in range(0, start+1):
            self.readline()
        for i in range(start+1, stop-1):
            line = self.readline()
            splitLine = line.split()
            if len(splitLine) >= 2:
                self.info[splitLine[0]] = splitLine[1]
            else :
                self.info[splitLine[0]] = '???'
        self.close()

        self.name = self.info.get('mss_Ciclo', '???')

    def readDataGofast(self):
        start, stop = self.searchGofastSection(filter='Dati')
        self.open()
        for i in range(0, start+1):
            self.readline()
        FieldName = self.readline().lower().split('\t')
        FieldUnit = self.readline().split('\t')
        columns = zip(FieldName, FieldUnit)
        df = pd.read_csv(self.File['dir'] + self.File['name'], sep='\t', skiprows=start + 3, nrows=stop - start - 3,
                         header=None)
        df = pd.DataFrame(df.values, columns=FieldName)
        self.Data = df
        self.unit = columns

    def AccEvaluation(self):
        dt = np.gradient(self.Data['time'], self.Data['time'])# self.Data['time'].diff()
        acc = np.gradient(self.Data['speed']/3.6, self.Data['time']) #self.Data['speed'].diff()/3.6
        # acc = dv/dt
        # acc[0] = 0
        # dt[0] = 0
        self.Data['dt'] = dt
        self.Data['acc'] = acc


if __name__ == "__main__":
    print('ciao')
    cycle = Cycle()
    cycle.File['name'] = r'Custom_MCT_UHU R_USA - BEVER_Template (TEST).mss'
    cycle.RaadGofastFile()


