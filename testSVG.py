from PyQt4 import QtGui, QtCore, QtSvg
import sys

class TestQG(QtGui.QWidget):
    
    def __init__(self, parent=None):
        
        super(TestQG, self).__init__(parent)

        mlayout = QtGui.QVBoxLayout()
        
        test = TestQGV(self)
        mlayout.addWidget(test)
        
        self.setLayout(mlayout)
        #self.resize(QtCore.QSize(400,400))

class TestQGV(QtGui.QGraphicsView):
    
    def __init__(self, parent):
        
        super(TestQGV, self).__init__(parent)
        
        self.sc = QtGui.QGraphicsScene()
        
        text = TestQGI() 
        
        svg = QtSvg.QGraphicsSvgItem('/home/personal_folders/ji.choi/Downloads/foo.svg')
        
        sca = QtCore.QSize()
        sca.scale(100,100, QtCore.Qt.KeepAspectRatio)
        
        svg.setScale(3)

        self.sc.addItem(svg)
        
        #self.sc.addItem(text)
        

        self.setScene(self.sc)
        #self.sc.addSimpleText('test test')

    def test(self):
        print 'test'

class TestQGI(QtGui.QGraphicsPolygonItem):
    
    def __init__(self, parent=None):
        
        super(TestQGI, self).__init__(parent)
        
        tv = [[6.0000000000000018, 6.0000000000000142], [6.0000000000000018, -5.9999999999999858], [-5.9999999999999982, -5.9999999999999858], [-5.9999999999999982, 6.0000000000000142], [-5.9999999999999982, 6.0000000000000142]]
        
        poly = QtGui.QPolygonF()
        
        for x in tv:
            poly.append(QtCore.QPointF(x[0]*10,x[1]*10))
        
        self.setPolygon(poly)
        


class TestQGIT(QtGui.QGraphicsSimpleTextItem):
    
    def __init__(self, parent=None):
        
        super(TestQGIT, self).__init__(parent)
        self.setText('test')

'''
class TestSVG(QtSvg.QGraphicsSvgItem):
    def __init__(self, parent=None):
        
        self.set
'''

# /home/personal_folders/ji.choi/Downloads

def main():
    app = QtGui.QApplication(sys.argv)
    win = TestQG()
    win.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
