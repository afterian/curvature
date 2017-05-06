import maya.cmds as cmds
import maya.mel as mel
from functools import partial

""" windows not saving my shelf buttons.
import cva
reload(cva)
cva.cvaUI()

To do:
-separate out ramp creation. add a selector for it. but also add a button for creating a default ramp like i have.
-add alpha counter to all functions.
-drive needs uv pos
-update loc to contain manual uv pos controls. 
"""
##version .06 "Lamprey" added loc array functionality. Select some things, click button, get locs at pos
##version .07 PosAtSpot ads a loc at surface pos,  def for Surface to pointOnsurface to Locater, it mainLooped will eventually be depreciated. it works now, not messing with it. But its possibly redundent.
#-addedalpha numeric counter . Currently only locAtPoint is using it.
#version .07 adjusting loccountx , y  to be able to do a single row or collum.
#adapting to pllugin changes
#version .10 going beta. Changing terminollgy so i can go opensource.

#defining global vars, I would like to find a better way to do this.
curvesel = ""
curveselShape =""
cvaName = ""
poca = ""
lastMScreated =""
globScaleRamp=""
globPosURamp=""
globPosVRamp=""
globDriveRamp=""
loccountX=""
loccountY=""
segnumX=""
segnumY=""
cva_root=""
upX=False
upY=False
upZ=True
createCAPN=True
inMode=1
myNameSpace=""
createWithAss=False
doConnectDrive=True
rayTranslate=True
rayRotate=True
rayScale=True
lampreyConnectOp=False
lampreyGetConnectOp=False
lampreyConnectNoneOp=True
masterOutGlobal=""
locAtSpot=""
paraU=""
paraV=""
cvaAlphaCounter="aaa"
alphal = '0123456789abcdefghijklmnopqrstuvwxyz'
#createNewRamps=True


#creating the main UI
def cvaUI():
    #see if window exists
    if cmds.window("cvaUI" , exists = True):
        cmds.deleteUI("cvaUI")

    #create the window
    window = cmds.window("cvaUI", title = "CurVeAture", w = 350 , h = 500 , mxb = False, sizeable = True)

    #create the mainlayout
    mainLayout = cmds.columnLayout("mainColumn", w = 350, h = 600)

    #banner image
    imagePathBanner = cmds.internalVar(upd = True) + "icons/cvaIcon.jpg"
    imagePathFolder = cmds.internalVar(upd = True) + "icons/cvaFolder.jpg"
    cmds.image(w = 350, h =60, image = imagePathBanner)

    #setting the tabs
    cmds.textField("cvaNametx",en = False, text = "NO CVA ASSIGNED")

        #Alpha Numeric counter.
    cmds.textField("cvaAlphaCounterTx", text = "aaa")
    cmds.button(command = cvaAlphaCounterSet, label = "set alpha counter", w = 350, h = 20)
    tabLayout = cmds.tabLayout("mainTabs", imw = 5, imh = 5)

    tabLayout = cmds.tabLayout("mainTabs", imw = 5, imh = 5)
    curvesel = "no surface"




    #curveAture tab
    cmds.columnLayout("CurVeAture", w = 350, h =600, parent = "mainTabs")
    cmds.textField("cva", w= 350, tx= "cva_aaa")
    cmds.button(command = getcvaName, label = "Set CVA", w = 350, h = 20)
    cmds.textField("curveseltx", w= 350, en = False, text = "NO SURFACE SELECTED")

    cmds.button(command = getcurvesel, label = "load nurbs Surface", w = 350, h = 20)

    cmds.intSliderGrp("loccountX", label = "number of locators X", minValue=1, maxValue=100, step=1, field=True, value = 2)
    cmds.intSliderGrp("loccountY", label = "number of locators Y", minValue=1, maxValue=100, step=1, field=True, value = 2)
    cmds.intSliderGrp(label = "start scale", minValue=1, maxValue=100, step=1, field=True,value = 1, en = False)
    cmds.intSliderGrp(label = "end scale", minValue=1, maxValue=100, step=1, field=True, value = 1, en = False)
    cmds.checkBox(label="Auto create with asset, see highlighted asset tab", en=False)
    cmds.checkBox(label="keep history", en=False)
    #cmds.checkBox(label="createNewRampsSel", value=True,  onCommand= createNewRampsboxOn,offCommand= createNewRampsboxOff)


    collection1 = cmds.radioCollection()
    cmds.radioButton( label='upX', sl= False, onc= getUpVectorX)
    cmds.radioButton( label='upY', sl = False, onc= getUpVectorY)
    cmds.radioButton( label='upZ', sl = True, onc= getUpVectorZ)

    cmds.text(label ="create with Asset from slot 1", align = "left")
    cmds.checkBox("refFile", value = False, onCommand = yesRefFile, offCommand = noRefFile)
    cmds.checkBox("connectDrive", value = True, onCommand = yesDrive, offCommand = noDrive)


    cmds.button(c=createCVA,w=350,h=40,label="create CVA Suface")
    #posAtSpot

    cmds.button(command = locAtSpot, label = "Loc At surface Point", w = 300, h = 20)


    #controls and connections tab
    cmds.columnLayout("Controls and Connections", w = 350, h =600, parent = "mainTabs")

    #create a peon
    masterName= cmds.textField("peonName", tx = "peon_aaa")
    cmds.button(command = createPeon, label = "Create Peon", w = 300, h = 20)


    #create a loc
    masterName= cmds.textField("locName", tx = "loc_aaa")
    cmds.button(command = createLocNew, label = "Create Loc", w = 300, h = 20)

    #master button
    masterName= cmds.textField("masterName", tx = "master_aaa")
    cmds.button(command = createMaster, label = "Create Master", w = 300, h = 20)

    #utilitys
    cmds.separator(h=40)
    #attachCVA
    cmds.button(command = attachMS, label = "CVA Attach", w = 300, h = 20)
    cmds.button(command = attachMSOFF, label = "CVA Attach OFFset", w = 300, h = 20)

    #attachCCC
    cmds.button(command = attachCCC, label = "world CCC Attach", w = 300, h = 20)
    cmds.button(command = attachCCCOFF, label = "world CCC Attach offset", w = 300, h = 20)
    #attachC basic parent scale no offsets.
    cmds.button(command = parentScaleOn, label = "Basic Attach", w = 300, h = 20)
    cmds.button(command = parentScaleOFF, label = "Basic Attach OFFset", w = 300, h = 20)





    #################################
    #Lamprey tab
    cmds.columnLayout("Lamprey", w = 350, h =600, parent = "mainTabs")
    #loc array
    cmds.separator(h=40)
    masterName= cmds.textField("arrayName", tx = "ray_aaa")
    cmds.button(command = locArray, label = "Loc Array", w = 300, h = 20)
    cmds.checkBox("rayTranslate", value = True, onCommand = yesTranslate, offCommand = noTranslate)
    cmds.checkBox("rayRotate", value = True, onCommand = yesRotate, offCommand = noRotate)
    cmds.checkBox("rayScale", value = True, onCommand = yesScale, offCommand = noScale)

    collectionlamprey = cmds.radioCollection()
    cmds.radioButton( label='connect', sl= False, onc= lampreyConnect)
    cmds.radioButton( label='getConnected', sl = False, onc= lampreyGetConnect)
    cmds.radioButton( label='noConnections', sl = True, onc= lampreyNoConnect)




    ###############################
    #assets tab
    cmds.columnLayout("Assets", w = 350, h =600, parent = "mainTabs")
    #asset a
    cmds.columnLayout("Asset_a", w = 350, h =600, parent = "Assets")
    cmds.textField("name_space_a", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_a", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_a"), w=30, h=30, image = imagePathFolder)
    #cmds.columnLayout("btn_a", w = 350, h =600, parent = "Assets")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_a,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_a,label="Import and Attach", w =155, h=20)
    cmds.button( command= addAssetMulti_a,label="mulitAss 2", w =155, h=20)



    #asset b
    cmds.columnLayout("Asset_b", w = 350, h =600, parent = "Asset_a")
    cmds.textField("name_space_b", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_b", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_b"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_b,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_b,label="Import and Attach", w =155, h=20)

    #asset C
    cmds.columnLayout("Asset_c", w = 350, h =600, parent = "Asset_b")
    cmds.textField("name_space_c", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_c", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_c"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_c,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_c,label="Import and Attach", w =155, h=20)

    #asset D
    cmds.columnLayout("Asset_d", w = 350, h =600, parent = "Asset_c")
    cmds.textField("name_space_d", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_d", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_d"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_d,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_d,label="Import and Attach", w =155, h=20)
    #asset e
    cmds.columnLayout("Asset_e", w = 350, h =600, parent = "Asset_d")
    cmds.textField("name_space_e", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_e", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_e"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_e,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_e,label="Import and Attach", w =155, h=20)
    #asset f
    cmds.columnLayout("Asset_f", w = 350, h =600, parent = "Asset_e")
    cmds.textField("name_space_f", w = 100, h=20,tx="asset_aaa")
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_f", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_f"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.button( command= addAssetRef_f,label="Reference and Attach", w =155, h=20)
    cmds.button( command= addAssetImp_f,label="Import and Attach", w =155, h=20)



    #modify tab
    cmds.columnLayout("Modify", w = 350, h =600, parent = "mainTabs")
    cmds.button(command = selectScaleRamp, label = "Select Scale Ramp" , w = 350, h = 20)
    cmds.button(command = selectPosURamp, label = "Select Posistion X Ramp" , w = 350, h = 20)
    cmds.button(command = selectPosVRamp, label = "Select Posistion Y Ramp" , w = 350, h = 20)
    cmds.button(command = selectDriveRamp, label = "Select Drive Ramp" , w = 350, h = 20)


    #show window
    cmds.showWindow(window)



#############################################################################
#UI Functions.

def addAssetTab (assetID,isRef):
    nameSpaceField="name_space_%s" % assetID
    inputField="inputField_%s"% assetID

    #set the global name space to the field.
    global myNameSpace
    myNameSpace = cmds.textField(nameSpaceField, query= True, tx=True)

    #gets the current master selection
    mSel = cmds.ls(sl=True)
    fileLocation = cmds.textField(inputField, query=True, text = True)
    if isRef == True:
        cmds.file( fileLocation, reference = True, type = "mayaAscii", namespace= myNameSpace)
    if isRef == False:
        cmds.file( fileLocation, i=True,  type = "mayaAscii",  namespace= myNameSpace)
    getPeonAss="%s:peon_aaa"%myNameSpace
    cmds.select(mSel[0],getPeonAss)
    attachMS()





def yesRefFile(*args):
    global createWithAss
    global inMode
    createWithAss=True
    inmode = 1
    print createWithAss
def noRefFile(*args):
    global createWithAss
    createWithAss=False
    inMode =1
    print createWithAss

def yesDrive(*args):
    global doConnectDrive
    global inMode
    doConnectDrive=True

    print doConnectDrive
def noDrive(*args):
    global doConnectDrive
    doConnectDrive=False

    print doConnectDrive

#lamprey menu defs
def noTranslate(*args):
    global rayTranslate
    rayTranslate=False

def yesTranslate(*args):
    global rayTranslate
    rayTranslate=True

def noRotate(*args):
    global rayRotate
    rayRotate=False

def yesRotate(*args):
    global rayRotate
    rayRotate=True

def noScale(*args):
    global rayScale
    rayScale=False

def yesScale(*args):
    global yesScale
    rayScale=True

def lampreyConnect (*args):
    global lampreyConnectOp
    global lampreyGetConnectOp
    global lampreyConnectNoneOp
    lampreyConnectOp=True
    lampreyGetConnectOp=False
    lampreyConnectNoneOp=False

def lampreyGetConnect (*args):
    global lampreyConnectOp
    global lampreyGetConnectOp
    global lampreyConnectNoneOp
    lampreyConnectOp=False
    lampreyGetConnectOp=True
    lampreyConnectNoneOp=False

def lampreyNoConnect (*args):
    global lampreyConnectOp
    global lampreyGetConnectOp
    global lampreyConnectNoneOp
    lampreyConnectOp=False
    lampreyGetConnectOp=False
    lampreyConnectNoneOp=True


#asset defs
def addAssetRef_a (*args):
    addAssetTab ("a",True)

def addAssetMulti_a (*args):
    addMultiAssetCVA ("a",True)


def addAssetImp_a(*args):
    addAssetTab ("a",False)

def addAssetRef_b (*args):
    addAssetTab ("b",True)

def addAssetImp_b(*args):
    addAssetTab ("b",False)

def addAssetRef_c (*args):
    addAssetTab ("c",True)

def addAssetImp_c(*args):
    addAssetTab ("c",False)

def addAssetRef_d (*args):
    addAssetTab ("d",True)

def addAssetImp_d(*args):
    addAssetTab ("d",False)
def addAssetRef_e (*args):
    addAssetTab ("e",True)

def addAssetImp_e(*args):
    addAssetTab ("e",False)

def addAssetRef_f (*args):
    addAssetTab ("f",True)

def addAssetImp_f(*args):
    addAssetTab ("f",False)







def browseFilePath(inputField, *args):
    returnPath=cmds.fileDialog2(fm=1, fileFilter = None, ds=2)[0]
    cmds.textField(inputField, edit = True, text = returnPath)
#alpha counter set
def cvaAlphaCounterSet(*args):
    global cvaAlphaCounter
    cvaAlphaCounter = cmds.textField("cvaAlphaCounterTx" , query=True, tx = True)



#gets the name of the CVA
def getcvaName(*args):
    global cvaName
    cvaName = cmds.textField("cva" , query=True, tx = True)
    addtotx = cmds.textField("cvaNametx", edit = True, text = cvaName)




    print cvaName
#gets the primary surface selection
def getcurvesel(*args):
    global curvesel
    global curveselShape
    curvesel=cmds.ls(sl=True)
    addtotx=cmds.textField("curveseltx", edit=True, text=curvesel[0])
    curveselShape = cmds.listRelatives(curvesel, shapes=True)
    print curvesel
    print curveselShape

def getUpVectorX (*args):
    global upX
    global upY
    global upZ
    upX=True
    upY=False
    upZ=False

    print upX,upY,upZ
def getUpVectorY (*args):
    global upX
    global upY
    global upZ
    upX=False
    upY=True
    upZ=False


    print upX,upY,upZ
def getUpVectorZ (*args):
    global upX
    global upY
    global upZ
    upX=False
    upY=False
    upZ=True

    print upX,upY,upZ



###############################################################################
def createCVA (createNewRamps):
    #defining global for later use. or even useing your own ramps later.
    global globScaleRamp
    global globPosURamp
    global globPosVRamp
    global globDriveRamp
    createNewRamps =True
    if createNewRamps == True:

        #scale ramp

        rampName=cvaName + "_scale_ramp"
        rampType= 1 #u-ramp
        newScaleRamp=createRamp(rampName,rampType)
        globScaleRamp= newScaleRamp

        rampName= cvaName + "_posU_ramp"
        rampType = 1 # u-ramps
        newPosURamp=createRamp(rampName,rampType)
        globPosURamp = newPosURamp

        #pos V ramp
        rampName= cvaName +"_posV_ramp"
        rampType = 0 # v-ramps
        newPosVRamp=createRamp(rampName,rampType)
        globPosVRamp = newPosVRamp

        #drive ramp
        rampName= cvaName + "_drive_ramp"
        rampType = 1 # u-ramps
        newDriveRamp=createRamp(rampName,rampType)
        globDriveRamp = newDriveRamp
    createCVAroot()
    #get the loc count
    getloccount()

    #execute math!
    loopMath()

    #main loop
    gridLoop()




def createCVAroot():
    global cva_root
    cva_root = cmds.group(em=True,n=cvaName)

def loopMath ():
    global segnumX
    global segnumY
    pointNumX=1
    pointNumY=1
    perNum =1
    if loccountX > 1:
        pointNumX= loccountX -1
    if loccountY > 1:
        pointNumY= loccountY -1
    segnumX = float (perNum) / float (pointNumX)
    segnumY = float (perNum) /  float (pointNumY)
    return segnumX,segnumY,pointNumX,pointNumY






#creates the ramps
def createRamp(rampName,rampType):

    #creates the ramps. Variables come from the createCVA

    rampCVA= cmds.shadingNode("ramp", asTexture=True, name = rampName)

    #adjust the color settings of the ramp
    cmds.setAttr(rampCVA + ".colorEntryList[0].position",0)
    cmds.setAttr(rampCVA+".colorEntryList[0].color", .9,.9,.9, type="double3")
    cmds.setAttr(rampCVA + ".colorEntryList[1].position",1)
    cmds.setAttr(rampCVA+".colorEntryList[1].color", 0.1,0.1,0.1, type="double3")

    #set the ramp type
    cmds.setAttr(rampCVA+".type",rampType)

    #connect a 2d place node for it
    ramp2D=cmds.shadingNode("place2dTexture", asUtility=True)
    cmds.connectAttr(ramp2D + ".outUV", rampCVA + ".uv")
    cmds.connectAttr(ramp2D + ".outUvFilterSize", rampCVA +".uvFilterSize")

    return rampName


#Math for finding the pos on the surface
def getloccount ():
    global loccountX
    global loccountY
    loccountX = cmds.intSliderGrp("loccountX",query=True, value = True)
    loccountY = cmds.intSliderGrp("loccountY",query=True, value = True)




#the main looping fuction

def gridLoop ():
    x=loccountX
    y=loccountY
    for iX in xrange (0,x):
        for iY in xrange (0,y):
            createLoc(iX,iY)
            mainLooped (iX,iY)
            print"im doing the new loop"


#def createLoc (iX,iY):# this will need to be migrated with the other loc function.
    #for now im just using grps. bla boring.
    #cmds.group(em=True, name = "grp_%d_%d_" %( iX, iY))

def createLoc(iX,iY):
    typeMS = "master"
    masterName=cvaName +"_loc_%d_%d" %( iX, iY)
    locOB = createMS(masterName,typeMS)
    parentMe = "%s_grp" % lastMScreated

    cmds.parent(parentMe , cva_root)


def mainLooped(iX,iY):
    #global poca
    #create the pos for the posistion aka poca
    poca= cmds.shadingNode("pointOnSurfaceInfo", n=cvaName +"_poc_", asUtility=True)
    cmds.setAttr(poca + ".turnOnPercentage", 1)
    posoncurveX= (iX * segnumX)
    posoncurveY= (iY * segnumY)

    cmds.setAttr(poca + ".parameterV", posoncurveY)
    cmds.setAttr(poca + ".parameterU", posoncurveX)

    cmds.connectAttr(curveselShape[0] +".worldSpace", poca + ".inputSurface", force = True)

    #createing the pos for the scale. aka poct
    poct= cmds.shadingNode("pointOnSurfaceInfo", n=cvaName +"_poct_", asUtility=True)
    cmds.setAttr(poct + ".turnOnPercentage", 1)
    cmds.connectAttr(curveselShape[0] +".worldSpace", poct + ".inputSurface", force = True)

    #adding the aim constraint
    aimconParent = lastMScreated +"_m"
    nameAC = cmds.createNode ("aimConstraint" ,parent = aimconParent, name = cvaName + "_aimcon" )

    #setting the params on the aim constraint
    cmds.setAttr(nameAC + ".tg[0].tw", 1)


    #setting the up vector
    if upX == True:
        cmds.setAttr(nameAC + ".a", 1,0,0, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 0,1,0, type="double3")
    if upY == True:
        cmds.setAttr(nameAC + ".a", 0,0,1, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 1,0,0, type="double3")

    if upZ == True:
        cmds.setAttr(nameAC + ".a", 0,1,0, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 0,0,1, type="double3")




    cmds.setAttr(nameAC + ".tg[0].tw", 1)
    #this whopping mess turns off some of the attributes i dont wan to key. not sure why i did this.
    mel.eval("""setAttr -k off ".v";setAttr -k off ".tx";setAttr -k off ".ty";setAttr -k off ".tz";setAttr -k off ".rx";setAttr -k off ".ry";setAttr -k off ".rz";setAttr -k off ".sx";setAttr -k off ".sy";setAttr -k off ".sz";""")

    #connect the poca to the loca. IE poct, and loc. but hey it ryhmes.
    cmds.connectAttr(poct + ".position", aimconParent + ".translate")
    cmds.connectAttr(poct + ".n", nameAC + ".tg[0].tt")
    cmds.connectAttr(poct + ".tv", nameAC + ".wu")
    cmds.connectAttr(nameAC + ".crx", aimconParent+ ".rx")
    cmds.connectAttr(nameAC + ".cry", aimconParent+ ".ry")
    cmds.connectAttr(nameAC + ".crz", aimconParent+ ".rz")

    if createCAPN ==True:
        #create the ColorAatPointNode CAPN
        CAPNType = "scale"
        CAPNScale = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globScaleRamp+".outColor", CAPNScale +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNScale + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNScale + ".inVCoord" ,force = True)
        scalePlug =lastMScreated +"_m"
        cmds.connectAttr(CAPNScale+".outColor", scalePlug +".scale")




        CAPNType = "posU"
        CAPNposU = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globPosURamp+".outColor", CAPNposU +".inColor")
        cmds.connectAttr(poca + ".parameterU", CAPNposU + ".inUCoord" ,force = True)
        cmds.connectAttr(poca + ".parameterV", CAPNposU + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        posLumU= cmds.shadingNode("luminance", asUtility = True,name= cvaName +"_lumU")
        cmds.connectAttr(CAPNposU +".outColor", posLumU +".value")
        cmds.connectAttr (posLumU +".outValue", poct +".parameterU")



        CAPNType = "posV"
        CAPNposV = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globPosVRamp+".outColor", CAPNposV +".inColor")
        cmds.connectAttr(poca + ".parameterU", CAPNposV + ".inUCoord" ,force = True)
        cmds.connectAttr(poca + ".parameterV", CAPNposV + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        posLumV= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumV")
        cmds.connectAttr(CAPNposV +".outColor", posLumV +".value")
        cmds.connectAttr (posLumV +".outValue", poct +".parameterV")

        CAPNType = "drive"
        CAPNDrive = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globDriveRamp+".outColor", CAPNDrive +".inColor")
        cmds.connectAttr(poca + ".parameterU", CAPNDrive + ".inUCoord" ,force = True)
        cmds.connectAttr(poca + ".parameterV", CAPNDrive + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        lumDrive= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumV")
        cmds.connectAttr(CAPNDrive +".outColor", lumDrive +".value")
        drivePlug = lastMScreated + "_m"
        cmds.connectAttr (lumDrive +".outValue", drivePlug +".drive")

    #if createing with an asset
    if createWithAss ==True:
        addAssetCVA(iX,iY,inMode)








def createMS(masterName,typeMS): # this is the def for createing Master Peon items.
    global lastMScreated
    global masterOutGlobal
    if typeMS == "master":
        print typeMS

        #create the octocurve shape.
        mel.eval("curve -d 1 -p 0 0.5 -0.05 -p -0.351178 0.354537 -0.05 -p -0.5 0 -0.05 -p -0.353553 -0.353553 -0.05 -p 0 -0.5 -0.05 -p 0.353553 -0.353553 -0.05 -p 0.5 0 -0.05 -p 0.353553 0.353553 -0.05 -p 0 0.5 -0.05 -p 0 0.5 0.05 -p 0 0.5 0.123731 -p -0.146466 0.5 0.123731 -p 0.00155382 0.5 0.186527 -p 0.137912 0.5 0.126422 -p 0 0.5 0.123731 -p 0 0.5 0.05 -p -0.353553 0.353553 0.05 -p -0.5 0 0.05 -p -0.5 0 0.176817 -p -0.5 0.0924729 0.136112 -p -0.5 -0.103869 0.128929 -p -0.5 0 0.174423 -p -0.5 0 0.05 -p -0.353176 -0.35371 0.05 -p -0.00415098 -0.498281 0.05 -p -0.00415098 -0.498281 0.126441 -p -0.148056 -0.498281 0.126441 -p 0.00280931 -0.498281 0.188869 -p 0.138068 -0.498281 0.124707 -p 0.00107523 -0.498281 0.124707 -p -0.00415098 -0.498281 0.05 -p 0.353553 -0.353553 0.05 -p 0.497706 -0.00553787 0.05 -p 0.497706 -0.00553787 0.171112 -p 0.497706 0.0854736 0.134867 -p 0.497706 -0.102769 0.134867 -p 0.497706 -0.00455561 0.166435 -p 0.498113 -0.00455561 0.05 -p 0.355252 0.349452 0.05 -p 0 0.5 0.05 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 ; ")


    #create a locator.
    if typeMS =="loc" or typeMS == "peon":
        print typeMS
        mel.eval ("spaceLocator -p 0 0 0;")

    #rename and extract shape node for messing with
    master = cmds.ls(sl = True)
    master = cmds.rename(master, masterName)
    master = cmds.ls(sl = True)
    masterShape = cmds.listRelatives(master[0], shapes=True)
    masterShape [0] = cmds.rename(masterShape[0], masterName + "Shape")

    #setting genereal and creating attrs. for it.
    cmds.addAttr (ln = "drive", k = True, dv = 0)
    cmds.addAttr (ln = "uniform_scale", sn = "uscale" , k = True, dv = 1)
    cmds.addAttr (ln = "world_blend", sn = "wblend" , k = True, dv = 1,minValue=0, maxValue=1)
    """# not currently using World translates. done with the _w grp.
    cmds.addAttr (ln = "world_translate_x", sn = "wtx", k = True, dv = 0)
    cmds.addAttr (ln = "world_translate_y", sn = "wty", k = True, dv = 0)
    cmds.addAttr (ln = "world_translate_z", sn = "wtz", k = True, dv = 0)
    cmds.addAttr (ln = "world_rotate_x", sn = "wrx", k = True, dv = 0)
    cmds.addAttr (ln = "world_rotate_y", sn = "wry", k = True, dv = 0)
    cmds.addAttr (ln = "world_rotate_z", sn = "wrz", k = True, dv = 0)
    """
    cmds.addAttr (ln="drive_offset", sn="dvo", k= True, dv=0)
    cmds.connectAttr( ".uniform_scale",   ".scaleX")
    cmds.connectAttr( ".uniform_scale",   ".scaleY")
    cmds.connectAttr( ".uniform_scale",   ".scaleZ")

    #type specific settings.
    if typeMS =="master":
        cmds.setAttr (masterShape[0] + ".overrideEnabled", 1)
        cmds.setAttr (masterShape[0] + ".overrideColor", 13)
    if typeMS =="loc":
        cmds.setAttr (masterShape[0] + ".overrideEnabled", 1)
        cmds.setAttr (masterShape[0] + ".overrideColor", 21)
        cmds.setAttr (masterShape[0] + ".localScaleX", .8)
        cmds.setAttr (masterShape[0] + ".localScaleY", .8)
        cmds.setAttr (masterShape[0] + ".localScaleZ", .8)
    if typeMS =="peon":
        cmds.setAttr (masterShape[0] + ".overrideEnabled", 1)
        cmds.setAttr (masterShape[0] + ".overrideColor", 17)
        cmds.setAttr (masterShape[0] + ".localScaleX", 1)
        cmds.setAttr (masterShape[0] + ".localScaleY", 1)
        cmds.setAttr (masterShape[0] + ".localScaleZ", 1)

    #create out grps
    cmds.select ( clear=True )
    masterOut = cmds.group (em = True, name = masterName + "_out")
    cmds.addAttr (ln = "drive", k = True, dv = 0)
    cmds.addAttr (ln = "uniform_scale", k = True, dv = 0)

    masterIn = cmds.group (em = True, name = masterName + "_in")
    cmds.addAttr (ln = "drive", k = True, dv = 0)
    cmds.addAttr (ln = "uniform_scale", k = True, dv = 0)
    masterM = cmds.group (em = True, name = masterName + "_m")
    cmds.addAttr (ln = "drive", k = True, dv = 0)
    cmds.addAttr (ln = "uniform_scale", k = True, dv = 0)
    masterW = cmds.group (em = True, name = masterName + "_w")
    cmds.addAttr (ln = "drive", k = True, dv = 0)
    cmds.addAttr (ln = "uniform_scale", k = True, dv = 0)
    cmds.parent(masterOut, master)
    cmds.select(master)
    cmds.parent(master, masterIn)
    cmds.select(masterIn, masterM, masterW)
    masterGrp = cmds.group(name= masterName + "_grp")
    cmds.select(masterGrp)
    print masterName
    lastMScreated = masterName
    #connect the master and world to the in grp.
    pmCon=cmds.parentConstraint (masterM,masterIn, mo=False, name = masterName +"_pCon")
    smCon=cmds.scaleConstraint(masterM,masterIn, mo = False, name = masterName +"_sCon")
    pwCon=cmds.parentConstraint (masterW,masterIn, mo=False, name = masterName +"_pCon")
    swCon=cmds.scaleConstraint(masterW,masterIn, mo = False, name = masterName +"_sCon")

    #create the reverse nodes, blend nodes, and other utilities.
    conReverseP = cmds.shadingNode("reverse", asUtility=True, name= masterName +"_conReverseP")
    conReverseS = cmds.shadingNode("reverse", asUtility=True, name= masterName +"_conReverseS")
    conBlendD = cmds.shadingNode("blendColors", asUtility=True, name= masterName +"_driveBlend")
    conAdd= cmds.shadingNode("plusMinusAverage", asUtility =True, name= masterName +"_driveOffset")

    #get the weight names
    pmConM= "." +masterName + "_mW0"
    pmConW= "." +masterName + "_wW1"
    smConM= "." +masterName + "_mW0"
    smConW= "." +masterName + "_wW1"

    #connect the weights together for the parant constraint
    cmds.connectAttr(masterName +".world_blend", conReverseP + ".inputX")
    cmds.connectAttr(masterName +".world_blend", pmCon[0] + pmConM)
    cmds.connectAttr(conReverseP +".outputX", pmCon[0] +pmConW, force=True)

    #connect the weights together for the scale constraint
    cmds.connectAttr(masterName +".world_blend", conReverseS + ".inputX")
    cmds.connectAttr(masterName +".world_blend", smCon[0] + smConM)
    cmds.connectAttr(conReverseS +".outputX", smCon[0] +smConW, force=True)

    #connect the drive up.
    cmds.connectAttr(masterName +".world_blend", conBlendD +".blender")
    cmds.connectAttr(masterM +".drive", conBlendD +".color1.color1R")
    cmds.connectAttr(masterW +".drive", conBlendD +".color2.color2R")
    cmds.connectAttr(conBlendD + ".output.outputR", masterIn +".drive")
    cmds.connectAttr(masterIn +".drive" ,conAdd +".input1D[0]", force=True)
    cmds.connectAttr(masterName +".drive_offset" ,conAdd +".input1D[1]", force=True)
    cmds.connectAttr(conAdd +".output1D", masterName +".drive")
    cmds.select(masterGrp)
    masterOutGlobal = masterOut

def createLocNew(masterName):
    masterName = cmds.textField("locName", q=True, text = True)
    typeMS = "loc"
    locOB = createMS(masterName,typeMS)



def createMaster(masterName):
    masterName = cmds.textField("masterName", q=True, text = True)#get name from text feild
    typeMS="master"#setting the creation type.
    masterOB = createMS(masterName,typeMS)


def createPeon(masterName):
    masterName = cmds.textField("peonName", q=True, text = True)#get name from text feild
    typeMS="peon"#setting the creation type.
    peonOB = createMS(masterName,typeMS)



def attachMS (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)

    #cmds.select(peon)
    #peonGrp= cmds.pickWalk(d="up")#sets the incoming connection to its _in node.

    peonGrp = peon + "_m"
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=False)
    cmds.scaleConstraint(master,peonGrp, mo = False)

    #connect drive.
    if doConnectDrive == True:
        cmds.connectAttr(master +".drive", peonGrp + ".drive")
    #cmds.connectAttr(master +".uniform_scale", peon + ".uniform_scale")
def attachMSOFF (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)

    #cmds.select(peon)
    #peonGrp= cmds.pickWalk(d="up")#sets the incoming connection to its _in node.

    peonGrp = peon + "_m"
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=True)
    cmds.scaleConstraint(master,peonGrp, mo = True)

    #connect drive.
    #cmds.connectAttr(master +".drive", peonGrp + ".drive")
    #cmds.connectAttr(master +".uniform_scale", peon + ".uniform_scale")


def attachCCC (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)



    peonGrp = peon + "_w"
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=False)
    cmds.scaleConstraint(master,peonGrp, mo = False)

    cmds.select (master)
    #cmds.addAttr (ln = "drive", k = True, dv = 0)
    #connect drive.
    #cmds.connectAttr(master +".drive", peonGrp + ".drive")
def attachCCCOFF (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)



    peonGrp = peon + "_w"
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=True)
    cmds.scaleConstraint(master,peonGrp, mo = True)

    cmds.select (master)
    #cmds.addAttr (ln = "drive", k = True, dv = 0)
    #connect drive.
    #cmds.connectAttr(master +".drive", peonGrp + ".drive")

def parentScaleOn (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)



    peonGrp = peon
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=False)
    cmds.scaleConstraint(master,peonGrp, mo = False)

    cmds.select (master)
    #cmds.addAttr (ln = "drive", k = True, dv = 0)
    #connect drive.
    #cmds.connectAttr(master +".drive", peonGrp + ".drive")
def parentScaleOFF (*args):
    selMS = cmds.ls(sl=True)
    master =selMS[0]
    peon = selMS[1]
    cmds.select(master)



    peonGrp = peon
    print peonGrp

    #constraints
    cmds.select(master,peonGrp)
    cmds.parentConstraint (master,peonGrp, mo=True)
    cmds.scaleConstraint(master,peonGrp, mo = True)

    cmds.select (master)
    #cmds.addAttr (ln = "drive", k = True, dv = 0)
    #connect drive.
    #cmds.connectAttr(master +".drive", peonGrp + ".drive")





def selectScaleRamp (*args):
    cmds.select(globScaleRamp)
def selectPosURamp (*args):
    cmds.select(globPosURamp)
def selectPosVRamp (*args):
    cmds.select(globPosVRamp)
def selectDriveRamp (*args):
    cmds.select(globDriveRamp)

#add asset
def addAssetCVA(iX,iY,inMode):


    if inMode == 1:
        refAss = True
    if inMode == 2:
        impAss = True
    if inMode == 3:
        dupAss = True
    if inMode == 4:
        dupInsAss= True

    if refAss == True:
        fileLocation = cmds.textField("inputField_a", query=True, text = True)
        nameSpaceRef = "%s_%s_%s" % (cvaName,iX,iY)
        connectCVA = True
        cmds.file( fileLocation, r=True, type = "mayaAscii", namespace= nameSpaceRef)
        if connectCVA == True:
            getPeonAss="%s:peon_aaa"%nameSpaceRef
            cmds.select(lastMScreated,getPeonAss)
            attachMS()

#add Multi Ass prototype
def addMultiAssetCVA(assetID,isRef):
    #set the global name space to the field.
    global myNameSpace
    nameSpaceField="name_space_%s" % assetID
    inputField="inputField_%s"% assetID
    myNameSpace = cmds.textField(nameSpaceField, query= True, tx=True)
    fileLocation = cmds.textField(inputField, query=True, text = True)
    mSel = cmds.ls(sl=True)

    aCount = len(mSel)

    cmds.file( fileLocation, r=True, type = "mayaAscii", namespace= myNameSpace)
    for iray in xrange (0,aCount):
         getPeonAss="%s:loc_%s_aaa"% (myNameSpace,iray)
         cmds.select(mSel[iray],getPeonAss)
         attachMS()






##Loc Array aka lamprey
def locArray(masterName):
    masterName = cmds.textField("arrayName", q=True, text = True)
    typeMS = "loc"
    selArray = cmds.ls(sl=True)
    aCount = len(selArray)
    print aCount


    for iray in xrange (0,aCount):
        irayName = "%s_%s" % (masterName,iray)
        cmds.select(selArray[iray])
        irayPos = cmds.xform(query=True, worldSpace=True, translation =True)
        irayRot = cmds.xform(query=True, worldSpace=True, rotation =True)
        iraySca = cmds.xform(query=True, worldSpace=True, scale =True)

        createMS(irayName,typeMS)
        if rayTranslate == True:
            irayLocPos = cmds.xform (worldSpace=True, translation = irayPos)
        if rayRotate == True:
            irayLocRot = cmds.xform (worldSpace=True, rotation = irayRot)
        if rayScale == True:
            irayLocSca = cmds.xform ( scale = iraySca)
        if lampreyConnectOp ==True:
            cmds.select(masterOutGlobal,selArray[iray])
            parentScaleOFF()
        if lampreyGetConnectOp ==True:
            cmds.select(selArray[iray],lastMScreated)
            attachMSOFF()



############new main looped.  Creates a point on surface node.
def ultraPOS(uCoord,vCoord):
    paraU = uCoord
    paraV = vCoord
    #global poca
    #create the pos for the posistion aka poca
    poca= cmds.shadingNode("pointOnSurfaceInfo", n=cvaName +"_poc_", asUtility=True)
    cmds.setAttr(poca + ".turnOnPercentage", 1)
    posoncurveX= (paraU)
    posoncurveY= (paraV)

    cmds.setAttr(poca + ".parameterV", posoncurveY)
    cmds.setAttr(poca + ".parameterU", posoncurveX)

    cmds.connectAttr(curveselShape[0] +".worldSpace", poca + ".inputSurface", force = True)


    #createing the pos for the scale. aka poct
    poct= cmds.shadingNode("pointOnSurfaceInfo", n=cvaName +"_poct_", asUtility=True)
    cmds.setAttr(poct + ".turnOnPercentage", 1)
    cmds.connectAttr(curveselShape[0] +".worldSpace", poct + ".inputSurface", force = True)
    cmds.setAttr(poct + ".parameterV", posoncurveY)
    cmds.setAttr(poct + ".parameterU", posoncurveX)

    #adding the aim constraint
    aimconParent = lastMScreated +"_m"
    nameAC = cmds.createNode ("aimConstraint" ,parent = aimconParent, name = cvaName + "_aimcon" )

    #setting the params on the aim constraint
    cmds.setAttr(nameAC + ".tg[0].tw", 1)


    #setting the up vector
    if upX == True:
        cmds.setAttr(nameAC + ".a", 1,0,0, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 0,1,0, type="double3")
    if upY == True:
        cmds.setAttr(nameAC + ".a", 0,0,1, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 1,0,0, type="double3")

    if upZ == True:
        cmds.setAttr(nameAC + ".a", 0,1,0, type="double3")#i think this is the aim vector.
        cmds.setAttr(nameAC + ".u", 0,0,1, type="double3")




    cmds.setAttr(nameAC + ".tg[0].tw", 1)
    #this whopping mess turns off some of the attributes i dont wan to key. not sure why i did this.
    mel.eval("""setAttr -k off ".v";setAttr -k off ".tx";setAttr -k off ".ty";setAttr -k off ".tz";setAttr -k off ".rx";setAttr -k off ".ry";setAttr -k off ".rz";setAttr -k off ".sx";setAttr -k off ".sy";setAttr -k off ".sz";""")

    #connect the poca to the loca. IE poct, and loc. but hey it ryhmes.
    cmds.connectAttr(poct + ".position", aimconParent + ".translate")
    cmds.connectAttr(poct + ".n", nameAC + ".tg[0].tt")
    cmds.connectAttr(poct + ".tv", nameAC + ".wu")
    cmds.connectAttr(nameAC + ".crx", aimconParent+ ".rx")
    cmds.connectAttr(nameAC + ".cry", aimconParent+ ".ry")
    cmds.connectAttr(nameAC + ".crz", aimconParent+ ".rz")











## ###### loc at spot
def locAtSpot(curveSel):
    typeMS = "loc"
#holy crap all this to clean the string.. has to be a smarter way.

    pointSel = cmds.ls(sl=True)
    cleanSel = pointSel[0]
    uStart= cleanSel.find('.')
    print uStart
    uU1=cleanSel[uStart:None]
    uU2=uU1[1:None]
    print uU2

    uU3 = uU2[3:None]
    uU3b= len(uU3)
    print uU3b
    uU3c = (uU3b -1)
    print uU3c
    uU4 = uU3[None:uU3c]
    print uU4

    removeYcoord=uU4.find('[')
    print removeYcoord

    uU5= uU4[None:removeYcoord]
    uU5b = len(uU5)
    uU5c = (uU5b -1)
    uU6 = uU5[None:uU5c]
    uU7 = uU6[None:5]
    uCoord = float(uU7)

    print uCoord


    vStart=uU4.find('[')
    print vStart
    vU1=uU4[(vStart):None]
    print vU1
    vU2=vU1[1:None]
    vU3 = vU2[None:5]
    vCoord = float(vU3)
    print vCoord

    #creating the pos.
    locAtSpotName = (cvaName + "_" + cvaAlphaCounter)
    createMS(locAtSpotName,typeMS)
    ultraPOS(uCoord,vCoord)
    cvaAlphaCountUp(cvaAlphaCounter)


#alpha Counter
def cvaAlphaCountUp(s):
    global cvaAlphaCounter
    new_s = []
    continue_change = True
    for c in s[::-1].lower():
        if continue_change:
            if c == 'z':
                new_s.insert(0, '0')
            else:
                new_s.insert(0, alphal[alphal.index(c) + 1])
                continue_change = False
        else:
            new_s.insert(0, c)

        cvaAlphaCounter =  ''.join(new_s)
        addtotx=cmds.textField("cvaAlphaCounterTx", edit=True, text=cvaAlphaCounter)
