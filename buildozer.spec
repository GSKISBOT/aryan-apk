[app]

# (str) Title of your application
title = Smart Diary

# (str) Package name
package.name = smartdiary

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (str) Application entry point, default is main.py
source.main = main.py

# (list) Application requirements
requirements = python3,kivy

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 24

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is 'import android' (crashes without)
android.theme = '@android:style/Theme.NoTitleBar'

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Custom source folders for requirements
#android.custom_source_dirs =

# (list) List of Java .jar files to add to the libs so that pyjnius can access them
#android.add_jars =

# (list) List of Java .aar files to add to the libs so that pyjnius can access them
#android.add_aars =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (list) Java classes to add as activities to the manifest.
#android.add_activities =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (bool) Use the new android toolchain (default False)
#android.new_toolchain = 1

# (list) List of service to declare
#services =

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.code =

# (str) Application versioning (method 3)
# version.git_commit =

# (list) Application requirements
#requirements = python3,kivy

# (str) Custom source folders for requirements
#source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application entry point, default is main.py
#source.main = main.py

# (str) Application icon
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (portrait, landscape or all)
#orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
#fullscreen = 1

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (list) Permissions
#android.permissions = INTERNET

# (int) Target API
#android.api = 33

# (int) Minimum API your APK will support
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 24

# (str) Android NDK version to use
#android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android entry point, default is ok
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is 'import android' (crashes without)
#android.theme = '@android:style/Theme.NoTitleBar'
