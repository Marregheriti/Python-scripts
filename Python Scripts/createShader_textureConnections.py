#   This scripts creates a Blinn shader and assigns
#   all textures from the File Dialog window into
#   the correct PBR slots in Maya.
#
#   For this to work it assumes:
#   -An object has been selected
#   -Textures have .dds file endings
#   -Textures are correctly named Object_Albedo/Emissive/Roughness, etc...
#       (for instance: pCube1_Roughness.dds)

#changed to TGA cause Marre needs it


import pymel.core as pm
from os import listdir

def main():
    selectionList = pm.ls(sl=True)


    basicFilter = "Image Files (*.TGA *.tga *.DDS *.dds *.PNG *.png)"
    path = pm.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=3)
    files = listdir(path[0])
    ddsFiles = []
    for item in files:
        fileEndings = ('.TGA', '.tga', '.DDS', '.dds', '.PNG', '.png')
        if (item.endswith(fileEndings)):
            ddsFiles.append(item)



    for obj in selectionList:
        shader = pm.shadingNode('phong', n=obj + "Shader", asShader=True)

        pm.select(obj)
        pm.hyperShade(assign=shader)
        if obj.find("_lod") !=-1:
            lodName = obj.split("_")
            shaderConnections(ddsFiles, lodName[0], shader, path)
        else:
            shaderConnections(ddsFiles, obj, shader, path)

        connections = pm.listConnections(shader, destination=False, source=True)
        if len(connections) < 6:

            errorstring = ""

            errorstring += ("# ===============================")
            errorstring += ("\n# %s texture(s) missing:" %str(6-len(connections)))
            errorstring += ("\n# ===============================")

            if len(pm.listConnections(shader+".color", destination=False, source=True)) < 1:
                errorstring += ("\n# - Albedo was not found!")

            if len(pm.listConnections(shader+".ambientColor", destination=False, source=True)) < 1:
                errorstring += ("\n# - Ambient Occlusion was not found!")

            if len(pm.listConnections(shader + ".incandescence", destination=False, source=True)) < 1:
                errorstring += ("\n# - Emissive was not found!")

            if len(pm.listConnections(shader+".normalCamera", destination=False, source=True)) < 1:
                errorstring += ("\n# - Normal Map was not found!")

            if len(pm.listConnections(shader + ".reflectedColor", destination=False, source=True)) < 1:
                errorstring += ("\n# - Metallic was not found!")

            if len(pm.listConnections(shader + ".specularColor", destination=False, source=True)) < 1:
                errorstring += ("\n# - Roughness was not found!")

            pm.confirmDialog(message=errorstring)
        else:
            victorystring = "All textures have been successfully linked!"
            pm.confirmDialog(message=victorystring)
        # pm.delete(shader) <-- use this if you want to remove
        # the shader after you're done with exporting everything

def shaderConnections(ddsFiles, obj, shader, path):
    for s in ddsFiles:
        if "_Albedo" in s and str(obj) in s:
            fileTexNode = pm.shadingNode('file', n='AlbedoFileTex', asTexture=True)
            pm.connectAttr(fileTexNode + '.outColor', shader + '.color')
            pm.setAttr('%s.fileTextureName' % fileTexNode, path[0] + "\\" + s, type='string')
        elif "_AmbientOcclusion" in s and str(obj) in s:
            fileTexNode = pm.shadingNode('file', n="AOFileTex", asTexture=True)
            pm.connectAttr(fileTexNode + ".outColor", shader + ".ambientColor")
            pm.setAttr("%s.fileTextureName" % fileTexNode, path[0] + "\\" + s, type="string")
        elif "_Emissive" in s and str(obj) in s:
            fileTexNode = pm.shadingNode("file", n="EmissiveFileTex", asTexture=True)
            pm.connectAttr(fileTexNode + ".outColor", shader + ".incandescence")
            pm.setAttr("%s.fileTextureName" % fileTexNode, path[0] + "\\" + s, type="string")
        elif "_Normals" in s and str(obj) in s:
            bumpNode = pm.shadingNode('bump2d', n='NormalsBumpNode', asUtility=True)
            fileTexNode = pm.shadingNode('file', n="NormalsFileTex", asTexture=True)
            pm.setAttr(bumpNode + ".bumpInterp", 1)
            pm.connectAttr(fileTexNode + ".outAlpha", bumpNode + ".bumpValue")
            pm.connectAttr(bumpNode + ".outNormal", shader + ".normalCamera")
            pm.setAttr('%s.fileTextureName' % fileTexNode, path[0] + "\\" + s, type='string')
        elif "_Metallic" in s and str(obj) in s:
            fileTexNode = pm.shadingNode("file", n='MetallicFileTex', asTexture=True)
            pm.connectAttr(fileTexNode + ".outColor", shader + ".reflectedColor")
            pm.setAttr("%s.fileTextureName" % fileTexNode, path[0] + "\\" + s, type="string")
        elif "_Roughness" in s and str(obj) in s:
            fileTexNode = pm.shadingNode("file", n="RoughnessFileTex", asTexture=True)
            pm.connectAttr(fileTexNode + ".outColor", shader + ".specularColor")
            pm.setAttr("%s.fileTextureName" % fileTexNode, path[0] + "\\" + s, type="string")