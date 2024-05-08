import glob
import sys
from pathlib import Path

import cv2
import numpy as np
import win32api
from PIL import ImageGrab
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
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
from ultralytics import YOLO


class SetMonitorWindow(QWidget):
    def __init__(self, label):
        super().__init__()

        self.setWindowTitle("화면세팅")
        self.setObjectName("setMonitorWindow")
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.label = label

        layout = QVBoxLayout()

        self.img_label = QLabel()
        img = cv2.imread("app/resource/no_image.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (320, 180))

        img = QImage(img.data, 320, 180, 320 * 3, QImage.Format.Format_RGB888)
        self.pixmap = QPixmap.fromImage(img)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_label)

        self.monitors = win32api.EnumDisplayMonitors()
        self.monitor_button_list = [
            QPushButton(f"모니터 {i+1}번") for i in range(len(self.monitors))
        ]

        for i, button in enumerate(self.monitor_button_list):
            button.setStyleSheet("background-color: #999999;")
            button.clicked.connect(
                lambda _, idx=i: self.select_monitor_button_clicked(_, idx)
            )
            layout.addWidget(button)

        self.submit_button = QPushButton("선택완료")
        self.submit_button.clicked.connect(self.submit_button_click)
        self.submit_button.setDisabled(True)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setFixedSize(QSize(360, 180 + 100 * (len(self.monitors) + 1)))

    def select_monitor_button_clicked(self, _, moniter_number):
        for i, button in enumerate(self.monitor_button_list):
            if i == moniter_number:
                button.setStyleSheet("background-color: #006ee6;")
            else:
                button.setStyleSheet("background-color: #999999;")

        self.monitor_number = moniter_number
        monitor = self.monitors[moniter_number][0]
        self.left, self.top, self.right, self.bottom = win32api.GetMonitorInfo(monitor)[
            "Monitor"
        ]

        img = ImageGrab.grab(
            bbox=(self.left, self.top, self.right, self.bottom), all_screens=True
        )
        img = np.array(img, dtype=np.float32)
        img = cv2.resize(img, (320, 180))
        img = np.array(img, dtype=np.uint8)

        img = QImage(img.data, 320, 180, 320 * 3, QImage.Format.Format_RGB888)
        self.pixmap = QPixmap.fromImage(img)
        self.img_label.setPixmap(self.pixmap)

        self.label.setText(f"모니터 {self.monitor_number+1}")

        self.submit_button.setEnabled(True)

    def submit_button_click(self):
        self.hide()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = YOLO("app/best.pt")
        self.table_97 = np.load("app/table_97.npy")
        self.table_77 = np.load("app/table_77.npy")
        self.prob = [0.75, 0.65, 0.55, 0.45, 0.35, 0.25]
        self.p = 0
        self.engraving_path = glob.glob("app/resource/increase_engraving*") + glob.glob(
            "app/resource/decrease_engraving*"
        )
        self.p_img_path = glob.glob("app/resource/p*.jpg")

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

        self.mode = "77"
        self.btn_77 = QPushButton("77 모드")
        self.btn_77.setObjectName("enabled")
        self.btn_77.clicked.connect(
            lambda temp="", mode="77": self.modeButtonClicked(mode)
        )
        self.btn_97 = QPushButton("97 모드")
        self.btn_97.setObjectName("disabled")
        self.btn_97.clicked.connect(
            lambda temp="", mode="97": self.modeButtonClicked(mode)
        )
        self.cmb_engraving = QComboBox()
        # fmt: off
        self.engraving_name_list = ["7 각인 선택", "각성", "강령술", "강화 방패", "결투의 대가", "구슬동자", "굳은 의지", "급소타격", "기습의 대가", "긴급 구조", "달인의 저력", "돌격대장", "마나 효율 증가", "마나의 흐름", "바리케이드", "번개의 분노", "부러진 뼈", "분쇄의 주먹", "불굴", "선수필승", "속전속결", "슈퍼 차지", "승부사", "시선 집중", "실드 관통", "아드레날린", "안정된 상태", "약자 무시", "에테르 포식자", "여신의 가호", "예리한 둔기", "원한", "위기 모면", "저주받은 인형", "전문의", "정기 흡수", "정밀 단도", "중갑 착용", "질량 증가", "최대 마나 증가", "추진력", "타격의 대가", "탈출의 명수", "폭발물 전문가"]
        # fmt: on
        self.engraving7 = "7 각인 선택"
        self.cmb_engraving.addItems(self.engraving_name_list)
        self.cmb_engraving.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        line_edit = QLineEdit()
        self.cmb_engraving.setLineEdit(line_edit)
        completer = QCompleter(self.engraving_name_list)
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.cmb_engraving.setCompleter(completer)
        self.cmb_engraving.currentTextChanged.connect(self.engravingComboboxChanged)

        layout = QHBoxLayout()
        layout.addWidget(self.btn_77)
        layout.addWidget(self.btn_97)
        layout.addWidget(self.cmb_engraving)

        widget.setLayout(layout)
        return widget

    def setMonitorLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(234, 70))
        widget.setObjectName("layout")

        btn_select_monitor = QPushButton("모니터\n선택")
        btn_select_monitor.setObjectName("setMonitorBtn")
        btn_select_monitor.clicked.connect(self.setMonitorButtonClicked)
        self.lb_select_monitor = QLabel("선택된 모니터 없음")
        self.lb_select_monitor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ckb_21_9 = QCheckBox()
        lb_21_9 = QLabel("21:9 사용여부")

        layout = QHBoxLayout()

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.lb_select_monitor)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ckb_21_9)
        h_layout.addWidget(lb_21_9)
        v_layout.addLayout(h_layout)

        layout.addWidget(btn_select_monitor)
        layout.addLayout(v_layout)

        widget.setLayout(layout)

        self.set_monitor_window = SetMonitorWindow(self.lb_select_monitor)
        return widget

    def setDetectionLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 140))
        widget.setObjectName("layout")

        self.btn_detect = QPushButton("인식하고 세공 시작")
        self.btn_detect.setStyleSheet(
            "border: 0px; font-size:32px; font-weight: bold; height: 100%;"
        )
        self.btn_detect.clicked.connect(self.detectButtonClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_detect)

        widget.setLayout(layout)
        return widget

    def setEngravingLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 220))
        widget.setObjectName("layout")

        layout = QVBoxLayout()

        # engraving[0], engraving[1] is increase engraving / engraving[2] is decrease engraving
        self.engraving_list = []
        # increase engraving point
        self.point_list1 = []
        self.point_list2 = []
        # decrease engraving point
        self.point_list3 = []

        for n in range(3):
            h_layout = QHBoxLayout()
            lb_engraving = QLabel()
            # if n < 2:
            #     lb_engraving.setStyleSheet(
            #         "border-radius: 25px; border: 2px solid #7BD3EA;"
            #     )
            # else:
            #     lb_engraving.setStyleSheet(
            #         "border-radius: 25px; border: 2px solid #C74B50;"
            #     )
            lb_engraving.setStyleSheet("border-radius: 25px; border: 2px solid black;")
            lb_engraving.setFixedSize(50, 50)
            lb_engraving.setScaledContents(True)
            h_layout.addWidget(lb_engraving)
            self.engraving_list.append(lb_engraving)

            for _ in range(1, 11):
                label = QLabel()
                label.setPixmap(QPixmap("app/resource/normal.png"))
                label.setFixedSize(26, 26)
                label.setScaledContents(True)
                h_layout.addWidget(label)
                if n == 0:
                    self.point_list1.append(label)
                elif n == 1:
                    self.point_list2.append(label)
                elif n == 2:
                    self.point_list3.append(label)

            layout.addLayout(h_layout)

        widget.setLayout(layout)
        return widget

    def modeButtonClicked(self, mode):
        if mode == "77":
            self.btn_77.setStyleSheet("border: 3px solid #EFBC9B;")
            self.btn_97.setStyleSheet("border: 1px solid #D9D9D9;")
            self.mode = "77"
        elif mode == "97":
            self.btn_77.setStyleSheet("border: 1px solid #D9D9D9;")
            self.btn_97.setStyleSheet("border: 3px solid #EFBC9B;")
            self.mode = "97"

    def engravingComboboxChanged(self):
        self.engraving7 = self.cmb_engraving.currentText()

        try:
            if self.engraving_name_list.index(self.engraving7) - 1 == int(
                self.cls_idx[0]
            ):
                self.mode = "79"
            elif self.engraving_name_list.index(self.engraving7) - 1 == int(
                self.cls_idx[11]
            ):
                self.mode = "97"
        except:
            pass

    def setMonitorButtonClicked(self):
        self.set_monitor_window.show()

    def detectButtonClicked(self):
        self.left = self.set_monitor_window.left
        self.top = self.set_monitor_window.top
        self.right = self.set_monitor_window.right
        self.bottom = self.set_monitor_window.bottom

        if self.ckb_21_9.isChecked():
            margin_w = (
                (self.right - self.left) - ((self.right - self.left) * 0.75)
            ) / 2
            margin_h = (
                (self.bottom - self.top) - ((self.bottom - self.top) * 0.75)
            ) / 2
            self.left += margin_w
            self.top += margin_h
            self.right -= margin_w
            self.bottom -= margin_h

        img = ImageGrab.grab(
            bbox=(self.left, self.top, self.right, self.bottom), all_screens=True
        )

        result = self.model.predict(img, imgsz=736, device="cpu", conf=0.5)

        xywh = result[0].boxes.xywh.numpy()
        sort_idx = np.argsort(xywh[:, 1])
        xywh = xywh[sort_idx, :]
        self.cls_idx = result[0].boxes.cls[sort_idx]

        line1, line2, line3 = np.vsplit(xywh, 3)
        self.line1 = line1[np.argsort(line1[:, 0]), :]
        self.line2 = line2[np.argsort(line2[:, 0]), :]
        self.line3 = line3[np.argsort(line3[:, 0]), :]

        self.engraving_list[0].setPixmap(
            QPixmap(self.engraving_path[int(self.cls_idx[0])])
        )
        self.engraving_list[1].setPixmap(
            QPixmap(self.engraving_path[int(self.cls_idx[11])])
        )
        self.engraving_list[2].setPixmap(
            QPixmap(self.engraving_path[int(self.cls_idx[22])])
        )

        if self.engraving_name_list.index(self.engraving7) - 1 == int(self.cls_idx[0]):
            self.mode = "79"
        elif self.engraving_name_list.index(self.engraving7) - 1 == int(
            self.cls_idx[11]
        ):
            self.mode = "97"
        else:
            self.mode = "77"

        self.e1_active = 0
        self.e1_try = 0
        self.e2_active = 0
        self.e2_try = 0
        self.e3_active = 0
        self.e3_try = 0
        img = np.array(img)
        for i, (box1, box2, box3) in enumerate(
            zip(self.line1[1:], self.line2[1:], self.line3[1:])
        ):
            box1 = box1.astype(np.int32)
            l, t, w, h = (
                box1[0] - int(box1[2] / 2),
                box1[1] - int(box1[3] / 2),
                box1[2],
                box1[3],
            )
            box1_mean = img[t : t + h, l : l + w, 2].mean()
            if box1_mean > 90:  # normal
                self.point_list1[i].setPixmap(QPixmap("app/resource/normal.png"))
            elif box1_mean > 65:  # increase
                self.point_list1[i].setPixmap(QPixmap("app/resource/increase.png"))
                self.e1_try += 1
                self.e1_active += 1
            elif box1_mean < 35:  # fail
                self.point_list1[i].setPixmap(QPixmap("app/resource/fail.png"))
                self.e1_try += 1

            box2 = box2.astype(np.int32)
            l, t, w, h = (
                box2[0] - int(box2[2] / 2),
                box2[1] - int(box2[3] / 2),
                box2[2],
                box2[3],
            )
            box2_mean = img[t : t + h, l : l + w, 2].mean()
            if box2_mean > 90:  # normal
                self.point_list2[i].setPixmap(QPixmap("app/resource/normal.png"))
            elif box2_mean > 65:  # increase
                self.point_list2[i].setPixmap(QPixmap("app/resource/increase.png"))
                self.e2_try += 1
                self.e2_active += 1
            elif box2_mean < 35:  # fail
                self.point_list2[i].setPixmap(QPixmap("app/resource/fail.png"))
                self.e2_try += 1

            box3 = box3.astype(np.int32)
            l, t, w, h = (
                box3[0] - int(box3[2] / 2),
                box3[1] - int(box3[3] / 2),
                box3[2],
                box3[3],
            )
            box3_mean = img[t : t + h, l : l + w, 0].mean()
            if box3_mean > 65:  # normal
                self.point_list3[i].setPixmap(QPixmap("app/resource/normal.png"))
            elif box3_mean > 40:  # decrease
                self.point_list3[i].setPixmap(QPixmap("app/resource/decrease.png"))
                self.e3_try += 1
                self.e3_active += 1
            elif box3_mean < 30:  # fail
                self.point_list3[i].setPixmap(QPixmap("app/resource/fail.png"))
                self.e3_try += 1

        height, width, _ = img.shape
        print(img.shape)
        box1 = self.line1[-1].astype(np.int32)
        l, t, w, h = (
            int(box1[0] + (width * 0.0475)),
            int(box1[1] - (height * 0.0675)),
            int(width * 0.022),
            int(height * 0.021),
        )
        x = img[t : t + h, l : l + w, :]
        src_gray = cv2.cvtColor(x, cv2.COLOR_RGB2GRAY)
        _, x = cv2.threshold(src_gray, 127, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)
        _, x = cv2.threshold(x, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        y = []
        for i, p in enumerate(self.p_img_path):
            p_img = cv2.imread(p)
            src_gray = cv2.cvtColor(p_img, cv2.COLOR_BGR2GRAY)
            _, p_img = cv2.threshold(
                src_gray, 127, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU
            )
            _, p_img = cv2.threshold(
                p_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
            )
            y.append(p_img)

        max_idx = -1
        max_ccoeff = -1

        for i in range(6):
            res = cv2.matchTemplate(x, y[i], cv2.TM_CCOEFF_NORMED)

            if res.max() > max_ccoeff:
                max_idx = i
                max_ccoeff = res.max()

        self.p = max_idx
        print(self.p)
        self.select_choice()

        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.craft_ability)

    def craft_ability(self):
        img = ImageGrab.grab(
            bbox=(self.left, self.top, self.right, self.bottom), all_screens=True
        )
        img = np.array(img)

        if self.e1_try + 1 <= 10:
            box1 = self.line1[self.e1_try + 1]
            box1 = box1.astype(np.int32)
            l, t, w, h = (
                box1[0] - int(box1[2] / 2),
                box1[1] - int(box1[3] / 2),
                box1[2],
                box1[3],
            )
            box1_mean = img[t : t + h, l : l + w, 2].mean()
            if box1_mean > 90:  # normal
                pass
            elif box1_mean > 65:  # increase
                self.point_list1[self.e1_try].setPixmap(
                    QPixmap("app/resource/increase.png")
                )
                self.e1_try += 1
                self.e1_active += 1
                self.p = self.p + 1 if self.p + 1 <= 5 else self.p
            elif box1_mean < 35:  # fail
                self.point_list1[self.e1_try].setPixmap(
                    QPixmap("app/resource/fail.png")
                )
                self.e1_try += 1
                self.p = self.p - 1 if self.p - 1 >= 0 else self.p

        if self.e2_try + 1 <= 10:
            box2 = self.line2[self.e2_try + 1]
            box2 = box2.astype(np.int32)
            l, t, w, h = (
                box2[0] - int(box2[2] / 2),
                box2[1] - int(box2[3] / 2),
                box2[2],
                box2[3],
            )
            box2_mean = img[t : t + h, l : l + w, 2].mean()
            if box2_mean > 90:  # normal
                pass
            elif box2_mean > 65:  # increase
                self.point_list2[self.e2_try].setPixmap(
                    QPixmap("app/resource/increase.png")
                )
                self.e2_try += 1
                self.e2_active += 1
                self.p = self.p + 1 if self.p + 1 <= 5 else self.p
            elif box2_mean < 35:  # fail
                self.point_list2[self.e2_try].setPixmap(
                    QPixmap("app/resource/fail.png")
                )
                self.e2_try += 1
                self.p = self.p - 1 if self.p - 1 >= 0 else self.p

        if self.e3_try + 1 <= 10:
            box3 = self.line3[self.e3_try + 1]
            box3 = box3.astype(np.int32)
            l, t, w, h = (
                box3[0] - int(box3[2] / 2),
                box3[1] - int(box3[3] / 2),
                box3[2],
                box3[3],
            )
            box3_mean = img[t : t + h, l : l + w, 0].mean()
            if box3_mean > 65:  # normal
                pass
            elif box3_mean > 40:  # decrease
                self.point_list3[self.e3_try].setPixmap(
                    QPixmap("app/resource/decrease.png")
                )
                self.e3_try += 1
                self.e3_active += 1
                self.p = self.p + 1 if self.p + 1 <= 5 else self.p
            elif box3_mean < 30:  # fail
                self.point_list3[self.e3_try].setPixmap(
                    QPixmap("app/resource/fail.png")
                )
                self.e3_try += 1
                self.p = self.p - 1 if self.p - 1 >= 0 else self.p

        self.select_choice()

    def select_choice(self):
        if self.mode == "97":
            prob1 = 0
            prob2 = 0
            prob3 = 0

            if self.e1_active <= 9 and self.e1_try <= 9:
                prob1 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e1_active + 1,
                        self.e1_try + 1,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e1_active,
                        self.e1_try + 1,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e2_active <= 9 and self.e2_try <= 9:
                prob2 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active + 1,
                        self.e2_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e3_active <= 9 and self.e3_try <= 9:
                prob3 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active + 1,
                        self.e3_try + 1,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try + 1,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            choice = 0 if prob1 >= prob2 else 1 if prob2 > prob3 else 2
            print(f"97 : {choice}")
            if prob1 >= prob2:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            elif prob2 > prob3:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            else:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )

        elif self.mode == "79":
            prob1 = 0
            prob2 = 0
            prob3 = 0

            if self.e1_active <= 9 and self.e1_try <= 9:
                prob1 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e2_active,
                        self.e2_try,
                        self.e1_active + 1,
                        self.e1_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e2_active,
                        self.e2_try,
                        self.e1_active,
                        self.e1_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e2_active <= 9 and self.e2_try <= 9:
                prob2 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e2_active + 1,
                        self.e2_try + 1,
                        self.e1_active,
                        self.e1_try,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e2_active,
                        self.e2_try + 1,
                        self.e1_active,
                        self.e1_try,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e3_active <= 9 and self.e3_try <= 9:
                prob3 = (
                    self.prob[self.p]
                    * self.table_97[
                        self.e2_active,
                        self.e2_try,
                        self.e1_active,
                        self.e1_try,
                        self.e3_active + 1,
                        self.e3_try + 1,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_97[
                        self.e2_active,
                        self.e2_try,
                        self.e1_active,
                        self.e1_try,
                        self.e3_active,
                        self.e3_try + 1,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            choice = 0 if prob1 >= prob2 else 1 if prob2 > prob3 else 2
            print(f"79 : {choice}")
            if prob1 >= prob2:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            elif prob2 > prob3:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            else:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )

        elif self.mode == "77":
            prob1 = 0
            prob2 = 0
            prob3 = 0

            if self.e1_active <= 9 and self.e1_try <= 9:
                prob1 = (
                    self.prob[self.p]
                    * self.table_77[
                        self.e1_active + 1,
                        self.e1_try + 1,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_77[
                        self.e1_active,
                        self.e1_try + 1,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e2_active <= 9 and self.e2_try <= 9:
                prob2 = (
                    self.prob[self.p]
                    * self.table_77[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active + 1,
                        self.e2_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_77[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try + 1,
                        self.e3_active,
                        self.e3_try,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            if self.e3_active <= 9 and self.e3_try <= 9:
                prob3 = (
                    self.prob[self.p]
                    * self.table_77[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active + 1,
                        self.e3_try + 1,
                        self.p + 1 if self.p + 1 <= 5 else self.p,
                    ]
                ) + (
                    (1 - self.prob[self.p])
                    * self.table_77[
                        self.e1_active,
                        self.e1_try,
                        self.e2_active,
                        self.e2_try,
                        self.e3_active,
                        self.e3_try + 1,
                        self.p - 1 if self.p - 1 >= 0 else self.p,
                    ]
                )

            choice = 0 if prob1 >= prob2 else 1 if prob2 > prob3 else 2
            print(f"77 : {choice}")
            if prob1 >= prob2:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            elif prob2 > prob3:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
            else:
                self.engraving_list[0].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[1].setStyleSheet(
                    "border-radius: 25px; border: 2px solid black;"
                )
                self.engraving_list[2].setStyleSheet(
                    "border-radius: 25px; border: 4px solid lime;"
                )


app = QApplication(sys.argv)
app.setStyleSheet(Path("qss/main.qss").read_text())

window = MainWindow()
window.show()

app.exec()
