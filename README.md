# readme 

vina分子对接脚本（大批量的分子对接）
 * 安装环境：
   ``
   pip install shutil  

pip install  tqdm
``


1、将配体(pdbqt格式，单个/多个都可以)放到Ligands文件夹中。

2、将受体(pdbqt格式，单个/多个都可以)放到Proteins文件夹中。

3、将config.txt(单个或多个)放到Config文件夹中
4、在命令行输入如下指令：
python3 ./main.py
将进行对接:
5、对接结果将会在Output文件夹下每个config.txt对应生成一个configout文件夹，蛋白质配体、受体、以及结果保存在该文件夹下
