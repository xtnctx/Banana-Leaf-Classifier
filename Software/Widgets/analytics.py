from PyQt5 import QtWidgets, QtGui, QtCore, QtChart
from Config import settings

class AnalyticsWindow(QtWidgets.QWidget):
    WIDTH = settings.ANALYTICS_WIDTH
    HEIGHT = settings.ANALYTICS_HEIGHT

    title = ''
    created = ''
    images = []
    image_count = 0
    blacksig = {}
    yellowsig = {}
    overall_confidence = 0.

    def __init__(self, data:dict):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout(self)

        self.title = data['title']
        self.created = data['created']
        self.images = data['images']
        self.image_count = data['image_count']
        self.blacksig = data['black_sigatoka']
        self.yellowsig = data['yellow_sigatoka']
        self.overall_confidence = data['overall_confidence']

        # TITLE & DATE
        titleFrame = QtWidgets.QFrame()
        titleLayout = QtWidgets.QVBoxLayout(titleFrame)
        titleLayout.setSpacing(0)
        titleLayout.setContentsMargins(0, 0, 0, 0)

        titleLabel = QtWidgets.QLabel(self.title)
        titleLabel.setFont(QtGui.QFont("Poppins", pointSize=12, weight=70))
        titleLayout.addWidget(titleLabel)

        dateLabel = QtWidgets.QLabel(', '.join(self.created.split(',')[1:3]))
        dateLabel.setToolTip(self.created)
        dateLabel.setFont(QtGui.QFont("Poppins", pointSize=8, weight=60))
        titleLayout.addWidget(dateLabel)

        # TOP-LEFT
        topleftFrame = QtWidgets.QFrame()
        topleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        topleftLayout = QtWidgets.QVBoxLayout(topleftFrame)

        titleOverallLayout = QtWidgets.QVBoxLayout()
        titleOverallLayout.setSpacing(0)
        titleOverallLayout.setContentsMargins(0, 0, 0, 0)

        titleOverallLabel = QtWidgets.QLabel('Overall Confidence')
        titleOverallLabel.setFont(QtGui.QFont("Poppins Medium", pointSize=10, weight=60))
        titleOverallLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleOverallLayout.addWidget(titleOverallLabel)

        self.overallConfidenceLabel = QtWidgets.QLabel('{:.2f}%'.format(self.overall_confidence * 100))
        self.overallConfidenceLabel.setFont(QtGui.QFont("Poppins", pointSize=22, weight=75))
        self.overallConfidenceLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleOverallLayout.addWidget(self.overallConfidenceLabel)
        

        subTotalLayout = QtWidgets.QGridLayout()
        subTotalLayout.setContentsMargins(10, 0, 10, 0)
        subTotalFont = QtGui.QFont("Poppins Medium", pointSize=8, weight=60)

        yellowSigatokaTotalLabel = QtWidgets.QLabel(settings.y_sigatoka)
        yellowSigatokaTotalLabel.setFont(subTotalFont)
        subTotalLayout.addWidget(yellowSigatokaTotalLabel, 0, 0, 1, 1)

        self.yellowSigatokaTotalConfidence = QtWidgets.QLabel('{:.2f}%'.format(self.yellowsig['total_confidence'] * 100))
        self.yellowSigatokaTotalConfidence.setAlignment(QtCore.Qt.AlignCenter)
        self.yellowSigatokaTotalConfidence.setFont(subTotalFont)
        subTotalLayout.addWidget(self.yellowSigatokaTotalConfidence, 0, 1, 1, 3)


        blackSigatokaTotalLabel = QtWidgets.QLabel(settings.b_sigatoka)
        blackSigatokaTotalLabel.setFont(subTotalFont)
        subTotalLayout.addWidget(blackSigatokaTotalLabel, 1, 0, 1, 1)

        self.blackSigatokaTotalConfidence = QtWidgets.QLabel('{:.2f}%'.format(self.blacksig['total_confidence'] * 100))
        self.blackSigatokaTotalConfidence.setAlignment(QtCore.Qt.AlignCenter)
        self.blackSigatokaTotalConfidence.setFont(subTotalFont)
        subTotalLayout.addWidget(self.blackSigatokaTotalConfidence, 1, 1, 1, 3)

        topleftLayout.addLayout(titleOverallLayout)
        topleftLayout.addLayout(subTotalLayout)

        # BOTTOM-LEFT
        bottomleftFrame = QtWidgets.QFrame()
        bottomleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        bottomleftLayout = QtWidgets.QVBoxLayout(bottomleftFrame)

        pieTitle = QtWidgets.QLabel('Detected Diseases')
        pieTitle.setAlignment(QtCore.Qt.AlignCenter)
        pieTitle.setFont(QtGui.QFont("Poppins Medium", pointSize=10, weight=60))

        self.pieSeries = QtChart.QPieSeries()
        self.pieSeries.append('Y', self.yellowsig['count'])
        self.pieSeries.append('B', self.blacksig['count'])
        self.pieSeries.setHoleSize(0.40)
        # pieSeries.setFont(QtGui.QFont("Poppins Medium", pointSize=7, weight=60))

        self.chart = QtChart.QChart()
        self.chart.addSeries(self.pieSeries)
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chart.setContentsMargins(0, 0, 0, 0)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setBackgroundRoundness(0)

        self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        self.chart.legend().setFont(QtGui.QFont("Poppins Medium", pointSize=8, weight=60))
        

        self._chart_view = QtChart.QChartView(self.chart)
        self._chart_view.setAlignment(QtCore.Qt.AlignCenter)
        self._chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self._chart_view.setContentsMargins(0, 0, 0, 0)


        bottomleftLayout.addWidget(pieTitle)
        bottomleftLayout.addWidget(self._chart_view)

        

        # SPLITTER FOR TOP-LEFT & BOTTOM-LEFT
        splitterLeft = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitterLeft.addWidget(titleFrame)
        splitterLeft.addWidget(topleftFrame)
        splitterLeft.addWidget(bottomleftFrame)
        splitterLeft.setSizes([100, 400, 600])


        # RIGHT
        rightFrame = QtWidgets.QFrame()
        rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        rightFrameLayout = QtWidgets.QVBoxLayout(rightFrame)

        self.table = ImagesResultTable(images=self.images)
        rightFrameLayout.addWidget(self.table)


        splitterRight = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitterRight.addWidget(splitterLeft)
        splitterRight.addWidget(rightFrame)
        splitterRight.setSizes([180, 600])

        vbox.addWidget(splitterRight)
        self.setLayout(vbox)

        # Center the window
        self.resize(self.WIDTH, self.HEIGHT)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    

class AlignDelegate(QtWidgets.QStyledItemDelegate): # Table.cell.alignCenter 
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter



class ImagesResultTable(QtWidgets.QTableWidget):
    COLUMNS = ['Image', 'Classification', 'Confidence']

    def __init__(self, images:list):
        super().__init__()

        images:list[dict] = images

        print(images)

        self.setGeometry(QtCore.QRect(10, 27, 432, 251))
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSortIndicatorShown(False)

        font = QtGui.QFont("Poppins", pointSize=9, weight=50)
        self.setFont(font)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False) # Row Index
        self.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.setAutoScroll(True)
        self.setAlternatingRowColors(True)
        self.setColumnCount(len(self.COLUMNS))
        self.setRowCount(0)
        self.setupColumns()


    def setupColumns(self):
        font = QtGui.QFont("Poppins Medium", pointSize=7, weight=75)
        for i, c in enumerate(self.COLUMNS):
            item = QtWidgets.QTableWidgetItem(c)
            item.setFont(font)
            self.setHorizontalHeaderItem(i, item)
            self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            self.setItemDelegateForColumn(i, AlignDelegate(self))
        self.verticalHeader().setDefaultSectionSize(44)
        