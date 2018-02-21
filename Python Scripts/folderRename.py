import os

scriptFolder = os.path.dirname(os.path.realpath(__file__))
files = os.listdir(scriptFolder)

print(scriptFolder)
test = "folderRename.py"
for item in files:
    print(item)
    if "_Albedo" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_Albedo" + ".dds")

    if "_Roughness" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_Roughness" + ".dds")

    if "_Normals" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_Normals" + ".dds")

    if "_Metallic" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_Metallic" + ".dds")

    if "_Emissive" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_Emissive" + ".dds")

    if "_AmbientOcclusion" in item:
        print("inside:" + item)
        os.rename(scriptFolder + "/" + item, scriptFolder + "/" + os.path.basename(scriptFolder) + "_AmbientOcclusion" + ".dds")

