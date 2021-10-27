import os
HomeDir = os.getcwd()
DirList = os.listdir(HomeDir)
for Dir in DirList:
    if Dir.find(".py") == -1:
        os.chdir(HomeDir + "/" + Dir)
        print(os.getcwd())
        FileList = os.listdir(HomeDir + "/" + Dir)
        sch = 1
        for File in FileList:
            os.rename(File, str(sch) + ".JPG")
            sch += 1