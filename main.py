import os
import subprocess
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
from PyQt6.QtGui import QPixmap
from art import text2art


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YounesWinterLabs (https://youneswinter.pro)')
        self.setGeometry(0, 0, 600, 400)
        self.setStyleSheet('background-color: #000;')

        layout = QVBoxLayout()
        layout.setSpacing(0)  # Set spacing to zero

        header_title = QLabel('WiFi Password Extractor', self)
        header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_title.setStyleSheet('color: #fff; font-size: 24px;')
        layout.addWidget(header_title)

        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            pixmap = QPixmap(os.path.join(base_path, 'logo.png'))
            logo = QLabel(self)
            logo.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo)
        except Exception as e:
            print(f"Error loading logo: {e}")

        text_label = QLabel('Press the Extract button below to get all the WiFi passwords stored in your device.', self)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet('color: #fff; font-weight: bold;')
        layout.addWidget(text_label)

        extract_button = QPushButton('Extract', self)
        extract_button.setStyleSheet('background-color: #006233; color: #ffffff;')
        extract_button.clicked.connect(self.extract_passwords)
        layout.addWidget(extract_button)

        self.setLayout(layout)

    def extract_passwords(self):

        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            # Retrieve Wi-Fi profile information
            wifi_data = subprocess.check_output(["netsh", "wlan", "show", "profiles"], creationflags=creation_flags).decode("utf-8").split("\n")
    
            # Extract SSIDs
            ssids = [i.split(":")[1][1:-1] for i in wifi_data if "All User" in i]
    
            # Initialize a dictionary to store SSID and password pairs
            wifi_credentials = {}
    
            # Retrieve passwords for each SSID
            for ssid in ssids:
                show_pass = subprocess.check_output(["netsh", "wlan", "show", "profile", ssid, "key=clear"], creationflags=creation_flags).decode(
                    "utf-8").split("\n")
                password = [b.split(":")[1][1:-1] for b in show_pass if "Key Content" in b]
                # Store in the dictionary
                wifi_credentials[ssid] = password[0] if password else ""
    
            executable_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    
            # Define the output file path relative to the executable
            output_file_path = os.path.join(executable_dir, 'wifi_passwords.txt')
    
            # Open a text file to write the SSID and password pairs
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write("{:<30} | {:<}\n".format("SSID", "Password"))
                file.write("-" * 50 + "\n")
                for ssid, password in wifi_credentials.items():
                    file.write("{:<30} | {:<}\n".format(ssid, password))
    
                # Add the signature in ASCII art font
                signature = text2art("Made By Younes Winter", "happy")  # You can choose different fonts and art styles
                file.write(f"\n\n{signature}")
    
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText('WiFi passwords have been saved successfully.')
            msg_box.setWindowTitle('Success')
            msg_box.exec()
        except UnicodeDecodeError as e:
            print(f"Error decoding UTF-8 data: {e}")
            # Handle the decoding error by skipping or replacing the problematic byte
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle other exceptions here
            pass

    def show(self):
        frameGm = self.frameGeometry()
        screen = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())
        super().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
