# %%
import numpy as np

lpf = np.array([0.02674875741080976, -0.01686411844287495, -0.07822326652898785, 0.2668641184428723, 0.6029490182363579, 0.2668641184428723, -0.07822326652898785, -0.01686411844287495, 0.02674875741080976])
hpf = np.array([0, 0.09127176311424948, -0.05754352622849957, -0.5912717631142470, 1.115087052456994, -0.5912717631142470, -0.05754352622849957, 0.09127176311424948, 0])

ilpf = np.array([0, -0.09127176311424948, -0.05754352622849957, 0.5912717631142470, 1.115087052456994, 0.5912717631142470, -0.05754352622849957, -0.09127176311424948, 0])
ihpf = np.array([0.02674875741080976, 0.01686411844287495, -0.07822326652898785, -0.2668641184428723, 0.6029490182363579, -0.2668641184428723, -0.07822326652898785, 0.01686411844287495, 0.02674875741080976])
# %%
def Padding(SIZE_X, SIZE_Y, LPFpadded, data):
    for x in range(4, int(SIZE_X + 4)):
        for y in range(4):
            i = 4 - y
            LPFpadded[y, x] = data[i, x - 4]
    for x in range(4):
        for y in range(4, SIZE_Y + 4):
            i = 4 - x
            LPFpadded[y, x] = data[y - 4, i]
    for x in range(4, int(SIZE_X + 4)):
        for y in range(SIZE_Y + 4, SIZE_Y + 8):
            i = SIZE_Y + (SIZE_Y - y)
            LPFpadded[y, x] = data[i, x - 4]
    for x in range(int(SIZE_X + 4), int(SIZE_X + 8)):
        for y in range(4, int(SIZE_Y + 4)):
            i = SIZE_X + (SIZE_X - x)
            LPFpadded[y, x] = data[y - 4, i]
    for x in range(4, int(SIZE_X + 4)):
        for y in range(4, SIZE_Y + 4):
            LPFpadded[y, x] = data[y - 4, x - 4]
# LVL 1
def getL(SIZE_X, SIZE_Y, data, LPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += lpf[index] * LPFpadded[y + 4, x + index]
    for y in range(SIZE_Y):
        for x in range(int(SIZE_X / 2)):
            data[y, x] = data[y, 2 * x]
def getH(SIZE_X, SIZE_Y, data, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += hpf[index] * HPFpadded[y + 4, x + index]
    for y in range(SIZE_Y):
        for x in range(int(SIZE_X / 2)):
            data[y, x] = data[y, 2 * x + 1]
# LVL 2
def getLLLH(SIZE_X, SIZE_Y, DWTdata, data, LPFpadded, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += lpf[index] * LPFpadded[y + index, x + 4]
    for x in range(SIZE_X): # LL
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y, x] = data[y * 2, x]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += hpf[index] * HPFpadded[y + index, x + 4]
    for x in range(SIZE_X): # LH
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y + int(SIZE_Y / 2), x] = data[y * 2 + 1, x]
def getHLHH(SIZE_X, SIZE_Y, DWTdata, data, LPFpadded, HPFpadded):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += lpf[index] * LPFpadded[y + index, x + 4]
    for x in range(SIZE_X): # HL
        for y in range(int(SIZE_Y / 2)):
            DWTdata[y, x + SIZE_X] = data[y * 2, x]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            data[y, x] = 0
            for index in range(9):
                data[y, x] += hpf[index] * HPFpadded[y + index, x + 4]
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
            for index in range(9):
                data[y, x] += ilpf[index] * ILPFpadded[y + index, x + 4]
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            for index in range(9):
                data[y, x] += ihpf[index] * IHPFpadded[y + index, x + 4]       
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
            for index in range(9):
                DWTdata[y, x] += ilpf[index] * ILPFpadded[y + 4, x + index]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            for index in range(9):
                DWTdata[y, x] += ihpf[index] * IHPFpadded[y + 4, x + index]
# %%