# %%
import numpy as np

lpf = np.array([-0.125,0.25,0.75,0.25,-0.125])
hpf = np.array([0, -0.5, 1, -0.5, 0])

ilpf = np.array([0, 0.5, 1, 0.5, 0])
ihpf = np.array([-0.125, -0.25, 0.75, -0.25, -0.125])
# %%
def Padding(SIZE_X, SIZE_Y, LPFpadded, data):
    for x in range(2, int(SIZE_X + 2)):
        for y in range(2):
            i = 2 - y
            LPFpadded[y, x] = data[i, x - 2]
    for x in range(2):
        for y in range(2, SIZE_Y + 2):
            i = 2 - x
            LPFpadded[y, x] = data[y - 2, i]
    for x in range(2, int(SIZE_X + 2)):
        for y in range(SIZE_Y + 2, SIZE_Y + 4):
            i = SIZE_Y + (SIZE_Y - y)
            LPFpadded[y, x] = data[i, x - 2]
    for x in range(int(SIZE_X + 2), int(SIZE_X + 4)):
        for y in range(2, int(SIZE_Y + 2)):
            i = SIZE_X + (SIZE_X - x)
            LPFpadded[y, x] = data[int(y - 2), i]
    for x in range(2, int(SIZE_X + 2)):
        for y in range(2, SIZE_Y + 2):
            LPFpadded[y, x] = data[y - 2, x - 2]
# LVL 1
def getL(SIZE_X, SIZE_Y, data, LPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += lpf[index] * LPFpadded[y + 2, x + index]
    for y in range(SIZE_Y):
        for x in range(int(SIZE_X / 2)):
            data[y, x] = data[y, 2 * x]
def getH(SIZE_X, SIZE_Y, data, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += hpf[index] * HPFpadded[y + 2, x + index]
    for y in range(SIZE_Y):
        for x in range(int(SIZE_X / 2)):
            data[y, x] = data[y, 2 * x + 1]
# LVL 2
def getLLLH(SIZE_X, SIZE_Y, DWTdata, data, LPFpadded, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += lpf[index] * LPFpadded[y + index, x + 2]
    for x in range(SIZE_X): # LL
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y, x] = data[y * 2, x]
            
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += hpf[index] * HPFpadded[y + index, x + 2]
    for x in range(SIZE_X): # LH
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y + int(SIZE_Y / 2), x] = data[y * 2 + 1, x]
def getHLHH(SIZE_X, SIZE_Y, DWTdata, data, LPFpadded, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += lpf[index] * LPFpadded[y + index, x + 2]
    for x in range(SIZE_X): # HL
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y, x + SIZE_X] = data[y * 2, x]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += hpf[index] * HPFpadded[y + index, x + 2]
    for x in range(SIZE_X): # HH
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y + int(SIZE_Y / 2), x + SIZE_X] = data[y * 2 + 1, x]
# %%
# IDWT func.
def LVL1Interp(SIZE_X, SIZE_Y, ILPFdataL, ILPFdataH, IHPFdataL, IHPFdataH, DWTdata):
    for y in range(SIZE_Y): # LL to LPFdataL
        for x in range(SIZE_X):
            ILPFdataL[y * 2, x] = DWTdata[y, x]
            ILPFdataL[y * 2 + 1, x] = 0
    for y in range(SIZE_Y): # HL to LPFdataH
        for x in range(SIZE_X):
            ILPFdataH[y * 2, x] = DWTdata[y, x + SIZE_X]
            ILPFdataH[y * 2 + 1, x] = 0
    for y in range(SIZE_Y): # LH to HPFdataL
        for x in range(SIZE_X):
            IHPFdataL[y * 2 + 1, x] = DWTdata[y + SIZE_Y, x]
            IHPFdataL[y * 2, x] = 0
    for y in range(SIZE_Y): # HH to HPFdataH
        for x in range(SIZE_X):
            IHPFdataH[y * 2 + 1, x] = DWTdata[y + SIZE_Y, x + SIZE_X]
            IHPFdataH[y * 2, x] = 0          
def I_getLH(SIZE_X, SIZE_Y, data, IHPFpadded, ILPFpadded): # I@PFdata@ to @data
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            data[y, x] = 0
            for index in range(5):
                data[y, x] += ilpf[index] * ILPFpadded[y + index, x + 2]
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            for index in range(5):
                data[y, x] += ihpf[index] * IHPFpadded[y + index, x + 2]       
def LVL2Interp(SIZE_X, SIZE_Y, ILdata, ILPFdata, IHdata, IHPFdata):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            ILdata[y, x * 2] = ILPFdata[y, x]
            ILdata[y, x * 2 + 1] = 0
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            IHdata[y, x * 2 + 1] = IHPFdata[y, x]
            IHdata[y, x * 2] = 0
def I_getOrig(SIZE_X, SIZE_Y, DWTdata, IHPFpadded, ILPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            DWTdata[y, x] = 0
            for index in range(5):
                DWTdata[y, x] += ilpf[index] * ILPFpadded[y + 2, x + index]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            for index in range(5):
                DWTdata[y, x] += ihpf[index] * IHPFpadded[y + 2, x + index]
# %%