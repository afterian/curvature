import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import xml.dom.minidom as xd
from random import randint

""" windows not saving my shelf buttons.
import cva
reload(cva)
cva.cvaUI()

To do:
-error check on :
    -cva name field. no bad names
-separate out ramp creation. add a selector for it. but also add a button for creating a default ramp like i have.
-curves, and poly support.
-clear xml menu list when loading new xml.
-supper duper . add a selection to dupe instead of ref.
-asset addiition for all generators.
-multiAss support.
-query spans and create percent for LOC at spot.
-Locking connect drive to True to prevent a bug while devving. rotation out.
-added rotation support.
-asset input selection tab may be borked. see line. 687
add nurb sphere upgrade.
-adding controls.
"""
##version .06 "Lamprey" added loc array functionality. Select some things, click button, get locs at pos
##version .07 PosAtSpot ads a loc at surface pos,  def for Surface to pointOnsurface to Locater, it mainLooped will eventually be depreciated. it works now, not messing with it. But its possibly redundent.
#-addedalpha numeric counter . Currently only locAtPoint is using it.
#version .07 adjusting loccountx , y  to be able to do a single row or collum.
#adapting to pllugin changes
#version .10 going beta. Changing terminollgy so i can go opensource.
#version .11 added alpha counter functionality to the other items.
#version .12 Xml,
#version .13 fixing bug on xml going past 11.
#version.4 randy ass

#defining global vars, I would like to find a better way to do this.
curvesel = ""
curveselShape =""
cvaName = "cva"
poca = ""
lastMScreated =""
globScaleRamp=""
globPosURamp=""
globPosVRamp=""
globDriveRamp=""
globRotXRamp=""
globRotYRamp=""
globRotZRamp=""
globalRotationRamp = ""
globalFolUpgrade=""
loccountX=2
loccountY=2
segnumX=""
segnumY=""
cva_root=""
upX=False
upY=False
upZ=True
doCreateCAPN=True
LastCAPN=""
inMode=1
myNameSpace=""
createWithAss=False
assetfromXML=False
doConnectDrive=True
doConnectPosU=True
doConnectPosV=True
doConnectRotX=False
doConnectRotY=False
doConnectRotZ=False
doConnectUscale=False
doAutoCreateMS =False
doFolUpgrade=False
doRandyAss = False
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
packagePath="Load XML asset package"
cvaAlphaCounter="aaa"
alphal = '0123456789abcdefghijklmnopqrstuvwxyz'
multiLocList = []
multiLCC=1
assetID =0
fileLocation =""
superDuper = ""

#createNewRamps=True


#creating the main UI
def cvaUI():
    global assetID
    #see if window exists
    if cmds.window("cvaUI" , exists = True):
        cmds.deleteUI("cvaUI")

    #create the window
    imagePathBanner = cmds.internalVar(upd = True) + "icons/cvaIcon.png"
    imagePathFolder = cmds.internalVar(upd = True) + "icons/cvaFolder.jpg"
    imagePathNurbGrid = cmds.internalVar(upd = True) + "icons/nurbArray.png"
    imagePathFolGrid = cmds.internalVar(upd = True) + "icons/folArray.png"
    imagePathPaintFol = cmds.internalVar(upd = True) + "icons/folBrush.png"
    imagePathLamprey = cmds.internalVar(upd = True) + "icons/lamprey.png"
    imagePathLocASpot = cmds.internalVar(upd = True) + "icons/locAspot.png"
    imagePathSelFol = cmds.internalVar(upd = True) + "icons/selFol.png"
    window = cmds.window("cvaUI", title = "CurVeAture", w = 350 , h = 700 , mxb = False, sizeable = True)
    #create the mainlayout
    mainLayout = cmds.columnLayout("mainColumn", w =350, h = 700)
    #banner image
    cmds.image(w = 350, h =60, image = imagePathBanner)
    cmds.separator(h=40)
    cmds.textField("cvaNametx",en = False, text = "NO CVA ASSIGNED", w= 360)
    #feedback
    cmds.columnLayout( "mainColumn", adjustableColumn = True)
    cmds.gridLayout("nameGridLayout01", numberOfRowsColumns = (3,2), cellWidthHeight = (180,20), parent = "mainColumn")


    #cmds.text("cvanameLabel", label = "Current CVA:", width = 20, height = 20, backgroundColor = [0.2, 0.2, 0.2])

    cmds.button(command = getcvaName, label = "Set CVA", w = 350, h = 20)
    cmds.textField("cva", w= 350, tx= "cva")

        #Alpha Numeric counter.
    cmds.button(command = cvaAlphaCounterSet, label = "set alpha counter", w = 350, h = 20)
    cmds.textField("cvaAlphaCounterTx", text = "aaa")
    curvesel = "no surface"

#curveAture tab
    cmds.button(command = getcurvesel, label = "Load Surface", w = 350, h = 20)
    cmds.textField("curveseltx", w= 350, en = False, text = "NO SURFACE SELECTED")





    ##main tabs start here.
    cmds.separator(h =20, vis = False)
    tabLayout = cmds.tabLayout("mainTabs", parent = mainLayout, imw = 5, imh = 5)
    cmds.columnLayout("CurVAture", w = 350, h =800, parent = "mainTabs")



    cmds.intSliderGrp("loccountXtx", label = "number of locators X", minValue=1, maxValue=100, step=1, field=True, value = 2)
    cmds.intSliderGrp("loccountYtx", label = "number of locators Y", minValue=1, maxValue=100, step=1, field=True, value = 2)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,300),(2,50)])
    cmds.button(c=createCVA,w=300,h=40,label="Create Nurb Grid Array")
    cmds.image(w = 40, h =40, image = imagePathNurbGrid)
    cmds.button(command = locAtSpot, label = "Create follicle Grid Array", w = 300, h = 40)
    cmds.image(w = 40, h =40, image = imagePathFolGrid)
    cmds.button(command = locAtSpot, label = "Convert Faces to follicles", w = 300, h = 40)
    cmds.image(w = 40, h =40, image = imagePathSelFol)
    cmds.button(command = locAtSpot, label = "Paint follicles", w = 300, h = 40)
    cmds.image(w = 40, h =40, image = imagePathPaintFol)


    cmds.button(command = locArray, label = "Lamprey", w = 300, h = 40)
    cmds.image(w = 40, h =40, image = imagePathLamprey)
    cmds.button(command = locAtSpot, label = "Loc At surface Point", w = 300, h = 40)
    cmds.image(w = 40, h =40, image = imagePathLocASpot)


    cmds.columnLayout("settingstxCol", w = 350, h =800, parent = "CurVAture")
    cmds.separator(20, vis = False)
    cmds.frameLayout("layoutFrameRamps", label = "Ramps and Textures", collapsable = True,  parent = "settingstxCol", w = 350)
    #layout
    rowColumnLayout = cmds.rowColumnLayout(nc=3,cw=[(1,170),(2,100),(3,80)])
    cmds.button(label="Create Ramp")
    cmds.textField("0002tx", text = "Name")
    cmds.optionMenu( "createRampType", label='type', changeCommand = selectAssetID)
    cmds.menuItem(label="U",en=False)
    cmds.menuItem(label="v",en=False)

    cmds.separator(h = 20, vis = False)

#rampF posU upgrade
    #cmds.columnLayout("rampPosUsettings", w = 350,  parent = "layoutFrameRamps")
    #rowColumnLayout = cmds.rowColumnLayout(nc=4,cw=[(1,120),(2,20),(3,130),(4,80)])
    #cmds.checkBox("autoCreateRampPosU", label = "PosU Ramp", value = True, onCommand = yesCreatePosURamp, offCommand = noCreatePosURamp)
    #cmds.button(command = setPosURamp, label = "Set", w = 20, h = 20)
    #cmds.textField("rampNamePosUtx", text = "ramp1")
    #cmds.button(command = selectPosURamp, label = "Select", w = 40, h = 20)







#rampF follicle upgrade
    cmds.columnLayout("rampFolsettings", w = 350,  parent = "layoutFrameRamps")
    rowColumnLayout = cmds.rowColumnLayout(nc=4,cw=[(1,120),(2,20),(3,130),(4,80)])
    cmds.checkBox("autoCreateRampF", label = "Follicle Upgrade", value = True, onCommand = yesCreateFolUpdgradeRamp, offCommand = noCreateFolUpgradeRamp)
    cmds.button(command = setFolUpgradeRamp, label = "Set", w = 20, h = 20)
    cmds.textField("rampNameFtx", text = "ramp1")
    cmds.button(command = selectFolUpgradeRamp, label = "Select", w = 40, h = 20)



    cmds.frameLayout("layoutFrameSettings", label = "Settings", collapsable = True,  parent = "settingstxCol")
    collection1 = cmds.radioCollection()
    cmds.radioButton( label='upX', sl= False, onc= getUpVectorX)
    cmds.radioButton( label='upY', sl = False, onc= getUpVectorY)
    cmds.radioButton( label='upZ', sl = True, onc= getUpVectorZ)


    cmds.checkBox("rayTranslate", value = True, onCommand = yesTranslate, offCommand = noTranslate)
    cmds.checkBox("rayRotate", value = True, onCommand = yesRotate, offCommand = noRotate)
    cmds.checkBox("rayScale", value = True, onCommand = yesScale, offCommand = noScale)
    cmds.checkBox("uScale", value = False, onCommand = yesuScale, offCommand = nouScale)
    cmds.checkBox("Upgrade nHair follicle", value = False, onCommand = yesFolUpgrade, offCommand = noFolUpgrade)

    collectionlamprey = cmds.radioCollection()
    cmds.radioButton( label='connect', sl= False, onc= lampreyConnect)
    cmds.radioButton( label='getConnected', sl = False, onc= lampreyGetConnect)
    cmds.radioButton( label='noConnections', sl = True, onc= lampreyNoConnect)


    cmds.checkBox("createCAPNtx", value = True, onCommand = yesCreateCAPN, offCommand = noCreateCAPN)
    cmds.checkBox("connectDrive", value = True, onCommand = yesDrive, offCommand = noDrive)
    cmds.checkBox("posUtx", value = True, onCommand = yesPosU, offCommand = noPosU)
    cmds.checkBox("posVtx", value = True, onCommand = yesPosV, offCommand = noPosV)
    cmds.checkBox("rotXtx", value = False, onCommand = yesRotX, offCommand = noRotX)
    cmds.checkBox("rotYtx", value = False, onCommand = yesRotY, offCommand = noRotY)
    cmds.checkBox("rotZtx", value = False, onCommand = yesRotZ, offCommand = noRotZ)
    #posAtSpot




    #controls and connections tab
    cmds.columnLayout("Connections", w = 350, h =600, parent = "mainTabs")



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
    cmds.columnLayout("Controls", w = 350, h =600, parent = "mainTabs")
    #loc array
    cmds.separator(h=40)
    #create a peon
    cmds.checkBox("autocreateMStx",  value = False, onCommand = yesAutoCreateMs, offCommand = noAutoCreateMs)
    masterName= cmds.textField("peonName", tx = "peon")
    cmds.button(command = createPeon, label = "Create Peon", w = 300, h = 20)


    #create a loc
    masterName= cmds.textField("locName", tx = "loc")
    cmds.button(command = createLocNew, label = "Create Loc", w = 300, h = 20)

    #master button
    masterName= cmds.textField("masterName", tx = "master")
    cmds.button(command = createMaster, label = "Create Master", w = 300, h = 20)
    masterName= cmds.textField("arrayName", tx = "ray")
    cmds.button(command = locArray, label = "Loc Array", w = 300, h = 20)





    ###############################
    #assets tab
    cmds.columnLayout("Assets", w = 350, h =600, parent = "mainTabs")
    cmds.textField("name_space_a", w = 100, h=20,tx="asset")
    #asset type selection
    cmds.checkBox("createWithAss", value = False, onCommand = yesCreateWithAss, offCommand = noCreateWithAss)
    cmds.checkBox("createWithXMLAss", value = False, onCommand = yesCreateWithXMLAss, offCommand = noCreateWithXMLAss)
    collectionlamprey = cmds.radioCollection()
    cmds.radioButton( label='Reference', sl= True, onc= inModeSelect1)
    cmds.radioButton( label='Import', sl = False, onc= inModeSelect2)
    cmds.radioButton( label='Duplicate', sl = False, onc= inModeSelect3)
    cmds.radioButton( label='Instance', sl = False, onc= inModeSelect4)


    #asset c super duper
    cmds.separator(h=40)
    cmds.checkBox("randyAsstx", value = False, onCommand = yesRandyAss, offCommand = noRandyAss)
    cmds.textField("superDupertx",w = 100, h = 20, tx="")
    cmds.button("superDuperBtn",command = setSuperDuper, w=300, h=30,label="Set from selection")


    #asset a
    cmds.columnLayout("Asset_a", w = 350, h =600, parent = "Assets")

    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_a", w = 300, h=20)
    folderBtn = cmds.symbolButton(command= partial(browseFilePath,"inputField_a"), w=30, h=30, image = imagePathFolder)


    rowColumnLayout = cmds.rowColumnLayout(nc=3,cw=[(1,30),(2,155)])
    setfileLocationBtn = cmds.button(command= setfileLocation, w=30, h=30,label="Set")
    cmds.button( command= addAssetRef_a,label="Reference and Attach", w =155, h=20)

    cmds.button( command= addAssetMulti_a,label="mulitAss", w =155, h=20)



    #asset b xml
    cmds.columnLayout("Asset_b", w = 350, h =600, parent = "Asset_a")
    cmds.textField("name_space_b", w = 100, h=20,tx="Asset Package", en=False)
    cmds.textField("assetIDtx", w = 100, h=20,tx="0", en=False)
    cmds.textField("multiLCCtx", w = 100, h=20,tx="1", en=False)
    cmds.textField("fileLocationtx", w = 100, h=20,tx="", en=False)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,310),(2,30)])
    inputField=cmds.textField("inputField_b", w = 300, h=20, tx = packagePath)
    folderBtn = cmds.symbolButton(command= partial(browseFilePathXML,"inputField_b"), w=30, h=30, image = imagePathFolder)
    rowColumnLayout = cmds.rowColumnLayout(nc=2,cw=[(1,155),(2,155)])
    cmds.optionMenu( "xmlAssetName", label='Asset', changeCommand = selectAssetID)
    cmds.menuItem(label="Select asset",en=False)




    #show window
    #cmds.showWindow(window)
    cmds.dockControl( area='left', floating = False,  content=window, allowedArea="all", label = "Curvature" )


#############################################################################
#UI Functions.

def addAssetTab (assetID,isRef):
    nameSpaceField="name_space_a"
    inputField="inputField_a"

    #set the global name space to the field.
    global myNameSpace

    makeNameSpace = cmds.textField(nameSpaceField, query= True, tx=True)
    myNameSpace = "%s_%s" %(makeNameSpace , cvaAlphaCounter)
    cvaAlphaCountUp(cvaAlphaCounter)


    #gets the current master selection
    mSel = cmds.ls(sl=True)
    #fileLocation = cmds.textField(inputField, query=True, text = True)
    if isRef == True:
        cmds.file( fileLocation, reference = True, type = "mayaAscii", namespace= myNameSpace)
    if isRef == False:
        cmds.file( fileLocation, i=True,  type = "mayaAscii",  namespace= myNameSpace)
    getPeonAss="%s:peon_aaa"%myNameSpace
    cvaAlphaCountUp
    cmds.select(mSel[0],getPeonAss)
    attachMS()



def selectFolUpgradeRamp(*args):
    global createWithAss
    createWithAss=True
    print createWithAss
def yesCreateFolUpdgradeRamp(*args):
    global createWithAss
    createWithAss=True
    print createWithAss
def noCreateFolUpgradeRamp(*args):
    global createWithAss
    createWithAss=True
    print createWithAss

def setFolUpgradeRamp(*args):
    global createWithAss
    createWithAss=True
    print createWithAss





def yesCreateWithAss(*args):
    global createWithAss
    assetfromXML=True


def noCreateWithAss(*args):
    global createWithAss
    assetfromXML=False


def yesCreateWithXMLAss(*args):
    global createWithAss
    createWithAss=True
    print createWithAss

def noCreateWithXMLAss(*args):
    global createWithAss
    createWithAss=False
    print createWithAss


def noRandyAss(*args):
    global doRandyAss
    doRandyAss=False
    print doRandyAss

def yesRandyAss(*args):
    global doRandyAss
    doRandyAss=True
    print doRandyAss




def yesDrive(*args):
    global doConnectDrive
    global inMode
    doConnectDrive=True

    print doConnectDrive
def noDrive(*args):
    global doConnectDrive
    doConnectDrive=False

    print doConnectDrive

def yesPosU(*args):
    global doConnectPosU
    global inMode
    doConnectPosU=True

    print doConnectPosU
def noPosU(*args):
    global doConnectPosU
    doConnectPosU=False

    print doConnectPosU

def yesPosV(*args):
    global doConnectPosV
    global inMode
    doConnectPosV=True

    print doConnectPosV
def noPosV(*args):
    global doConnectPosV
    doConnectPosV=False

    print doConnectPosV

def yesRotX(*args):
    global doConnectRotX
    global inMode
    doConnectRotX=True

    print doConnectDrive
def noRotX(*args):
    global doConnectRotX
    doConnectRotX=False

    print doConnectRotX

def yesRotY(*args):
    global doConnectRotY
    global inMode
    doConnectRotY=True

    print doConnectRotY
def noRotY(*args):
    global doConnectRotY
    doConnectRotY=False

    print doConnectRotY

def yesRotZ(*args):
    global doConnectRotZ
    global inMode
    doConnectRotZ=True

    print doConnectRotZ
def noRotZ(*args):
    global doConnectRotZ
    doConnectRotZ=False

    print doConnectRotZ





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

def yesuScale(*args):
    global doConnectUscale
    doConnectUscale=True
def nouScale(*args):
    global doConnectUscale
    doConnectUscale=False

def yesFolUpgrade(*args):
    global doFolUpgrade
    global surfaceType
    surfaceType = "srfPoly"
    doFolUpgrade=True
def noFolUpgrade(*args):
    global doFolUpgrade
    doFolUpgrade=False

def yesAutoCreateMs(*args):
    global doAutoCreateMS
    doAutoCreateMS=True
def noAutoCreateMs(*args):
    global doAutoCreateMS
    doAutoCreateMScreateMS=False

def yesCreateCAPN(*args):
    global doCreateCAPN
    doCreateCAPN=True
def noCreateCAPN(*args):
    global doCreateCAPN
    doCreateCAPN=False


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
def inModeSelect1 (*args):
    global inMode
    inMode = 1
def inModeSelect2 (*args):
    global inMode
    inMode = 2
def inModeSelect3 (*args):
    global inMode
    inMode = 3
def inModeSelect4 (*args):
    global inMode
    inMode = 4


def setSuperDuper (*args):
    global superDuper
    superDuper = cmds.ls(sl=True)
    cmds.textField("superDupertx", edit = True, text = superDuper[0])





def addAssetRef_a (*args):
    addAssetTab ("a",True)

def addAssetMulti_a (*args):
    addMultiAssetCVA ("a",True)



def setfileLocation(*args):
    global fileLocation
    fileLocation = cmds.textField("inputField_a",query = True, text = True)
    cmds.textField("fileLocationtx", edit = True, text = fileLocation)

def browseFilePath(inputField, *args):
    returnPath=cmds.fileDialog2(fm=1, fileFilter = None, ds=2)[0]
    cmds.textField(inputField, edit = True, text = returnPath)

def browseFilePathXML(inputField, *args):
    global packagePath
    global assetID
    returnPath=cmds.fileDialog2(fm=1, fileFilter = None, ds=2)[0]
    packagePath = returnPath
    cmds.textField(inputField, edit = True, text = returnPath)

    #queryXMLfile
    dom = xd.parse(packagePath)
    menuAsses = len(dom.getElementsByTagName("asset"))

    for node in dom.getElementsByTagName("asset"):
        attrs= node.attributes.keys()
        for assetIDattr in attrs:
            pair = node.attributes[assetIDattr]
        assetLocation = node.getAttribute("fileLocation")
        labelName =node.attributes[assetIDattr].value
        menuLabel = "%s_%s" %(assetID,labelName)
        cmds.menuItem( label=menuLabel, parent="xmlAssetName")
        assetID = assetID + 1
    assetID = 0


def selectAssetID(*args):
    global fileLocation
    global assetID
    global multiLCC
    global multiLocList
    if doRandyAss==True:
        print "randy"
        randyAss()
    if assetfromXML ==True:
        getAssetName = cmds.optionMenu("xmlAssetName", query=True, value=True)
        assetIDtrim = getAssetName.find("_")
        assetIDstr = getAssetName[None:assetIDtrim]

        assetID = int(assetIDstr)

    #getting the filepath from teh xml
        dom= xd.parse(packagePath)
        asset=dom.getElementsByTagName("asset")[assetID]
        print (asset.firstChild.data)

        getfileLocation = dom.getElementsByTagName("fileLocation")[assetID]
        fileLocation = str( (getfileLocation.firstChild.data))

    #gettng the locs list.

        getassloc = dom.getElementsByTagName("loc")[assetID]
        getMultiAssCount =getassloc.attributes["count"].value

#multi ass gathering.
        print (getassloc.firstChild.data)
        multiLocListStr = str(getassloc.firstChild.data)
        multiLocList = multiLocListStr.split(',')
        cmds.textField("multiLCCtx", edit = True, text = getMultiAssCount )
        cmds.textField("assetIDtx", edit = True, text = assetID)
        cmds.textField("fileLocationtx", edit = True, text = fileLocation)
    else:
        assetID = 0

def randyAss(*args):
    global assetID
    global fileLocation

    print "randy ass is on bitches."
    dom = xd.parse(packagePath)
    menuAssesL = len(dom.getElementsByTagName("asset"))
    menuAsses = menuAssesL -1
    print assetID
    print menuAsses
    assetID = randint(0,menuAsses)
    dom= xd.parse(packagePath)
    asset=dom.getElementsByTagName("asset")[assetID]
    print (asset.firstChild.data)

    getfileLocation = dom.getElementsByTagName("fileLocation")[assetID]
    fileLocation = str( (getfileLocation.firstChild.data))

    #gettng the locs list.

    getassloc = dom.getElementsByTagName("loc")[assetID]
    getMultiAssCount =getassloc.attributes["count"].value

#multi ass gathering.
    print (getassloc.firstChild.data)
    multiLocListStr = str(getassloc.firstChild.data)
    multiLocList = multiLocListStr.split(',')
    cmds.textField("multiLCCtx", edit = True, text = getMultiAssCount )
    cmds.textField("assetIDtx", edit = True, text = assetID)
    cmds.textField("fileLocationtx", edit = True, text = fileLocation)

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
    global surfaceType
    surfaceType="srfNurb"
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

#this will be the new CAPN creation defs. for more flexiablity.
def createCAPN(CAPNType,uCoord,vCoord,inputColor,inputThing):
    global lastCAPN
    if CAPNType == "folCAPN":
        CAPNTypeName = CAPNType
        inputColor = inputColor
        inputThing = inputThing #either a pos or a hair follicle
        CAPN = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" + CAPNTypeName)

        cmds.connectAttr(inputColor+".outColor", CAPN +".inColor")
        cmds.connectAttr(inputThing + ".parameterU", CAPN + ".inUCoord" ,force = True)
        cmds.connectAttr(inputThing + ".parameterV", CAPN+ ".inVCoord" ,force = True)
        lastCAPN = CAPN


###############################################################################
def createCVA (createNewRamps):
    #defining global for later use. or even useing your own ramps later.
    global globScaleRamp
    global globPosURamp
    global globPosVRamp
    global globDriveRamp
    global globRotXRamp
    global globRotYRamp
    global globRotZRamp
    createNewRamps =True
    if createNewRamps == True:

        #scale ramp

        rampName=cvaName + "_scale_ramp"
        rampType= 1 #u-ramp
        newScaleRamp=createRamp(rampName,rampType)
        globScaleRamp= newScaleRamp
        if doConnectPosU == True:
            rampName= cvaName + "_posU_ramp"
            rampType = 1 # u-ramps
            newPosURamp=createRamp(rampName,rampType)
            globPosURamp = newPosURamp

        if doConnectPosV == True:
        #pos V ramp
            rampName= cvaName +"_posV_ramp"
            rampType = 0 # v-ramps
            newPosVRamp=createRamp(rampName,rampType)
            globPosVRamp = newPosVRamp

        #drive ramp
        if doConnectDrive == True:
            rampName= cvaName + "_drive_ramp"
            rampType = 1 # u-ramps
            newDriveRamp=createRamp(rampName,rampType)
            globDriveRamp = newDriveRamp

        #drive ramp
        if doConnectRotX == True:
            rampName= cvaName + "_rotX_ramp"
            rampType = 1 # u-ramps
            newRotXRamp=createRamp(rampName,rampType)
            globRotXRamp = newRotXRamp
        #drive ramp
        if doConnectRotY == True:
            rampName= cvaName + "_rotY_ramp"
            rampType = 1 # u-ramps
            newRotYRamp=createRamp(rampName,rampType)
            globRotYRamp = newRotYRamp
        #drive ramp
        if doConnectRotZ == True:
            rampName= cvaName + "_rotZ_ramp"
            rampType = 1 # u-ramps
            newRotZRamp=createRamp(rampName,rampType)
            globRotZRamp = newRotZRamp


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
    loccountX = cmds.intSliderGrp("loccountXtx",query=True, value = True)
    loccountY = cmds.intSliderGrp("loccountYtx",query=True, value = True)




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

    if doCreateCAPN ==True:
        #create the ColorAatPointNode CAPN
        CAPNType = "scale"
        CAPNScale = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globScaleRamp+".outColor", CAPNScale +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNScale + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNScale + ".inVCoord" ,force = True)
        scalePlug =lastMScreated +"_m"
        cmds.connectAttr(CAPNScale+".outColor", scalePlug +".scale")



    if doConnectPosU ==True:
        CAPNType = "posU"
        CAPNposU = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globPosURamp+".outColor", CAPNposU +".inColor")
        cmds.connectAttr(poca + ".parameterU", CAPNposU + ".inUCoord" ,force = True)
        cmds.connectAttr(poca + ".parameterV", CAPNposU + ".inVCoord" ,force = True)
            #need an rgbto lum node, because its a single value not a color.
        posLumU= cmds.shadingNode("luminance", asUtility = True,name= cvaName +"_lumU")
        cmds.connectAttr(CAPNposU +".outColor", posLumU +".value")
        cmds.connectAttr (posLumU +".outValue", poct +".parameterU")


    if doConnectPosV ==True:
        CAPNType = "posV"
        CAPNposV = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globPosVRamp+".outColor", CAPNposV +".inColor")
        cmds.connectAttr(poca + ".parameterU", CAPNposV + ".inUCoord" ,force = True)
        cmds.connectAttr(poca + ".parameterV", CAPNposV + ".inVCoord" ,force = True)
            #need an rgbto lum node, because its a single value not a color.
        posLumV= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumV")
        cmds.connectAttr(CAPNposV +".outColor", posLumV +".value")
        cmds.connectAttr (posLumV +".outValue", poct +".parameterV")

    if doConnectRotX ==True:
        CAPNType = "rotX"
        CAPNrotX = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globRotXRamp+".outColor", CAPNrotX +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNrotX + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNrotX + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        rotXLumV= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumRotX")
        cmds.connectAttr(CAPNrotX +".outColor", rotXLumV +".value")
        rotXmdiv = cmds.shadingNode("multiplyDivide", asUtility = True, name= cvaName +"_rotxMdiv")
        cmds.connectAttr(rotXLumV + ".outValue", rotXmdiv + ".input1.input1X.")
        cmds.setAttr(rotXmdiv + ".input2X", 360)
        cmds.connectAttr(rotXmdiv + ".outputX", nameAC + ".offset.offsetX")

    if doConnectRotY ==True:
        CAPNType = "RotY"
        CAPNRotY = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globRotYRamp+".outColor", CAPNRotY +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNRotY + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNRotY + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        RotYLumV= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumRotY")
        cmds.connectAttr(CAPNRotY +".outColor", RotYLumV +".value")
        RotYmdiv = cmds.shadingNode("multiplyDivide", asUtility = True, name= cvaName +"_RotYMdiv")
        cmds.connectAttr(RotYLumV + ".outValue", RotYmdiv + ".input1.input1X.")
        cmds.setAttr(RotYmdiv + ".input2X", 360)
        cmds.connectAttr(RotYmdiv + ".outputX", nameAC + ".offset.offsetY")

    if doConnectRotZ ==True:
        CAPNType = "RotZ"
        CAPNRotZ = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globRotZRamp+".outColor", CAPNRotZ +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNRotZ + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNRotZ + ".inVCoord" ,force = True)
        #need an rgbto lum node, because its a single value not a color.
        RotZLumV= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumRotZ")
        cmds.connectAttr(CAPNRotZ +".outColor", RotZLumV +".value")
        RotZmdiv = cmds.shadingNode("multiplyDivide", asUtility = True, name= cvaName +"_RotZMdiv")
        cmds.connectAttr(RotZLumV + ".outValue", RotZmdiv + ".input1.input1X.")
        cmds.setAttr(RotZmdiv + ".input2X", 360)
        cmds.connectAttr(RotZmdiv + ".outputX", nameAC + ".offset.offsetZ")


    if doConnectDrive ==True:
        CAPNType = "drive"
        CAPNDrive = cmds.shadingNode("CVA_ColorAtPointNode", asUtility=True, name = cvaName + "_CAPN_" +CAPNType)

        cmds.connectAttr(globDriveRamp+".outColor", CAPNDrive +".inColor")
        cmds.connectAttr(poct + ".parameterU", CAPNDrive + ".inUCoord" ,force = True)
        cmds.connectAttr(poct + ".parameterV", CAPNDrive + ".inVCoord" ,force = True)
            #need an rgbto lum node, because its a single value not a color.
        lumDrive= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumV")
        cmds.connectAttr(CAPNDrive +".outColor", lumDrive +".value")
            #connect drive
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
        mel.eval("curve -d 1 -p -1 0 0 -p 0 -1 0 -p 1 0 0 -p 0 1 0 -p -1 0 0 -p 0 0 1 -p 1 0 0 -p 0 0 -1 -p -1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8; ")


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
    cmds.addAttr (ln="drive_offset", sn="dvo", k= True, dv=0)
    cmds.addAttr (ln = "v_pos", k = True, minValue=0, maxValue=1, dv = 0)
    cmds.addAttr (ln = "u_pos", k = True, minValue=0, maxValue=1, dv = 0)
    cmds.addAttr (ln = "v_pos_offset", k = True, dv = 0)
    cmds.addAttr (ln = "u_pos_offset", k = True, dv = 0)
    cmds.addAttr (ln = "v_pos_mult", k = True, dv = 0)
    cmds.addAttr (ln = "u_pos_mult", k = True, dv = 0)

    #connecting lost uniformscale
    #if doConnectUscale == True:
    cmds.connectAttr(master[0] + ".uscale",master[0] + ".scaleX")
    cmds.connectAttr(master[0] + ".uscale",master[0] + ".scaleY")
    cmds.connectAttr(master[0] + ".uscale",master[0] + ".scaleZ")


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

    #create with asset.
    if doAutoCreateMS ==True:
        iX=0
        iY=0
        addAssetCVA(iX,iY,inMode)

def createLocNew(masterName):
    txFieldName = cmds.textField("locName",  q=True, text = True)#get name from text feild
    masterName = "%s_%s" % (txFieldName,cvaAlphaCounter)
    cvaAlphaCountUp(cvaAlphaCounter)
    typeMS = "loc"
    locOB = createMS(masterName,typeMS)



def createMaster(masterName):
    txFieldName = cmds.textField("masterName",  q=True, text = True)#get name from text feild
    masterName = "%s_%s" % (txFieldName,cvaAlphaCounter)
    cvaAlphaCountUp(cvaAlphaCounter)
    typeMS="master"#setting the creation type.
    masterOB = createMS(masterName,typeMS)


def createPeon(masterName):

    txFieldName = cmds.textField("peonName",  q=True, text = True)#get name from text feild
    masterName = "%s_%s" % (txFieldName,cvaAlphaCounter)
    cvaAlphaCountUp(cvaAlphaCounter)
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
    if doConnectUscale == True:
        cmds.connectAttr(master +".uniform_scale", peon + ".uniform_scale")
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
    if doConnectDrive == True:
        cmds.connectAttr(master +".drive", peonGrp + ".drive")
    if doConnectUscale == True:
        cmds.connectAttr(master +".uniform_scale", peon + ".uniform_scale")


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

def parentScaleFol (*args):
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
    #offseting the contrain cuz hair follicles are tilted.
    cmds.parentConstraint (master,peonGrp, mo=True)

    cmds.scaleConstraint(master,peonGrp, mo = True)

    #connect drive.
    #if doConnectDrive == True:
    #    cmds.connectAttr(master +".drive", peonGrp + ".drive")
    #if doConnectUscale == True:
    #    cmds.connectAttr(master +".uniform_scale", peon + ".uniform_scale")




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
    print"running select"




    if inMode == 1:

        selectAssetID ()
        nameSpaceRef = "%s_%s_%s_%s" % (cvaName,iX,iY,cvaAlphaCounter)
        cvaAlphaCountUp
        connectCVA = True
        cmds.file( fileLocation, r=True, type = "mayaAscii", namespace= nameSpaceRef)
        if connectCVA == True:
            getPeonAss="%s:peon_aaa"%nameSpaceRef
            cmds.select(lastMScreated,getPeonAss)

            attachMS()
#import
    if inMode == 2:
        nameSpaceRef = "%s_%s_%s_%s" % (cvaName,iX,iY,cvaAlphaCounter)
        cvaAlphaCountUp
        connectCVA = True
        cmds.file( fileLocation, i=True, type = "mayaAscii", namespace= nameSpaceRef)
        if connectCVA == True:
            getPeonAss="%s:peon_aaa"%nameSpaceRef
            cmds.select(lastMScreated,getPeonAss)
            attachMS()
#duplicate
    if inMode == 3:
        nameSpaceRef = "%s_%s_%s_%s_%s" % (cvaName,superDuper[0],iX,iY,cvaAlphaCounter)
        cvaAlphaCountUp
        connectCVA = True
        cmds.select(superDuper)
        cmds.duplicate(n= nameSpaceRef)
        if connectCVA == True:
            getPeonAss=nameSpaceRef
            cmds.select(lastMScreated,getPeonAss)
            parentScaleOn()
#duplicate instance
    if inMode == 4:
        nameSpaceRef = "%s_%s_%s_%s_%s" % (cvaName,superDuper[0],iX,iY,cvaAlphaCounter)
        cvaAlphaCountUp
        connectCVA = True
        cmds.select(superDuper)
        cmds.duplicate(n= nameSpaceRef,ilf =True)
        if connectCVA == True:
            getPeonAss=nameSpaceRef
            cmds.select(lastMScreated,getPeonAss)
            parentScaleOn()

#add Multi Ass prototype
def addMultiAssetCVA(assetID,isRef):
    #set the global name space to the field.
    global myNameSpace

    nameSpaceField="name_space_a"


    inputField="inputField_a"
    myNameSpaceF = cmds.textField(nameSpaceField, query= True, tx=True)
    myNameSpace = "%s_%s" %(myNameSpaceF,cvaAlphaCounter)

    #fileLocation = cmds.textField(inputField, query=True, text = True)
    mSel = cmds.ls(sl=True)

    aCount = len(mSel)

    cmds.file( fileLocation, r=True, type = "mayaAscii", namespace= myNameSpace)
    for iray in xrange (0,aCount):
        print iray
        multiLocID = multiLocList[iray]
        print multiLocList[iray]
        cvaAlphaCountUp (cvaAlphaCounter)
#old
        getPeonAss="%s:%s"% (myNameSpace,multiLocID)
        cmds.select(mSel[iray],getPeonAss)
        attachMS()
    cmds.select(multLocList[0])





##Loc Array aka lamprey
def locArray(masterName):

    masterName = cvaName
    typeMS = "master"
    selArray = cmds.ls(sl=True)
    aCount = len(selArray)
    print aCount


    for iray in xrange (0,aCount):

        irayName = "%s_%s" % (masterName,cvaAlphaCounter)

        cmds.select(selArray[iray])
        irayPos = cmds.xform(query=True, worldSpace=True, rotatePivot =True)
        irayRot = cmds.xform(query=True, worldSpace=True, rotation =True)
        iraySca = cmds.xform(query=True, worldSpace=True, scale =True)
        if doFolUpgrade ==True:

            folU=.1
            folV=1

            #print inputFol[0]
            folUpgrade (folU,folV,irayName)
        noAutoCreateMs()
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
        if createWithAss ==True:
            iX=iray
            iY=iray

            addAssetCVA(iX,iY,inMode)

        cvaAlphaCountUp(cvaAlphaCounter)


            #
############new main looped.  Creates a point on surface node.
def folUpgrade (uCoord,vCoord,folName):
    paraU = uCoord
    paraV = vCoord
    folName=folName



    folSel = cmds.ls(sl=True)
    cmds.addAttr (folSel, ln = "drive", k = True, dv = 0)
    cmds.addAttr (folSel, ln = "uniform_scale", k = True, dv = 1)
    inputFolShape = cmds.listRelatives(folSel, shapes=True)
    inputFol = inputFolShape
    inputColor = "ramp1"

    if doCreateCAPN == True:
    #create CAPN
        CAPNType = "folCAPN"
        createCAPN(CAPNType,paraU,paraV,inputColor,inputFol[0])
    #need an rgbto lum node, because its a single value not a color.
    #addDrive to foli


    #create the pos for the posistion aka poca
        lumDrive= cmds.shadingNode("luminance", asUtility = True, name= cvaName +"_lumV")
        cmds.connectAttr(lastCAPN +".outColor", lumDrive +".value")
    #connect drive
        drivePlug = str(folSel)
        cmds.connectAttr (lumDrive +".outValue", folSel[0] +".drive")





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
    nameAC = cmds.createNode ("aimConstraint" ,parent = aimconParent, name = cvaName + "_aimcon" + lastMScreated )

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
    if createWithAss ==True:
        iX=0
        iY=0
        addAssetCVA(iX,iY,inMode)
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
