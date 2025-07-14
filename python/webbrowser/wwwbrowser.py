import sys
import os
import datetime
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, QVBoxLayout, QWidget, QDialog, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox, QLabel, QStatusBar, QProgressBar, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QDesktopServices


class BookmarkManager(QDialog):
    def __init__(self, parent=None):
        super(BookmarkManager, self).__init__(parent)
        self.setWindowTitle("Bookmarks")
        self.setGeometry(100, 100, 400, 300)
        self.setObjectName("BookmarkManager")

        self.layout = QVBoxLayout()
        self.bookmark_list = QListWidget()
        self.bookmark_list.setObjectName("BookmarkList")
        self.layout.addWidget(self.bookmark_list)

        self.button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.setObjectName("BookmarkButton")
        self.open_button.clicked.connect(self.open_bookmark)
        self.button_layout.addWidget(self.open_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("BookmarkButton")
        self.delete_button.clicked.connect(self.delete_bookmark)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.load_bookmarks()

    def load_bookmarks(self):
        self.bookmark_list.clear()
        try:
            with open("bookmarks.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|||")
                    if len(parts) == 2:
                        name, url = parts
                        item = QListWidgetItem(name)
                        item.setData(Qt.UserRole, url)
                        self.bookmark_list.addItem(item)
        except FileNotFoundError:
            pass

    def add_bookmark(self, name, url):
        existing_urls = []
        try:
            with open("bookmarks.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|||")
                    if len(parts) == 2:
                        existing_urls.append(parts[1])
        except FileNotFoundError:
            pass

        if url not in existing_urls:
            with open("bookmarks.txt", "a") as f:
                f.write(f"{name}|||{url}\n")
            self.load_bookmarks()
        else:
            QMessageBox.warning(self, "Bookmark Exists", "This URL is already bookmarked.")

    def open_bookmark(self):
        selected_item = self.bookmark_list.currentItem()
        if selected_item:
            url = selected_item.data(Qt.UserRole)
            self.parent().add_new_tab(QUrl(url), selected_item.text())
            self.accept()

    def delete_bookmark(self):
        selected_item = self.bookmark_list.currentItem()
        if selected_item:
            reply = QMessageBox.question(self, 'Delete Bookmark', 'Are you sure you want to delete this bookmark?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                url_to_delete = selected_item.data(Qt.UserRole)
                bookmarks_to_keep = []
                try:
                    with open("bookmarks.txt", "r") as f:
                        for line in f:
                            parts = line.strip().split("|||")
                            if len(parts) == 2 and parts[1] != url_to_delete:
                                bookmarks_to_keep.append(line)
                    with open("bookmarks.txt", "w") as f:
                        for bookmark_line in bookmarks_to_keep:
                            f.write(bookmark_line)
                except FileNotFoundError:
                    pass
                self.load_bookmarks()


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.setObjectName("BrowserWindow")
        self.setWindowTitle("My Advanced Browser")

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setObjectName("BrowserTabs")

        self.setCentralWidget(self.tabs)
        self.showMaximized()

        navbar = QToolBar()
        navbar.setObjectName("BrowserToolbar")
        navbar.setIconSize(QSize(24, 24))
        self.addToolBar(navbar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.url_status_label = QLabel("Ready")
        self.status_bar.addWidget(self.url_status_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        self.setup_toolbar_actions(navbar)

        # Set DuckDuckGo as default homepage
        self.add_new_tab(QUrl("https://duckduckgo.com/"), "Homepage")

        self.bookmark_manager = BookmarkManager(self)

    def setup_toolbar_actions(self, navbar):
        back_btn = QAction(QIcon.fromTheme("go-previous"), "Back", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon.fromTheme("go-next"), "Forward", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon.fromTheme("view-refresh"), "Reload", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        stop_btn = QAction(QIcon.fromTheme("process-stop"), "Stop", self)
        stop_btn.triggered.connect(lambda: self.current_browser().stop())
        navbar.addAction(stop_btn)

        home_btn = QAction(QIcon.fromTheme("go-home"), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addSeparator()

        new_tab_btn = QAction(QIcon.fromTheme("tab-new"), "New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(new_tab_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setObjectName("UrlBar")
        navbar.addWidget(self.url_bar)

        search_btn = QAction(QIcon.fromTheme("system-search"), "Search", self)
        search_btn.triggered.connect(self.perform_search)
        navbar.addAction(search_btn)

        navbar.addSeparator()

        add_bookmark_btn = QAction(QIcon.fromTheme("bookmark-new"), "Add Bookmark", self)
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(add_bookmark_btn)

        view_bookmarks_btn = QAction(QIcon.fromTheme("bookmarks-organize"), "View Bookmarks", self)
        view_bookmarks_btn.triggered.connect(self.view_bookmarks)
        navbar.addAction(view_bookmarks_btn)

        navbar.addSeparator()

        about_btn = QAction(QIcon.fromTheme("help-about"), "About", self)
        about_btn.triggered.connect(self.show_about_dialog)
        navbar.addAction(about_btn)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            # New tabs default to DuckDuckGo
            qurl = QUrl("https://duckduckgo.com/")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda q, browser=browser: self.update_url_bar_and_status(q, browser))
        browser.loadProgress.connect(lambda p, browser=browser: self.update_load_progress(p, browser))
        browser.loadFinished.connect(lambda s, browser=browser: self.handle_load_finished(s, browser))
        browser.titleChanged.connect(lambda t, browser=browser: self.update_tab_title(t, browser))
        browser.page().profile().downloadRequested.connect(self.on_download_requested)
        browser.loadStarted.connect(lambda browser=browser: self.set_status_message(f"Loading {browser.url().host()}", browser))

        self.update_url_bar_and_status(qurl, browser)
        self.update_tab_title(label, browser)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_browser(self):
        return self.tabs.currentWidget()

    def current_tab_changed(self, i):
        if self.tabs.count() > 0:
            current_browser = self.current_browser()
            qurl = current_browser.url()
            self.update_url_bar_and_status(qurl, current_browser)
            self.update_tab_title(current_browser.page().title(), current_browser)
            if current_browser.loadProgress() < 100 and not current_browser.url().isEmpty():
                 self.progress_bar.setValue(current_browser.loadProgress())
                 self.progress_bar.setVisible(True)
                 self.set_status_message(f"Loading... {current_browser.loadProgress()}%")
            else:
                 self.progress_bar.setVisible(False)
                 self.set_status_message(current_browser.url().toDisplayString())
        else:
            self.url_bar.setText("")
            self.setWindowTitle("My Advanced Browser")
            self.set_status_message("No tabs open. Open a new tab.")
            self.progress_bar.setVisible(False)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            QMessageBox.information(self, "Cannot Close Last Tab", "Cannot close the last remaining tab.")
            return
        self.tabs.removeTab(i)

    def navigate_home(self):
        # Home button navigates to DuckDuckGo
        self.current_browser().setUrl(QUrl("https://duckduckgo.com/"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            if "." in url and " " not in url:
                url = "http://" + url
            else:
                self.perform_search(url)
                return
        self.current_browser().setUrl(QUrl(url))

    def perform_search(self, query=None):
        search_query = query if query else self.url_bar.text()
        if search_query:
            # Using DuckDuckGo Search
            search_url = QUrl(f"https://duckduckgo.com/?q={search_query}")
            self.current_browser().setUrl(search_url)

    def update_url_bar_and_status(self, q, browser=None):
        if browser and browser != self.current_browser():
            return
        self.url_bar.setText(q.toDisplayString())
        self.url_bar.setCursorPosition(0)
        self.set_status_message(q.toDisplayString())

    def update_load_progress(self, progress, browser=None):
        if browser and browser != self.current_browser():
            return
        self.progress_bar.setValue(progress)
        self.progress_bar.setVisible(progress < 100)
        if progress < 100:
            self.set_status_message(f"Loading... {progress}%")

    def handle_load_finished(self, success, browser=None):
        if browser and browser != self.current_browser():
            return

        self.progress_bar.setVisible(False)

        if not success:
            self.set_status_message(f"Error loading {browser.url().toDisplayString()}", timeout=5000)
        else:
            self.set_status_message(browser.url().toDisplayString())

        self.update_tab_title(browser.page().title(), browser)

    def update_tab_title(self, title, browser=None):
        if browser and browser != self.current_browser():
            return
        index = self.tabs.indexOf(browser)
        display_title = title if title else "New Tab"
        self.tabs.setTabText(index, display_title)
        if browser == self.current_browser():
            self.setWindowTitle(f"My Advanced Browser - {display_title}")

    def set_status_message(self, message, timeout=0):
        self.status_bar.showMessage(message, timeout)

    def add_bookmark(self):
        current_url = self.current_browser().url().toString()
        if current_url and current_url != "about:blank":
            title = self.current_browser().page().title()
            text, ok = QMessageBox.getText(self, 'Add Bookmark', 'Enter a name for this bookmark:', QLineEdit.Normal, title if title else current_url)
            if ok and text:
                self.bookmark_manager.add_bookmark(text, current_url)
        else:
            QMessageBox.warning(self, "Cannot Add Bookmark", "Cannot add a bookmark for a blank or invalid page.")

    def view_bookmarks(self):
        self.bookmark_manager.load_bookmarks()
        self.bookmark_manager.exec_()

    def on_download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.url().fileName())
        if path:
            download.setPath(path)
            download.accept()
            download.finished.connect(lambda: self.download_finished(download))
            self.set_status_message(f"Downloading: {download.url().fileName()}")
        else:
            download.cancel()
            self.set_status_message("Download cancelled.")

    def download_finished(self, download):
        if download.isFinished() and download.state() == download.Completed:
            reply = QMessageBox.question(self, "Download Complete",
                                         f"'{download.url().fileName()}' downloaded to:\n{download.path()}\n\nDo you want to open it?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl.fromLocalFile(download.path()))
            self.set_status_message(f"Download complete: {download.url().fileName()}", timeout=3000)
        elif download.state() == download.Cancelled:
            self.set_status_message(f"Download cancelled: {download.url().fileName()}", timeout=3000)
        else:
            self.set_status_message(f"Download failed: {download.url().fileName()}", timeout=3000)

    def show_about_dialog(self):
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        info_text = f"""
        <html>
        <body>
            <h3>My Advanced Browser</h3>
            <p>Version: 1.0.0</p>
            <p>Developed by Connor for educational purposes.</p>
            <p>This browser uses PyQt5 and QtWebEngine.</p>
            <p><b>Current Time:</b> {current_time} MDT</p>
            <p><b>Current Date:</b> {current_date}</p>
            <p><b>System:</b> {sys.platform}</p>
        </body>
        </html>
        """
        QMessageBox.about(self, "About My Advanced Browser", info_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("My Advanced Browser")

    app.setStyleSheet("""
        QMainWindow#BrowserWindow {
            background-color: #333;
            color: #eee;
        }

        QToolBar#BrowserToolbar {
            background-color: #222;
            border: none;
            padding: 5px;
            spacing: 10px;
        }

        QToolBar QAction {
            font-size: 14px;
            color: #ccc;
            padding: 5px 10px;
        }

        QToolBar QAction:hover {
            background-color: #444;
            border-radius: 3px;
        }

        QToolBar QAction::icon {
            background-color: transparent;
        }

        QLineEdit#UrlBar {
            border: 1px solid #555;
            border-radius: 8px;
            padding: 5px 10px;
            background-color: #444;
            color: #eee;
            selection-background-color: #007bff;
            font-size: 14px;
            margin-left: 10px;
            margin-right: 10px;
        }

        QTabWidget::pane {
            border-top: 1px solid #444;
            background-color: #1e1e1e;
        }

        QTabBar::tab {
            background: #444;
            border: 1px solid #555;
            border-bottom-color: #444;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 15px;
            margin-right: 2px;
            color: #ccc;
            font-size: 13px;
        }

        QTabBar::tab:selected {
            background: #1e1e1e;
            border-bottom-color: #1e1e1e;
            color: #fff;
            font-weight: bold;
        }

        QTabBar::tab:hover:!selected {
            background: #555;
        }

        QStatusBar {
            background-color: #222;
            color: #ccc;
            border-top: 1px solid #444;
            padding: 2px;
        }

        QStatusBar QLabel {
            color: #ccc;
        }

        QProgressBar {
            border: 1px solid #555;
            border-radius: 5px;
            text-align: center;
            background-color: #444;
            color: #eee;
        }

        QProgressBar::chunk {
            background-color: #007bff;
            border-radius: 5px;
        }

        QDialog#BookmarkManager {
            background-color: #333;
            border: 1px solid #555;
            border-radius: 5px;
        }

        QListWidget#BookmarkList {
            background-color: #2a2a2a;
            border: 1px solid #444;
            border-radius: 5px;
            color: #eee;
            padding: 5px;
        }

        QListWidget::item {
            padding: 5px;
        }

        QListWidget::item:selected {
            background-color: #007bff;
            color: #fff;
        }

        QPushButton#BookmarkButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 14px;
            margin: 5px;
        }

        QPushButton#BookmarkButton:hover {
            background-color: #0056b3;
        }

        QMessageBox {
            background-color: #333;
            color: #eee;
        }

        QMessageBox QLabel {
            color: #eee;
        }

        QMessageBox QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
        }

        QMessageBox QPushButton:hover {
            background-color: #0056b3;
        }
    """)

    window = Browser()
    sys.exit(app.exec_())
