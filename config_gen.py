'''
Author: your name
Date: 2022-03-16 09:31:25
LastEditTime: 2022-03-16 09:55:27
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \AI制药\分子对接脚本\脚本_version1\config_gen.py
'''
"""
根据用户输入生成config.txt文件

receptor = protein.pdbqt
ligand = ligend.pdbqt

center_x = -18.955
center_y = -5.188
center_z = 8.617
size_x = 40
size_y = 40
size_z = 40
energy_range =  4
exhaustiveness = 8

也可以读取excel，生成config
"""
import os
import sys
import random
import pandas as pd

def gen_config_file(output_name="./Config", ligand="ligand.pdbqt",receptor="protein.pdbqt",x=8, y=-8, z=8, size_x=40,size_y=40, size_z=40,energy_range =  4,exhaustiveness = 8):
    """

    :param output_name: 输出路径名 "./Config"
    :param x: x坐标
    :param y: y坐标
    :param z: z坐标
    :param size: 盒子大小
    :param energy_range  exhaustiveness ligand 配体文件名a.pdbqt receptor:受体文件名b.pdbqt
    """
    #新建的config文件名
    config_name = output_name+ os.sep + ligand[0:-6] +"_" + receptor[0:-6] + str(random.randint(1,50)) +".txt"
    with open(config_name, "w", encoding='UTF-8') as f:
        f.writelines("receptor = " + str(receptor) + "\n")
        f.writelines("ligand = " + str(ligand) + "\n")
        f.writelines("center_x = " + str(x) + "\n")
        f.writelines("center_y = " + str(y) + "\n")
        f.writelines("center_z = " + str(z) + "\n")
        f.writelines("size_x = " + str(size_x) + "\n")
        f.writelines("size_y = " + str(size_x) + "\n")
        f.writelines("size_z = " + str(size_x) + "\n")
        f.writelines("exhaustiveness = " + str(exhaustiveness) + "\n")
        f.writelines("energy_range = " + str(energy_range) + "\n")
        


def write_excel(excel_name="./input.xlsx",output_name="./Config"):
    """
    将excel中的参数转换为config.txt文件
    ：param excel_name：execl文件夹名 "./input.xlsx"
    :param output_name config文件夹名 "./Config"
    """
    # 3.读取excel的某一个sheet
    df = pd.read_excel(excel_name, sheet_name='Sheet1')
    print(df.columns)
    print(df.index)
    for indexs in df.index:
        print(df.loc[indexs].values)
        conf = df.loc[indexs].values
        config_name = output_name+ os.sep + conf[0]+".txt"
        with open(config_name, "w", encoding='UTF-8') as f:
            f.writelines("receptor = " + str(conf[1]) + "\n")
            f.writelines("ligand = " + str(conf[2]) + "\n")
            f.writelines("center_x = " + str(conf[3]) + "\n")
            f.writelines("center_y = " + str(conf[4]) + "\n")
            f.writelines("center_z = " + str(conf[5]) + "\n")
            f.writelines("size_x = " + str(conf[6]) + "\n")
            f.writelines("size_y = " + str(conf[7]) + "\n")
            f.writelines("size_z = " + str(conf[8]) + "\n")
            f.writelines("exhaustiveness = " + str(conf[9]) + "\n")
            f.writelines("energy_range = " + str(conf[10]) + "\n")

if __name__ == "__main__":
    gen_config_file()
    write_excel()