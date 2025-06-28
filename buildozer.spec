[app]

# Title of your application
title = Smart Diary

# Package name and domain
package.name = smartdiary
package.domain = org.example

# Source code directory and main file
source.dir = .
source.main = main.py

# Application version
version = 1.0

# Application requirements (you can add more like 'sqlite3', 'plyer', etc. if needed)
requirements = python3,kivy

# Application icon
icon.filename = %(source.dir)s/icon.png

# Presplash screen image
presplash.filename = %(source.dir)s/presplash.png

# Supported orientation
orientation = portrait

# Fullscreen mode
fullscreen = 1

# Permissions required by the app
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Target and minimum API levels
android.api = 33
android.minapi = 21

# NDK configuration
android.ndk = 25b
android.ndk_api = 21

# Use private storage for app data
android.private_storage = True

# Entry point for the Android app
android.entrypoint = org.kivy.android.PythonActivity

# Theme used by the Android app
android.theme = @android:style/Theme.NoTitleBar

# Enable this if you want to include compiled Python modules as shared libraries
android.copy_libs = 1

# Uncomment and edit the following line to include additional file types
#source.include_exts = py,png,jpg,kv,atlas

# Uncomment to specify files/folders to include
#source.include_patterns = assets/*,images/*.png

# Uncomment to exclude specific files/folders
#source.exclude_patterns = license,images/*/*.jpg

# Uncomment to add extra .jar or .aar files if using Java/Kotlin code
#android.add_jars = path/to/yourfile.jar
#android.add_aars = path/to/yourfile.aar

# Uncomment to include gradle dependencies if required
#android.gradle_dependencies = com.example:library:1.0.0
