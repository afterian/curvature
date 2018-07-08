#CVA_inProgress node.
# based off (c) 2007/2008 - Pascal Loef | www.dddpl.tv

#


import maya.OpenMaya as om
import maya.OpenMayaRender as omRender
import maya.OpenMayaMPx as omMPx

kPluginNodeTypeName = "CVA_ColorAtPointNode"
kPluginNodeClassify = "utility/general"
kPluginNodeId = om.MTypeId(0x85123)

# Node definition
class plColorAtPoint(omMPx.MPxNode):
	# class variables
	inColor = om.MObject()
	useSG = om.MObject()
	inSG = om.MObject()
	inPoint = om.MObject()
	useRefPoint = om.MObject()
	refPoint = om.MObject()
	normal = om.MObject()
	tangentU = om.MObject()
	tangentV = om.MObject()
	filterSize = om.MObject()
	useShadowMaps = om.MObject()
	reUseShadowMaps = om.MObject()
	inUCoord = om.MObject()
	inVCoord = om.MObject()
	eyeToWorld = om.MObject()
	time = om.MObject()
	outColor = om.MObject()

	def __init__(self):
		omMPx.MPxNode.__init__(self)

	def compute(self, plug, data):
		if plug == self.outColor or plug.parent()==self.outColor:
			thisNode = self.thisMObject()
			fnThisNode = om.MFnDependencyNode(thisNode)

			uData = data.inputValue(self.inUCoord)
			uValue = uData.asFloat()
			uArray = om.MFloatArray(1)
			uArray.set(uValue,0)

			timeData = data.inputValue(self.time)
			timeValue = timeData.asFloat()

			vData = data.inputValue(self.inVCoord)
			vValue = vData.asFloat()
			vArray = om.MFloatArray(1)
			vArray.set(vValue,0)

			shadowsData = data.inputValue(self.useShadowMaps)
			shadowsValue = shadowsData.asBool()

			reShadowsData = data.inputValue(self.reUseShadowMaps)
			reShadowsValue = reShadowsData.asBool()

			filterSizeData = data.inputValue(self.filterSize)
			filterSizeValue = filterSizeData.asFloat()
			filterSizeArray = om.MFloatArray(1)
			filterSizeArray.set(filterSizeValue,0)

			inPointData = data.inputValue(self.inPoint)
			inPointValue = inPointData.asFloatVector()
			inPointArray = om.MFloatPointArray(1)
			inPointArray.set(0,inPointValue.x,inPointValue.y,inPointValue.z,1)

			useRefPointData = data.inputValue(self.useRefPoint)
			useRefPointValue = useRefPointData.asBool()

			refPointArray = om.MFloatPointArray(1)
			if useRefPointValue:
				refPointData = data.inputValue(self.refPoint)
				refPointValue = refPointData.asFloatVector()
				refPointArray.set(0,refPointValue.x,refPointValue.y,refPointValue.z,1)
			else:
				refPointArray.set(0,inPointValue.x,inPointValue.y,inPointValue.z,1)

			normalData = data.inputValue(self.normal)
			normalValue = normalData.asFloatVector()
			normalArray = om.MFloatVectorArray(1)
			normalArray.set(normalValue,0)

			tangentUData = data.inputValue(self.tangentU)
			tangentUValue = tangentUData.asFloatVector()
			tangentUArray = om.MFloatVectorArray(1)
			tangentUArray.set(tangentUValue,0)

			tangentVData = data.inputValue(self.tangentV)
			tangentVValue = tangentVData.asFloatVector()
			tangentVArray = om.MFloatVectorArray(1)
			tangentVArray.set(tangentVValue,0)

			useSGData = data.inputValue(self.useSG)
			useSGValue = useSGData.asBool()

			plugArray = om.MPlugArray()
			inColorPlugName = ""
			inSGPlugName = ""
			sampleSource = ""
			isSGNode = False

			sgPlug = om.MPlug(thisNode, self.inSG)
			hasConnections = sgPlug.connectedTo(plugArray,1,0)
			if hasConnections:
				inSGPlugName = plugArray[0].name()
				inSGPlugNameSplit = inSGPlugName.split(".")
				sourceNode = om.MObject()
				sourceNode = plugArray[0].node()
				isSGNode = sourceNode.hasFn(om.MFn.kShadingEngine)
				inSGPlugName = inSGPlugNameSplit[0]
			else:
				inSGPlugName = ""

			colorPlug = om.MPlug(thisNode, self.inColor)
			hasConnections = colorPlug.connectedTo(plugArray,1,0)
			if hasConnections :
				inColorData = data.inputValue(self.inColor)
				inColorPlugName = plugArray[0].name()

			if useSGValue:
				if isSGNode:
					sampleSource = inSGPlugName
				elif inSGPlugName == "":
					print ("\"inSG\" has no connections. Please connect the \"message\" attribute of a shadingGroup to \"inSG\"")
					#return om.MStatus.kUnknownParameter
				else:
					print ( inSGPlugName + " is not a shading group. Only the \"message\" attribute of a shadingGroup should be connected to \"inSG\"")
					#return om.MStatus.kUnknownParameter
			else:
				if not inColorPlugName == "":
					sampleSource = inColorPlugName
				else:
					print ("\"inColor\" has no connections")
					#return om.MStatus.kUnknownParameter

			cameraMatData = data.inputValue(self.eyeToWorld)
			cameraMat = om.MFloatMatrix()
			cameraMat = cameraMatData.asFloatMatrix()

			resColors = om.MFloatVectorArray(1)
			resTransparencies = om.MFloatVectorArray(1)

			renderUtil = omRender.MRenderUtil
			renderUtil.sampleShadingNetwork(sampleSource,1,shadowsValue,reShadowsValue,cameraMat,inPointArray,uArray,vArray,normalArray,refPointArray,tangentUArray,tangentVArray,filterSizeArray,resColors,resTransparencies)

			outColorRAttr = fnThisNode.attribute("outColorR")
			outColorRPlug = om.MPlug(thisNode,outColorRAttr)
			outColorRHandle = data.outputValue(outColorRPlug)
			outColorRHandle.setFloat(resColors[0].x)
			outColorRHandle.setClean()

			outColorGAttr = fnThisNode.attribute("outColorG")
			outColorGPlug = om.MPlug(thisNode,outColorGAttr)
			outColorGHandle = data.outputValue(outColorGPlug)
			outColorGHandle.setFloat(resColors[0].y)
			outColorGHandle.setClean()

			outColorBAttr = fnThisNode.attribute("outColorB")
			outColorBPlug = om.MPlug(thisNode,outColorBAttr)
			outColorBHandle = data.outputValue(outColorBPlug)
			outColorBHandle.setFloat(resColors[0].z)
			outColorBHandle.setClean()

			data.setClean(plug)

			#return om.MStatus.kSuccess

		else :
			print ("something Failed")
			#return om.MStatus.kUnknownParameter


def nodeCreator():
	return omMPx.asMPxPtr( plColorAtPoint() )

def nodeInitializer():
	nAttr = om.MFnNumericAttribute()
	tAttr = om.MFnTypedAttribute()
	mmAttr = om.MFnMatrixAttribute()
	mAttr = om.MFnMessageAttribute()
	uAttr = om.MFnUnitAttribute()

	plColorAtPoint.inColor = nAttr.createColor("inColor","ic")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.useSG = nAttr.create("useSG","sg", om.MFnNumericData.kBoolean,0)
	nAttr.setReadable(False)
	nAttr.setChannelBox(True)

	plColorAtPoint.useShadowMaps = nAttr.create("useShadowMaps","shd", om.MFnNumericData.kBoolean,0)
	nAttr.setReadable(False)
	nAttr.setChannelBox(True)

	plColorAtPoint.reUseShadowMaps = nAttr.create("reUseShadowMaps","rsh", om.MFnNumericData.kBoolean,0)
	nAttr.setReadable(False)
	nAttr.setChannelBox(True)

	plColorAtPoint.inSG = mAttr.create("inShadingGroup","isg")
	mAttr.setWritable(True)
	mAttr.setReadable(False)

	plColorAtPoint.inPoint = nAttr.createPoint("inPoint","ip")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.useRefPoint = nAttr.create("useRefPoint","urp", om.MFnNumericData.kBoolean,0)
	nAttr.setReadable(False)
	nAttr.setChannelBox(True)

	plColorAtPoint.refPoint = nAttr.createPoint("refPoint","rp")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.normal = nAttr.createPoint("normal","n")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.tangentU = nAttr.createPoint("tangentU","tu")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.tangentV = nAttr.createPoint("tangentV","tv")
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.filterSize =  nAttr.create("filterSize","fs", om.MFnNumericData.kFloat,0.0)
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.inUCoord =  nAttr.create("inUCoord","iuc", om.MFnNumericData.kFloat,0.0)
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	plColorAtPoint.inVCoord =  nAttr.create("inVCoord","ivc", om.MFnNumericData.kFloat,0.0)
	nAttr.setKeyable(True)
	nAttr.setReadable(False)

	defaultEyeToWorldMatrix = om.MFloatMatrix()
	defaultEyeToWorldMatrix.setToIdentity()
	plColorAtPoint.eyeToWorld = mmAttr.create( "eyeToWorldMatrix", "etw", om.MFnNumericData.kFloat)
	mmAttr.setDefault(defaultEyeToWorldMatrix)
	mmAttr.setHidden(True)
	mmAttr.setReadable(False)
	mmAttr.setKeyable(True)

	plColorAtPoint.time = uAttr.create( "time", "tm",om.MFnUnitAttribute.kTime,0.0)
	uAttr.setHidden(False)
	uAttr.setReadable(False)
	uAttr.setKeyable(True)

	plColorAtPoint.outColor = nAttr.createColor("outColor","oc")
	nAttr.setHidden(True)
	nAttr.setWritable(False)
	nAttr.setReadable(True)
	nAttr.setStorable(False)

	plColorAtPoint.addAttribute(plColorAtPoint.inColor)
	plColorAtPoint.addAttribute(plColorAtPoint.inUCoord)
	plColorAtPoint.addAttribute(plColorAtPoint.inVCoord)
	plColorAtPoint.addAttribute(plColorAtPoint.filterSize)
	plColorAtPoint.addAttribute(plColorAtPoint.useSG)
	plColorAtPoint.addAttribute(plColorAtPoint.useShadowMaps)
	plColorAtPoint.addAttribute(plColorAtPoint.reUseShadowMaps)
	plColorAtPoint.addAttribute(plColorAtPoint.inSG)
	plColorAtPoint.addAttribute(plColorAtPoint.inPoint)
	plColorAtPoint.addAttribute(plColorAtPoint.useRefPoint)
	plColorAtPoint.addAttribute(plColorAtPoint.refPoint)
	plColorAtPoint.addAttribute(plColorAtPoint.normal)
	plColorAtPoint.addAttribute(plColorAtPoint.tangentU)
	plColorAtPoint.addAttribute(plColorAtPoint.tangentV)
	plColorAtPoint.addAttribute(plColorAtPoint.eyeToWorld)
	plColorAtPoint.addAttribute(plColorAtPoint.time)
	plColorAtPoint.addAttribute(plColorAtPoint.outColor)

	plColorAtPoint.attributeAffects(plColorAtPoint.time, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.inColor, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.useSG, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.inSG, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.inPoint, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.useRefPoint, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.refPoint, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.normal, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.tangentU, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.tangentV, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.useShadowMaps, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.reUseShadowMaps, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.inUCoord, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.inVCoord, plColorAtPoint.outColor)
	plColorAtPoint.attributeAffects(plColorAtPoint.eyeToWorld, plColorAtPoint.outColor)

	#return om.MStatus.kSuccess

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject, "Pascal Loef - www.dddpl.tv", "0.3", "Any")
	try:
		mplugin.registerNode( kPluginNodeTypeName, kPluginNodeId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDependNode, kPluginNodeClassify)
	except:
		sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( kPluginNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
		raise
