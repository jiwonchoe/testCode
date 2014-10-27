# Written by jiwon choi

import pymel.core as pm
import pymel.api as pa
import numpy as np
import tbe_maya.rig.rig_nonDeform as trnd
from PyQt4 import QtGui, QtCore
import sip

def getPyQtMayaWindow():
    accessMainWindow = pa.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject) 


class TreeTreeTreeUI(QtGui.QWidget):

    def __init__(self, parent=getPyQtMayaWindow()):
        
        super(TreeTreeTreeUI, self).__init__(parent)
        
        mLayout = QtGui.QVBoxLayout()
        
        btFont = QtGui.QFont()
        btFont.setPointSize(24)
        btFont.setBold(True)
        
        lbFont = QtGui.QFont()
        lbFont.setBold(True)
        lbFont.setPointSize(12)

        
        inText = "TreeTreeTreeTool\n~(o_ O )~ ~(  O_o)~\n1. select -r 'model_gr'\n2. select -add 'shapes'\n3. Push Button"

        lText = QtGui.QLabel(inText)
        lText.setAlignment(QtCore.Qt.AlignHCenter)
        lText.setFont(lbFont)
        
        runBt = QtGui.QPushButton('Big\nButton')
        runBt.setFont(btFont)
        runBt.clicked.connect(self.run)
        
        
        mLayout.addWidget(lText)
        mLayout.addWidget(runBt)
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setLayout(mLayout)
        self.setWindowTitle('TreeTreeTool')
        self.show()
        
        
    def run(self):
        getList = pm.ls(sl=1)
        tree = TreeTreeTree(getList[0], getList[1])
        tree.run()

class TreeTreeTree():

    def __init__(self, model, shapes):

        self.model = model
        self.shapes =  shapes
        
        self.ctrlName = []
        self.byby = []

    def findItem(self, itemList, findString):
    
        getItem = []
    
        for x in itemList:
            if x.name().find(findString) != -1:
                getItem.append(x)
    
        return getItem[0].getChildren()
    
    def findList(self, itemList, findString):
        
        getItem = []
        
        for x in itemList:
            if x.name().find(findString) != -1:
                getItem.append(x)
        
        return getItem[0]
    
    def popItem(self, itemList, findString):
    
        reList = []
        
        for x in itemList:
            if x.name().find(findString) == -1:
                reList.append(x)
        
        return reList
    
    def lockHide(self, attrList):
        
        for x in attrList:
            x.setKeyable(0)
            x.lock()
    
    def inGroup(self, obj):
    
        gp = pm.createNode('transform', n=obj.name() + '_gp')
        pc = pm.parentConstraint(obj, gp)
        pm.delete(pc)
        pr.setParent(obj.getParent())
        obj.setParent(gp)
        
        return gp
    
    def animUU(self, nodeName, timeValue, value):
    
        dgmod = pa.MDGModifier()
        keyNode = dgmod.createNode('animCurveUU')
        dgmod.renameNode(keyNode, nodeName)
        dgmod.doIt()
        
        key = pa.MFnAnimCurve()
        
        key.setObject(keyNode)
        
        key.addKey(timeValue[0], value[0], pa.MFnAnimCurve.kTangentAuto, pa.MFnAnimCurve.kTangentAuto)
        key.addKey(timeValue[1], value[1], pa.MFnAnimCurve.kTangentAuto, pa.MFnAnimCurve.kTangentAuto)
        key.addKey(timeValue[2], value[2], pa.MFnAnimCurve.kTangentAuto, pa.MFnAnimCurve.kTangentAuto)
       
        keys = pm.PyNode(key.name())
        
        return keys

    def getItem(self):

        shapesList = self.shapes.getChildren()
        
        self.lowLeaf = self.findItem(shapesList, 'lo')
        self.hiLeaf = self.findItem(shapesList, 'hi')
        self.trunk = self.findItem(shapesList, 'trunk')

        modelList = self.model.getChildren()
        
        self.modelLeavesHi = self.findList(self.findItem(modelList, 'hi'), 'leaves')
        self.modelTrunkHi = self.findList(self.findItem(modelList, 'hi'), 'trunk')
        
        self.modelLeavesLow = self.findList(self.findItem(modelList, 'lo'), 'leaves')
        self.modelTrunkLow = self.findList(self.findItem(modelList, 'lo'), 'trunk')

        self.hiBlend = pm.blendShape(self.hiLeaf, self.modelLeavesHi,foc=1)[0]
        self.loBlend = pm.blendShape(self.lowLeaf, self.modelLeavesLow,foc=1)[0]
        self.hiTrunkBlend = pm.blendShape(self.trunk, self.modelTrunkHi,foc=1)[0]
        self.loTrunkBlend = pm.blendShape(self.trunk, self.modelTrunkLow,foc=1)[0]


    def makeCtrl(self):
        
        self.outCurveA = pm.curve(d=1, p=[[0, 0, 0], [-1, 0, 0], [-1, 10, 0], [1, 10, 0], [1, 0, 0], [0, 0, 0]], n='cycle_guideLine' + '')
        self.inCurveA = pm.curve(d=1, p=[[0, -0.707107, 0], [-0.707107, 0, 0], [0, 0.707107, 0], [0.707107, 0, 0], [0, -0.707107, 0]], n='cycle' + '_C')
        
        self.outCurveB = pm.curve(d=1, p=[[0, 0, 0], [-1, 0, 0], [-1, 10, 0], [1, 10, 0], [1, 0, 0], [0, 0, 0]], n='intensity_guideLineB' + '')
        self.inCurveB = pm.curve(d=1, p=[[0, -0.707107, 0], [-0.707107, 0, 0], [0, 0.707107, 0], [0.707107, 0, 0], [0, -0.707107, 0]], n='intensity' + '_C')

        self.outCurveA.overrideEnabled.set(1)
        self.outCurveA.overrideColor.set(17)
        self.outCurveA.template.set(1)
        self.inCurveA.overrideEnabled.set(1)
        self.inCurveA.overrideColor.set(15)
        
        self.outCurveB.overrideEnabled.set(1)
        self.outCurveB.overrideColor.set(17)
        self.outCurveB.template.set(1)
        self.inCurveB.overrideEnabled.set(1)
        self.inCurveB.overrideColor.set(15)
        
        self.inCurveA.setLimit('translateMinY', 0)
        self.inCurveA.setLimit('translateMaxY', 10)
        
        self.inCurveB.setLimit('translateMinY', 0)
        self.inCurveB.setLimit('translateMaxY', 10)
        
        inCurveALockHideList = self.popItem(self.inCurveA.listAttr(k=1), 'translateY')
        inCurveBLockHideList = self.popItem(self.inCurveB.listAttr(k=1), 'translateY')
        
        self.lockHide(inCurveALockHideList)
        self.lockHide(inCurveBLockHideList)
        self.lockHide(self.outCurveA.listAttr(k=1))
        self.lockHide(self.outCurveB.listAttr(k=1))
       
        ActrlGp = pm.createNode('transform', n='cycle_ctrl_gp')
        BctrlGp = pm.createNode('transform', n='intensity_ctrl_gp')
        
        self.inCurveA.setParent(ActrlGp)
        self.inCurveB.setParent(BctrlGp)
        self.outCurveA.setParent(ActrlGp)
        self.outCurveB.setParent(BctrlGp)
        
        self.scaleGp = pm.createNode('transform', n='ctrl_scale_gp')
        
        ActrlGp.tx.set(10)
        ActrlGp.ty.set(10)
        ActrlGp.setParent(self.scaleGp)
        
        BctrlGp.tx.set(14)
        BctrlGp.ty.set(10)
        BctrlGp.setParent(self.scaleGp)
        
        self.scaleGp.s.set(10,10,10)

    def animKey(self):

        a = list(np.arange(0,10,(10/8.0)))
        a += [10]
        
        tValue = []
        self.animKeyNode = []
        
        aa, bb, cc = a[0], a[0]+a[1], a[0]+a[2]
        
        for x in range(7):
            tValue.append([aa,bb,cc])
            aa += a[1]
            bb += a[1]
            cc += a[1]
            self.animKeyNode.append(self.animUU('setKey_%02d' % (x+1), tValue[x], [0.0, 1.0, 0.0]))

    def animConn(self):

        for i in self.animKeyNode:
            self.inCurveA.ty >> i.input
        
        for k in self.hiTrunkBlend.weightIndexList():
            self.animKeyNode[k].output >> self.hiTrunkBlend.w[k]
            self.animKeyNode[k].output >> self.loTrunkBlend.w[k]
            self.animKeyNode[k].output >> self.hiBlend.w[k]
            self.animKeyNode[k].output >> self.loBlend.w[k]
        
        envelopeMTD = pm.createNode('multiplyDivide')
        envelopeMTD.input2X.set(.1)
        envelopeMTD.outputX >> self.hiTrunkBlend.envelope
        envelopeMTD.outputX >> self.loTrunkBlend.envelope
        envelopeMTD.outputX >> self.hiBlend.envelope
        envelopeMTD.outputX >> self.loBlend.envelope
        
        self.inCurveB.ty >> envelopeMTD.input1X

    def simpleRig(self):

        pm.select(self.model, r=1)
        
        toonbox = trnd
        toonbox.run()

        self.scaleGp.setParent(toonbox.tbeTool_rigControlGroupName)
        pm.parentConstraint(toonbox.tbeTool_subGround2CNTName, self.scaleGp)

    def run(self):
        
        self.getItem()
        self.makeCtrl()
        self.animKey()
        self.animConn()
        self.simpleRig()



# test Run



test = TreeTreeTreeUI()






