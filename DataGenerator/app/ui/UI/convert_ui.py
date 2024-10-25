import os

path = os.path.dirname(__file__)
print(path)
env = "/BlenderProcPython"

for name in os.listdir(path):
    if ".ui" in name:
        src = "{}/{}".format(path, name)
        dest = "{}/{}".format(os.path.dirname(path), name.replace(".ui", ".py"))
        print(src, dest)
        os.system("{}/bin/activate&pyside2-uic {} > {}".format(env, src, dest))
    
    if ".qrc" in name:
        src = "{}/{}".format(path, name)
        dest = "{}/{}".format(os.path.dirname(path), name.replace(".qrc", "_rc.py"))
        print(src, dest)
        os.system("{}/bin/activate&pyside2-rcc {} > {}".format(env, src, dest))




