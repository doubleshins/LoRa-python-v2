#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import serial
import mraa

COM_PORT = '/dev/ttyUSB0'
BAUD_RATES = 115200
ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=10)

loraflag = 0


def Fun_CRC(data):
    crc = 0
    for i in data:
        crc = crc ^ i
    return crc


def FunLora_0_GetChipID():
    #print("讀取F/W版本及Chip ID")
    ser.write(serial.to_bytes([0x80, 0x00, 0x00, 0x80]))
    data = ser.read(10)
    #print(data.encode('hex'))
    if str(data[3].encode('hex')) == "c1":
        global loraflag
        loraflag += 1
    else:
        print("FunLora_0_GetChipID error")


def FunLora_1_Init():
    #print("重置 & 初始化")
    ser.write(serial.to_bytes([0xC1, 0x01, 0x00, 0xC0]))
    data = ser.read(5)
    #print(data.encode('hex'))
    if str(data[1].encode('hex')) == "aa":
        global loraflag
        loraflag += 1
    else:
        print("FunLora_1_Init error")


def FunLora_2_ReadSetup():
    #print("讀取設定狀態")
    ser.write(serial.to_bytes([0xC1, 0x02, 0x00, 0xC3]))
    data = ser.read(12)
    #print(data.encode('hex'))
    if str(data[1].encode('hex')) == "82":
        global loraflag
        loraflag += 1
    else:
        print("FunLora_2_ReadSetup error")


def FunLora_3_RX():
    #print("設定 RX (W)_IN 接收端")
    # freq 920.00MHz
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x03, 0x01, 0x67, 0x60, 0x0F,
                         0xCD]))
    data = ser.read(5)
    #print(data.encode('hex'))
    if str(data[1].encode('hex')) == "aa":
        global loraflag
        loraflag += 1
    else:
        print("FunLora_3_RX error")


def FunLora_3_TX():
    #print("設定 TX (R)_OUT 發送端")
    # freq 920.00MHz
    ser.write(
        serial.to_bytes([0xC1, 0x03, 0x05, 0x02, 0x01, 0x67, 0x60, 0x0F,
                         0xCC]))
    data = ser.read(5)
    #print(data.encode('hex'))
    if str(data[1].encode('hex')) == "aa":
        global loraflag
        loraflag += 1
    else:
        print("FunLora_3_TX error")


def FunLora_ckinit():
    if loraflag == 4:
        print("Init success")
        print("")
    else:
        print("Init error")
        print("")


def FunLora_6_redata():
    print("讀取資料")
    ser.write(serial.to_bytes([0xC1, 0x06, 0x00, 0xC7]))
    data = ser.read(38)
    print(data.encode('hex'))
    print("")
   
    num_list = [(int(data[i].encode('hex'), 16)) for i in range(0, 38)]
    print "rssi", num_list[36]
    print "crc", num_list[37]

    ck_list = [(int(data[i].encode('hex'), 16)) for i in range(0, 37)]
    ckcrc = Fun_CRC(ck_list)
    print "ckcrc", ckcrc

    if num_list[37] == ckcrc:
        print("=====success===")
    else:
        print("=====error=====")


def FunLora_5_write_test():
    # * 寫入資料
    print("寫入資料")
    ser.write(
        serial.to_bytes([
            0xC1, 0x05, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x01, 0x01, 0xE4
        ]))
    data = ser.read(5)
    print(data.encode('hex'))


def loraswitch():
    pin = mraa.Gpio(17)
    pin.dir(mraa.DIR_IN)
    x = pin.read()
    return x


# 檢查是否有資料進來
def Fun_ckonoff():
    while True:
        dataled = loraswitch()
        print dataled  #低電位 0
        if dataled == 1:  #有資料
            FunLora_6_redata()
            break
        time.sleep(1)


FunLora_0_GetChipID()
FunLora_1_Init()
FunLora_2_ReadSetup()
FunLora_3_RX()
#FunLora_3_TX()

FunLora_ckinit()

#FunLora_6_redata()
#FunLora_5_write_test()
Fun_ckonoff()

ser.close()
