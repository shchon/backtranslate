[app]

# (str) Title of your application
title = BackTranslate

# (str) Package name
package.name = backtranslate

# (str) Package domain (needs to be unique)
package.domain = org.backtranslate

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (relative to source.dir)
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,otf

# (list) List of inclusions (pattern, regex)
# source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (pattern, regex)
# source.exclude_patterns = license,images/*.png

# (str) Application versioning
version = 0.1.0

# (str) Application requirements (Kivy + dependencies)
requirements = python3,hostpython3,kivy,requests,plyer,android,Pillow

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Orientation (one of landscape, sensorLandscape, portrait, sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 24

# (str) Android NDK version to use
# android.ndk = 25c

# (bool) Use Android's private storage for app data
android.private_storage = True

# (str) Android entry point
# android.entrypoint = main.py

# (list) Python for Android bootstrap
# bootstrap = sdl2

# (str) Log level
log_level = 2

# (bool) Accept SDK license
android.accept_sdk_license = True

# (int) Target architecture (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a

# (str) AAB vs APK (aab or apk)
android.release_artifact = apk

[buildozer]

# (int) Log level (0=error, 1=warning, 2=info, 3=debug)
log_level = 2

# (str) Path to build artifact storage
# build_dir = ./.buildozer

# (str) Path to build output (APK/AAB files)
# bin_dir = ./bin

# (str) Android SDK directory
# android.sdk_path = ~/.buildozer/android/platform/android-sdk

# (str) Android NDK directory
# android.ndk_path = ~/.buildozer/android/platform/android-ndk

# (str) Android ANT directory
# android.ant_path = ~/.buildozer/android/platform/apache-ant

# (str) Android SDK command line tools version
# android.cmdline_tools_version = 8.0

# (str) Java version (openjdk-17 or openjdk-11)
# java.version = 17