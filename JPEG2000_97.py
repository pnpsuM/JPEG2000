# %%
filter = '97'
import jpeg2000func_97 as f97
import numpy as np

PXL_NUM = 512

file = open("lena.raw", 'rb')
out = open(f"outputs\lena_DWT_{filter}.raw", 'wb')
outimg = open(f"outputs\lena_IDWT_{filter}.raw", 'wb')
image = np.fromfile(file, dtype = 'uint8')
image = np.reshape(image, [PXL_NUM, PXL_NUM])

outdata = np.zeros(shape = [PXL_NUM, PXL_NUM], dtype = 'uint8')
outimage = np.zeros(shape = [PXL_NUM, PXL_NUM], dtype = 'uint8')
DWTdata = np.zeros(shape = [PXL_NUM, PXL_NUM])
for y in range(PXL_NUM):
    for x in range(PXL_NUM):
        DWTdata[y, x] = image[y, x]
# %%
SIZE_X = int(PXL_NUM)
SIZE_Y = int(PXL_NUM)
LPFpadded = np.zeros(shape = [PXL_NUM + 8, PXL_NUM + 8])
HPFpadded = np.zeros(shape = [PXL_NUM + 8, PXL_NUM + 8])
LPFdata = np.zeros(shape = [PXL_NUM, PXL_NUM])
HPFdata = np.zeros(shape = [PXL_NUM, PXL_NUM])

ILPFpadded = np.zeros(shape = [PXL_NUM + 8, PXL_NUM + 8])
IHPFpadded = np.zeros(shape = [PXL_NUM + 8, PXL_NUM + 8])
ILPFdata = np.zeros(shape = [PXL_NUM, PXL_NUM])
IHPFdata = np.zeros(shape = [PXL_NUM, PXL_NUM])

ILPFdataL = np.zeros(shape = [PXL_NUM, PXL_NUM])
ILPFdataH = np.zeros(shape = [PXL_NUM, PXL_NUM])
IHPFdataL = np.zeros(shape = [PXL_NUM, PXL_NUM])
IHPFdataH = np.zeros(shape = [PXL_NUM, PXL_NUM])

ILdata = np.zeros(shape = [PXL_NUM, PXL_NUM])
IHdata = np.zeros(shape = [PXL_NUM, PXL_NUM])
    
# DWT
def DWT(SIZE_X, SIZE_Y, LPFpadded, HPFpadded, LPFdata, HPFdata, DWTdata, cycle):
    while cycle > 0:
        f97.Padding(SIZE_X, SIZE_Y, LPFpadded, DWTdata)
        f97.Padding(SIZE_X, SIZE_Y, HPFpadded, DWTdata)
        f97.getL(SIZE_X, SIZE_Y, LPFdata, LPFpadded)
        f97.getH(SIZE_X, SIZE_Y, HPFdata, HPFpadded)
        SIZE_X = int(SIZE_X / 2)
        
        f97.Padding(SIZE_X, SIZE_Y, LPFpadded, LPFdata)
        f97.Padding(SIZE_X, SIZE_Y, HPFpadded, LPFdata)
        f97.getLLLH(SIZE_X, SIZE_Y, DWTdata, LPFdata, LPFpadded, HPFpadded)
        f97.Padding(SIZE_X, SIZE_Y, LPFpadded, HPFdata)
        f97.Padding(SIZE_X, SIZE_Y, HPFpadded, HPFdata)
        f97.getHLHH(SIZE_X, SIZE_Y, DWTdata, HPFdata, LPFpadded, HPFpadded)
        SIZE_Y = int(SIZE_Y / 2)
        cycle -= 1
    
    print("DWT Done")
    for y in range(PXL_NUM):
        for x in range(PXL_NUM):
            outdata[y, x] = int(DWTdata[y, x])
#IDWT
def IDWT(SIZE_X, SIZE_Y, IHPFpadded, ILPFpadded, ILPFdataL, ILPFdataH, IHPFdataL, IHPFdataH, DWTdata):
    SIZE_X = int(SIZE_X / (2**num))
    SIZE_Y = int(SIZE_Y / (2**num))
    cnt = 0
    
    while cnt < num:
        f97.LVL1Interp(SIZE_X, SIZE_Y, ILPFdataL, ILPFdataH, IHPFdataL, IHPFdataH, DWTdata)
        SIZE_Y *= 2
        f97.Padding(SIZE_X, SIZE_Y, IHPFpadded, IHPFdataL)    
        f97.Padding(SIZE_X, SIZE_Y, ILPFpadded, ILPFdataL)
        f97.I_getLH(SIZE_X, SIZE_Y, ILPFdata, IHPFpadded, ILPFpadded)             
        f97.Padding(SIZE_X, SIZE_Y, IHPFpadded, IHPFdataH)
        f97.Padding(SIZE_X, SIZE_Y, ILPFpadded, ILPFdataH)
        f97.I_getLH(SIZE_X, SIZE_Y, IHPFdata, IHPFpadded, ILPFpadded)
        f97.LVL2Interp(SIZE_X, SIZE_Y, ILdata, ILPFdata, IHdata, IHPFdata)
        SIZE_X *= 2
        f97.Padding(SIZE_X, SIZE_Y, IHPFpadded, IHdata)
        f97.Padding(SIZE_X, SIZE_Y, ILPFpadded, ILdata)
        f97.I_getOrig(SIZE_X, SIZE_Y, DWTdata, IHPFpadded, ILPFpadded)
        cnt += 1
       
    print("IDWT Done") 
    for y in range(PXL_NUM):
        for x in range(PXL_NUM):
            outimage[y, x] = int(DWTdata[y, x])
            
def MSE():
    err_rate = 0
    for y in range(PXL_NUM):
        for x in range(PXL_NUM):
            err_rate += (image[y][x] - DWTdata[y][x])**2
    err_rate /= PXL_NUM**2
    return err_rate
# %%
print("input the number of DWT cycles : ")
cycle = int(input())
num = cycle

DWT(SIZE_X, SIZE_Y, LPFpadded, HPFpadded, LPFdata, HPFdata, DWTdata, cycle)
IDWT(SIZE_X, SIZE_Y, IHPFpadded, ILPFpadded, ILPFdataL, ILPFdataH, IHPFdataL, IHPFdataH, DWTdata)

outdata.tofile(out)
outimage.tofile(outimg)
# %%
file.close()
out.close()
outimg.close()
print("Level", num, "DWT/IDWT is Done!")
print(f"MSE error rate : {MSE():.5f} %")
# %%
