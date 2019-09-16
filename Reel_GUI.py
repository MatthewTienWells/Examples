import kivy
from kivy.core.text import Label
from kivy.app import App
from kivy.core.window import Window
import reel_comparison as reels
##
##class FileBox1(FileChooser):
##    def _on_file_drop(self, window, file_path):
##        print('Got file 1')
##        self.get_running_app().file1_set(file_path)
##
##class FileBox2(FileChooser):
##    def __init__(self):
##        print('Statrt')
##        Window.bind(on_dropfile=self._on_file_drop)
##        return
##    
##    def _on_file_drop(self, window, file_path):
##        self.get_running_app().file2_set(file_path)

class Reel_GUI(App):
    def file1_set(self, file_path):
        self.file1 = file_path
        if self.file2 != None:
            self.file_compare()

    def file2_set(self, file_path):
        self.file2 = file_path
        if self.file1 != None:
            self.file_compare()

    def file_compare(self, file1, file2):
        print('Going')
        print(file1.selection)
        reel1 = reels.ReelList(reels.trim_xml(file1.selection[0]))
        reel2 = reels.ReelList(reels.trim_xml(file2.selection[0]))
        try:
            self.root.ids.output.text = reels.compare_reels(reel1, reel2)
        except ValueError:
            self.root.ids.output.text = 'Those files are not valid.'

if __name__ == '__main__':
    Reel_GUI().run()
