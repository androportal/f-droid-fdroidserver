
#Copy this file to config.py, then amend the settings below according to
#your system configuration.

sdk_path = "/home/YOUR-USERNAME/PATH-TO-android-sdk-linux-folder"
ndk_path = "/home/YOUR-USERNAME/PATH-TO-android-ndk-r8e"

#You probably don't need to change this...
javacc_path = "/usr/bin/javacc"

#Command for running maven 3 (could be mvn, mvn3, or a full path)
mvn3 = "mvn"

repo_url = "http://localhost/fdroid/repo"
repo_name = "YOUR-REPO-NAME"
repo_icon = "fdroid-icon.png"
repo_description = """
YOUR F-DROID REPO DESCRIPTION
"""

# As above, but for the archive repo.
# archive_older sets the number of versions kept in the main repo, with all
# older ones going to the archive. Set it to 0, and there will be no archive
# repository, and no need to define the other archive_ values.
# archive_older = 3
# archive_url = "https://f-droid.org/archive"
# archive_name = "F-Droid Archive"
# archive_icon = "fdroid-icon.png"
# archive_description = """
# The archive repository of the F-Droid client. This contains older versions
# of applications from the main repository.
#"""


#The key (from the keystore defined below) to be used for signing the
#repository itself. Can be None for an unsigned repository.
repo_keyalias = "repokey"
#repo_keyalias = None

#The keystore to use for release keys when building. This needs to be
#somewhere safe and secure, and backed up!
keystore = "/home/USER-NAME/fdroid-keystore/my.keystore"

#The password for the keystore (at least 6 characters).
keystorepass = "YOUR-PASSWORD"

#The password for keys - the same is used for each auto-generated key
#as well as for the repository key.
keypass = "YOU-CAN-PUT-SAME-PASSWORD-HERE"

#The distinguished name used for all keys.
keydname = "CN=darkstar, OU=IIT, O=IIT Bombay, L=Mumbai, S=Maharashtra, C=IN"

#Use this to override the auto-generated key aliases with specific ones
#for particular applications. Normally, just leave it empty.
#keyaliases = {}
#keyaliases['com.example.app'] = 'example'
#You can also force an app to use the same key alias as another one, using
#the @ prefix.
#keyaliases['com.example.another.plugin'] = '@com.example.another'

#The ssh path to the server's public web root directory. This is used for
#uploading data, etc.
serverwebroot = 'USER-NAME@localhost:/var/www/fdroid'

#Wiki details
wiki_server = "server"
wiki_path = "/wiki/"
wiki_user = "login"
wiki_password = "1234"

#Only set this to true when running a repository where you want to generate
#stats, and only then on the master build servers, not a development
#machine.
update_stats = True

#Use the following to push stats to a Carbon instance:
# stats_to_carbon = False
# carbon_host = '0.0.0.0'
# carbon_port = 2003


#Set this to true to always use a build server. This saves specifying the
#--server option on dedicated secure build server hosts.
build_server_always = False

