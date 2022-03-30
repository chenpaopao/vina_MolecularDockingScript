'''
Author: your name
Date: 2022-03-16 08:50:29
LastEditTime: 2022-03-30 17:37:39
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \AI制药\分子对接脚本\脚本_version1\main.py
'''
import shutil
import os
import sys
from tqdm import tqdm

## 分子对接命令
def vina_dock(output_dir,ligand, protein, config):
    """
    使用vina命令进行对接
    :param output_dir:输出的文件夹（将对接完成的分子以及log日志放到该文件）
    :param ligand: 配体文件名 ligand.pdbqt
    :param protein: 受体文件名 preped.pdbqt
    :param config: 配置文件名+地址 config1.txt
    :return: 返回1表示正常
    """

    cmd = "vina --ligand %s --receptor %s --config %s --log %s --out %s" % \
          (output_dir+os.sep+ligand, output_dir+os.sep+protein, config, output_dir+os.sep+"log.txt", output_dir+os.sep+"output.pdbqt")

    #print(cmd)
    return os.system(cmd)
#检查输入参数 ，后续扩展功能
def check_cmd_para(cmd_para):
    # 直接运行
    if len(cmd_para) == 1:
        return 1
    # 检查文件名
    else:
        for i in range(1,len(cmd_para)):
            proteins = cmd_para[1]
            if check_dir(proteins):
                return 1
            else:
                return 0
def check_dir(filename):
    """
    :param filename: 判断的名字
    :return: 如果是文件夹，如果存在返回1，不存在返回0。不是文件夹返回0。
    """
    if os.path.isdir(filename):
        if os.path.exists(filename):
            return 1
        else:
            return 0
    else:
        return 0
#创建文件夹
def mk_output_dir(output_path):
    """
    如果不存在就创建输出文件夹
    :param output_path: 目标文件夹
    """
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except FileExistsError:
            return
#扩展功能
def copy_proteins(src_dir, dst_dir):
    """
    将一个文件夹中的所有pdbqt格式的蛋白复制到另一个文件夹中
    :param src_dir: 原始文件夹
    :param dst_dir: 目标文件夹
    """
    for file in os.listdir(src_dir):
        if file.endswith(".pdbqt"):
            src_file = os.path.join(src_dir, file)
            shutil.copy(src_file, dst_dir)

def read_para(txtdir,para_name):
    """
    读取txtdir目标文件（txt文件），获取以para_name开头的那一行参数值
    :param txtdir: 带读取的文件夹
    :param para_name:待提取的参数值
    """
    with open(txtdir, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            if line.startswith(para_name):
                return line.split("=")[1].strip()

def pdbqt2dir(proteins_dir,ligands_dir,out_path,configname,receptor,ligands):
    """
    在output路径创建一个configname名字的文件夹，将pdbqt文件移动进去。
    :param out_path: 文件夹创建路径
    :configname:文件夹名字
    """
    # 1.创建文件夹
    out_path = out_path +os.sep + configname[0:-4]+"out"
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    # 2.复制pdbqt文件
    target_path = proteins_dir + os.sep + receptor
    if not os.path.exists(target_path):
        return False
    else:
        shutil.copyfile(target_path, out_path+os.sep+receptor)
    
    target_path = ligands_dir + os.sep + ligands
    if not os.path.exists(target_path):
        return False
    else:
        shutil.copyfile(target_path, out_path+os.sep+ligands)
    return out_path

class Main:

    def __init__(self):
        self.ligands_dir = None
        self.proteins_dir = None
        self.output_path = None

    def run(self):

        # 1.读取配体和受体
        # 输入的配体放在./Ligands文件夹
        # 指定受体文件夹
        # 输出在./Output文件夹
        # if not check_cmd_para(sys.argv):
        #     print("INFO")
        #     sys.exit()
        self.ligands_dir = "." + os.sep + "Ligands"
        #self.proteins_dir = sys.argv[1]
        self.proteins_dir = "." + os.sep + "Proteins"

        self.config_dir = "." + os.sep + "Config"
        self.output_path = "." + os.sep + "Output"

        # 2、读取config文件夹中的每一个文件每一行
        configs = tqdm(os.listdir(self.config_dir))
        for config in configs:
            configs.set_description("Processing %s" % config)
            if not config.endswith(".txt"):
                continue
            nowconfig_dir = self.config_dir+os.sep+config
            receptor = read_para(nowconfig_dir,"receptor")
            ligand = read_para(nowconfig_dir,"ligand")
            #energy_range = read_para(nowconfig_dir,"energy_range")
            #print(receptor,ligand)
            #3、根据config文件中的 ligand，receptor进行对接前的文件复制
            if not os.path.exists(self.ligands_dir + os.sep + ligand) or not os.path.exists(self.proteins_dir + os.sep + receptor):
                print("在Proteins 或 Ligands文件中不存在{}文件中所需要的蛋白质或配体".format(config))
                continue
            outpath = pdbqt2dir(self.proteins_dir,self.ligands_dir,self.output_path,config,receptor,ligand)
            #现在在output文件夹下有了configi_out的文件夹
            #4 进行对接
            vina_dock(outpath, ligand,receptor, nowconfig_dir)
        print("对接————完成")

if __name__ == '__main__':
    main = Main()
    main.run()
