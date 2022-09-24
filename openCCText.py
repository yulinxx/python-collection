from opencc import OpenCC
import time

def transText(file, newFile):
    index = 0
    covT = OpenCC('s2t')  # 转繁体
    covTW = OpenCC('s2tw')  # 转台湾繁体
    covHK = OpenCC('s2hk')  # 转香港繁体

    with open(file, "r", encoding="utf-8") as f1, open(newFile, "w", encoding="utf-8") as f2:
        for line in f1:
            index += 1
            if index % 200 == 0:
                print(f'Line{index}')

            f2.write(line)

            t = covT.convert(line)
            if t != line:
                f2.write(t)

            tw = covTW.convert(line)
            if t != tw:
                f2.write(t)

            hk = covHK.convert(line)
            if hk != tw:
                f2.write(hk)


if __name__ == '__main__':
    time_start = time.time()

    filename = 'D:/april/Downloads/clover.schema-1.1.4/THUOCL_car.dict.yaml'
    filenameN = 'D:/april/Downloads/clover.schema-1.1.4/THUOCL_car.dict.yaml_'

    transText(filename, filenameN)

    time_end = time.time()
    print(f'End ,time cost {time_end-time_start} s')


