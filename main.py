from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from datetime import datetime
import json
import os

# Set window size for desktop testing (remove or adjust for mobile)
Window.size = (360, 640)

DATA_DIR = "data"
ENTRY_FILE = os.path.join(DATA_DIR, "entries.json")
PASSWORD_FILE = os.path.join(DATA_DIR, "password.json")
EXPORT_FILE = os.path.join(DATA_DIR, "diary_export.txt")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(ENTRY_FILE):
    with open(ENTRY_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump({"password": "diary123"}, f)

def load_entries():
    try:
        with open(ENTRY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_entries(entries):
    with open(ENTRY_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

def load_password():
    try:
        with open(PASSWORD_FILE, 'r') as f:
            data = json.load(f)
            return data.get("password", "diary123")
    except:
        return "diary123"

def save_password(new_password):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump({"password": new_password}, f, indent=2)

class ThemeManager:
    light_bg = get_color_from_hex("#f0f0f5")
    light_fg = get_color_from_hex("#000000")
    dark_bg = get_color_from_hex("#2f2f2f")
    dark_fg = get_color_from_hex("#ffffff")

class PasswordScreen(Screen):
    password_input = ObjectProperty(None)

    def verify_password(self):
        entered = self.password_input.text
        if entered == load_password():
            self.password_input.text = ""
            self.manager.current = "main"
        else:
            self.show_popup("Error", "Incorrect password!")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

class BaseScreen(Screen):
    def add_back_button(self):
        back_btn = Button(text="Back", size_hint=(None, None), size=(100, 40), pos_hint={"top": 1, "right": 1})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.add_widget(back_btn)

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

class MainScreen(Screen):
    mood_spinner = ObjectProperty(None)
    note_input = ObjectProperty(None)
    word_count_label = ObjectProperty(None)
    theme_spinner = ObjectProperty(None)

    def on_pre_enter(self):
        self.update_word_count()

    def update_word_count(self):
        text = self.note_input.text.strip()
        words = len(text.split()) if text else 0
        self.word_count_label.text = f"Word Count: {words}"

    def save_entry(self):
        mood = self.mood_spinner.text
        note = self.note_input.text.strip()
        if mood == "Select" or not note:
            self.show_popup("Warning", "Please select a mood and write something.")
            return
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {"date": date, "mood": mood, "note": note}
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)
        self.note_input.text = ""
        self.mood_spinner.text = "Select"
        self.update_word_count()
        self.show_popup("Success", "Your entry has been saved.")

    def go_to_view(self):
        self.manager.get_screen("view").load_entries()
        self.manager.current = "view"

    def go_to_edit(self):
        self.manager.get_screen("edit").load_entries()
        self.manager.current = "edit"

    def go_to_delete(self):
        self.manager.get_screen("delete").load_entries()
        self.manager.current = "delete"

    def go_to_search(self):
        self.manager.get_screen("search").reset_search()
        self.manager.current = "search"

    def go_to_stats(self):
        self.manager.get_screen("stats").load_stats()
        self.manager.current = "stats"

    def go_to_import(self):
        self.manager.current = "import"

    def go_to_export(self):
        entries = load_entries()
        try:
            with open(EXPORT_FILE, 'w') as f:
                for entry in entries:
                    f.write(f"Date: {entry['date']}\nMood: {entry['mood']}\nNote: {entry['note']}\n{'-'*40}\n")
            self.show_popup("Success", f"Entries exported to {EXPORT_FILE}")
        except:
            self.show_popup("Error", "Failed to export entries.")

    def go_to_change_password(self):
        self.manager.current = "change_password"

    def go_to_help(self):
        self.manager.current = "help"

    def go_to_feedback(self):
        self.manager.current = "feedback"

    def go_to_creator_info(self):
        self.manager.current = "creator_info"

class ViewScreen(BaseScreen):
    scroll_layout = ObjectProperty(None)

    def on_pre_enter(self):
        self.load_entries()
        self.add_back_button()

    def load_entries(self):
        self.scroll_layout.clear_widgets()
        entries = load_entries()
        if not entries:
            self.scroll_layout.add_widget(Label(text="No entries found."))
            return
        for entry in entries:
            text = f"Date: {entry['date']}\nMood: {entry['mood']}\nNote: {entry['note']}\n{'-'*40}"
            self.scroll_layout.add_widget(Label(text=text, size_hint_y=None, height=120))

class EditScreen(BaseScreen):
    entry_spinner = ObjectProperty(None)
    mood_spinner = ObjectProperty(None)
    note_input = ObjectProperty(None)

    def on_pre_enter(self):
        self.load_entries()
        self.add_back_button()

    def load_entries(self):
        self.entries = load_entries()
        self.entry_spinner.values = [f"{e['date']} - {e['mood']}" for e in self.entries]
        self.entry_spinner.text = "Select Entry"
        self.mood_spinner.text = "Select"
        self.note_input.text = ""

    def on_entry_select(self, text):
        for e in self.entries:
            label = f"{e['date']} - {e['mood']}"
            if label == text:
                self.mood_spinner.text = e['mood']
                self.note_input.text = e['note']
                break

    def save_edit(self):
        selected = self.entry_spinner.text
        if selected == "Select Entry":
            self.show_popup("Warning", "Please select an entry.")
            return
        index = self.entry_spinner.values.index(selected)
        self.entries[index]['mood'] = self.mood_spinner.text
        self.entries[index]['note'] = self.note_input.text.strip()
        save_entries(self.entries)
        self.show_popup("Success", "Entry updated.")
        self.load_entries()

class DeleteScreen(BaseScreen):
    entry_spinner = ObjectProperty(None)

    def on_pre_enter(self):
        self.load_entries()
        self.add_back_button()

    def load_entries(self):
        self.entries = load_entries()
        self.entry_spinner.values = [f"{e['date']} - {e['mood']}" for e in self.entries]
        self.entry_spinner.text = "Select Entry"

    def delete_entry(self):
        selected = self.entry_spinner.text
        if selected == "Select Entry":
            self.show_popup("Warning", "Please select an entry.")
            return
        index = self.entry_spinner.values.index(selected)
        self.entries.pop(index)
        save_entries(self.entries)
        self.show_popup("Success", "Entry deleted.")
        self.load_entries()

class SearchScreen(BaseScreen):
    search_input = ObjectProperty(None)
    scroll_layout = ObjectProperty(None)

    def on_pre_enter(self):
        self.reset_search()
        self.add_back_button()

    def reset_search(self):
        self.search_input.text = ""
        self.scroll_layout.clear_widgets()

    def perform_search(self):
        keyword = self.search_input.text.strip().lower()
        self.scroll_layout.clear_widgets()
        if not keyword:
            self.show_popup("Warning", "Please enter a keyword.")
            return
        entries = load_entries()
        found = False
        for entry in entries:
            if (keyword in entry['note'].lower() or
                keyword in entry['mood'].lower() or
                keyword in entry['date']):
                text = f"Date: {entry['date']}\nMood: {entry['mood']}\nNote: {entry['note']}\n{'-'*40}"
                self.scroll_layout.add_widget(Label(text=text, size_hint_y=None, height=120))
                found = True
        if not found:
            self.show_popup("Info", "No entries found.")

class StatsScreen(BaseScreen):
    stats_label = ObjectProperty(None)

    def on_pre_enter(self):
        self.load_stats()
        self.add_back_button()

    def load_stats(self):
        entries = load_entries()
        mood_count = {"Happy": 0, "Sad": 0, "Angry": 0, "Calm": 0}
        for entry in entries:
            mood = entry['mood'].strip()
            if mood in mood_count:
                mood_count[mood] += 1
        total = len(entries)
        stats_text = f"Total Entries: {total}\n\nMood Breakdown:\n"
        for mood, count in mood_count.items():
            stats_text += f"{mood}: {count}\n"
        self.stats_label.text = stats_text

class ImportScreen(BaseScreen):
    file_path_input = ObjectProperty(None)

    def on_pre_enter(self):
        self.file_path_input.text = ""
        self.add_back_button()

    def import_entries(self):
        path = self.file_path_input.text.strip()
        if not os.path.exists(path):
            self.show_popup("Error", "File not found.")
            return
        try:
            with open(path, 'r') as f:
                new_data = json.load(f)
            entries = load_entries()
            entries.extend(new_data)
            save_entries(entries)
            self.show_popup("Success", "Entries imported successfully.")
            self.file_path_input.text = ""
        except:
            self.show_popup("Error", "Invalid JSON file.")

class ChangePasswordScreen(BaseScreen):
    old_password_input = ObjectProperty(None)
    new_password_input = ObjectProperty(None)

    def on_pre_enter(self):
        self.old_password_input.text = ""
        self.new_password_input.text = ""
        self.add_back_button()

    def change_password(self):
        old_pwd = self.old_password_input.text
        new_pwd = self.new_password_input.text
        current_password = load_password()
        if old_pwd != current_password:
            self.show_popup("Error", "Incorrect old password.")
            return
        if not new_pwd:
            self.show_popup("Warning", "New password cannot be empty.")
            return
        save_password(new_pwd)
        self.show_popup("Success", "Password changed successfully.")
        self.old_password_input.text = ""
        self.new_password_input.text = ""

class HelpScreen(BaseScreen):
    help_text = StringProperty("""
=== Help Guide ===

1. Save Entry:
   - Use: Save your current note with a mood.
   - How: Select a mood from the dropdown, type your note, click 'Save Entry'.
   - Result: Note is saved with timestamp and mood.

2. Edit Entry:
   - Use: Modify an existing entry.
   - How: Click 'Edit Entry', select an entry, update mood/note, click 'Save Edit'.
   - Result: Selected entry is updated.

3. Export Entries:
   - Use: Export all entries to a file.
   - How: Click 'Export Entries' to save as 'diary_export.txt'.
   - Result: File is created in the data folder.

4. View Stats:
   - Use: See entry statistics.
   - How: Click 'View Stats' for a summary.
   - Result: Shows total entries and mood breakdown.

5. View Entries:
   - Use: Display all saved entries.
   - How: Click 'View Entries' to see all notes.
   - Result: Lists all entries in a scrollable window.

6. Delete Entry:
   - Use: Remove an entry.
   - How: Click 'Delete Entry', select an entry, confirm deletion.
   - Result: Entry is removed.

7. Search Entries:
   - Use: Find entries by keyword.
   - How: Click 'Search Entries', enter a keyword, click 'Search'.
   - Result: Shows matching entries.

8. Import Entries:
   - Use: Import entries from a JSON file.
   - How: Click 'Import Entries', enter file path, confirm.
   - Result: Entries are added to the data.
""")

    def on_pre_enter(self):
        self.add_back_button()

class FeedbackScreen(BaseScreen):
    feedback_input = ObjectProperty(None)
    info_label = ObjectProperty(None)

    def on_pre_enter(self):
        self.feedback_input.text = ""
        self.info_label.text = ""
        self.add_back_button()

    def submit_feedback(self):
        feedback = self.feedback_input.text.strip()
        if not feedback:
            self.show_popup("Warning", "Please enter feedback.")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        feedback_file = os.path.join(DATA_DIR, f"feedback_{timestamp}.txt")
        try:
            with open(feedback_file, 'w') as f:
                f.write(f"Feedback at {timestamp}:\n{feedback}")
            self.show_popup("Success", "Feedback saved locally in data folder.")
            self.feedback_input.text = ""
        except:
            self.show_popup("Error", "Failed to save feedback.")

class CreatorInfoScreen(BaseScreen):
    info_text = StringProperty("""
======================================================================
                       ~ About the Creator ~
======================================================================

:) • Name: Aryan Sharma
•Created: June 2025
•Version: 1.0 - The Dawn of Smart Diary
~ Contact: setgamerz0090@gmail.com

@About Me:
I am a passionate coder dedicated to building tools that inspire. 
Smart Diary is my effort to help you organize thoughts with style.

∆ Key Features:
- Real-time word count.
- Mood-based entry tracking.
- Password protection.
- Export/import options.

@ Design Vision:
Modern look with light/dark themes for comfort.

+Future Plans:
- Image support.
- Cloud backup.
- Visual charts.

✓ Thanks:
Your feedback drives this app's growth. Contact me anytime!

======================================================================
""")

    def on_pre_enter(self):
        self.add_back_button()

class DiaryApp(App):
    def build(self):
        self.title = "Smart Diary"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(PasswordScreen(name="password"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ViewScreen(name="view"))
        sm.add_widget(EditScreen(name="edit"))
        sm.add_widget(DeleteScreen(name="delete"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(ImportScreen(name="import"))
        sm.add_widget(ChangePasswordScreen(name="change_password"))
        sm.add_widget(HelpScreen(name="help"))
        sm.add_widget(FeedbackScreen(name="feedback"))
        sm.add_widget(CreatorInfoScreen(name="creator_info"))
        return sm

if __name__ == "__main__":
    DiaryApp().run()
