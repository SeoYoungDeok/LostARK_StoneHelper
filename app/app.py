import sys
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QCompleter,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LostARK StoneHelper")
        self.setFixedSize(QSize(560, 460))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # settings layout
        layout1 = QHBoxLayout()
        layout1.addWidget(self.setModeLayout())
        layout1.addWidget(self.setMonitorLayout())
        main_layout.addLayout(layout1)

        # detection layout
        layout2 = QVBoxLayout()
        layout2.addWidget(self.setDetectionLayout())
        main_layout.addLayout(layout2)

        # engraving layout
        layout3 = QVBoxLayout()
        layout3.addWidget(self.setEngravingLayout())
        main_layout.addLayout(layout3)

        central_widget.setLayout(main_layout)

    def setModeLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(300, 70))
        widget.setObjectName("layout")

        btn_77 = QPushButton("77 모드")
        btn_77.setObjectName("enabled")
        btn_97 = QPushButton("97 모드")
        btn_97.setObjectName("disabled")
        cmb_engraving = QComboBox()
        # fmt: off
        engraving = ["7 각인 선택", "각성", "강령술", "강화 방패", "결투의 대가", "구슬동자", "굳은 의지", "급소타격", "기습의 대가", "긴급 구조", "달인의 저력", "돌격대장", "마나 효율 증가", "마나의 흐름", "바리케이드", "번개의 분노", "부러진 뼈", "분쇄의 주먹", "불굴", "선수필승", "속전속결", "슈퍼 차지", "승부사", "시선 집중", "실드 관통", "아드레날린", "안정된 상태", "약자 무시", "에테르 포식자", "여신의 가호", "예리한 둔기", "원한", "위기 모면", "저주받은 인형", "전문의", "정기 흡수", "정밀 단도", "중갑 착용", "질량 증가", "최대 마나 증가", "추진력", "타격의 대가", "탈출의 명수", "폭발물 전문가"]
        # fmt: on
        cmb_engraving.addItems(engraving)
        cmb_engraving.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        line_edit = QLineEdit()
        cmb_engraving.setLineEdit(line_edit)
        completer = QCompleter(engraving)
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        cmb_engraving.setCompleter(completer)

        layout = QHBoxLayout()
        layout.addWidget(btn_77)
        layout.addWidget(btn_97)
        layout.addWidget(cmb_engraving)

        widget.setLayout(layout)
        return widget

    def setMonitorLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(234, 70))
        widget.setObjectName("layout")

        btn_select_monitor = QPushButton("모니터\n선택")
        btn_select_monitor.setObjectName("setMonitorBtn")
        lb_select_monitor = QLabel("선택된 모니터 없음")
        ckb_21_9 = QCheckBox()
        lb_21_9 = QLabel("21:9 사용여부")

        layout = QHBoxLayout()

        v_layout = QVBoxLayout()
        v_layout.addWidget(lb_select_monitor)
        h_layout = QHBoxLayout()
        h_layout.addWidget(ckb_21_9)
        h_layout.addWidget(lb_21_9)
        v_layout.addLayout(h_layout)

        layout.addWidget(btn_select_monitor)
        layout.addLayout(v_layout)

        widget.setLayout(layout)
        return widget

    def setDetectionLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 140))
        widget.setObjectName("layout")

        label = QLabel("인식하고 세공 시작")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)

        widget.setLayout(layout)
        return widget

    def setEngravingLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 220))
        widget.setObjectName("layout")

        layout = QVBoxLayout()

        increase_engraving_layout1 = QHBoxLayout()
        lb_increase_engraving1 = QLabel()
        lb_increase_engraving1.setObjectName("increaseEngraving")
        lb_increase_engraving1.setFixedSize(50, 50)
        lb_increase_engraving1.setScaledContents(True)
        increase_engraving_layout1.addWidget(lb_increase_engraving1)
        for i in range(1, 11):
            label = QLabel("P")
            label.setObjectName(f"point_1_{i}")
            label.setPixmap(QPixmap("app/resource/normal.png"))
            label.setFixedSize(26, 26)
            label.setScaledContents(True)
            increase_engraving_layout1.addWidget(label)

        increase_engraving_layout2 = QHBoxLayout()
        lb_increase_engraving2 = QLabel()
        lb_increase_engraving2.setObjectName("increaseEngraving")
        lb_increase_engraving2.setFixedSize(50, 50)
        lb_increase_engraving2.setScaledContents(True)
        increase_engraving_layout2.addWidget(lb_increase_engraving2)
        for i in range(1, 11):
            label = QLabel("P")
            label.setObjectName(f"point_2_{i}")
            label.setPixmap(QPixmap("app/resource/normal.png"))
            label.setFixedSize(26, 26)
            label.setScaledContents(True)
            increase_engraving_layout2.addWidget(label)

        increase_engraving_layout3 = QHBoxLayout()
        lb_increase_engraving3 = QLabel()
        lb_increase_engraving3.setObjectName("decreaseEngraving")
        lb_increase_engraving3.setFixedSize(50, 50)
        lb_increase_engraving3.setScaledContents(True)
        increase_engraving_layout3.addWidget(lb_increase_engraving3)
        for i in range(1, 11):
            label = QLabel("P")
            label.setObjectName(f"point_3_{i}")
            label.setPixmap(QPixmap("app/resource/normal.png"))
            label.setFixedSize(26, 26)
            label.setScaledContents(True)
            increase_engraving_layout3.addWidget(label)

        layout.addLayout(increase_engraving_layout1)
        layout.addLayout(increase_engraving_layout2)
        layout.addLayout(increase_engraving_layout3)

        widget.setLayout(layout)
        return widget


app = QApplication(sys.argv)
app.setStyleSheet(Path("qss/main.qss").read_text())

window = MainWindow()
window.show()

app.exec()
