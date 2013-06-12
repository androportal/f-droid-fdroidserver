Setting up an f-droid server
============================


System requirement
------------------

#. Android SDK(assuming you have a 32bit system, download it from
   `here
   <http://dl.google.com/android/android-sdk_r22.0.1-linux.tgz>`_ )
#. Android NDK(assuming you have a 32bit system, download it from
   `here
   <http://dl.google.com/android/ndk/android-ndk-r8e-linux-x86.tar.bz2>`_)

#. Extract it to suitable location on your system. You will use these
   paths in server configuration.

#. ``ant``, ``ant-contrib``, ``maven``, ``javacc``, ``openjdk-6-jdk``,
   any one version control like ``git``.

#. An ``apache`` webserver


Cloning this repository
-----------------------

#. Clone this repo using::

     git clone https://github.com/androportal/f-droid-fdroidserver.git


Setting system's PATH
---------------------

#. Adding ``fdroid`` binary in system's ``$PATH``

   - copy the python script ``fdroid`` from this repository to your
     system's binary location like ``/usr/bin/`` ::

       sudo cp -v fdroid /usr/bin


Setting up a repository for apk's
---------------------------------

#. Assuming your webserver's `document root` is ``/var/www/``(this is
   default in case of Ubuntu), make a directory like
   ``/var/www/fdroid``.

   Type ::

     sudo mkdir -p /var/www/fdroid

   You need to provide your `sudo` password

#. Copy ``config.py`` from this repository to ``/var/www/fdroid``
   localtion ::

     sudo cp -v config.py /var/www/fdroid

   This is the modified file, the original version of this file is
   with the name ``config.sample.py``

#. Also copy ``fdroid-icon.png`` to same location
   ``/var/www/fdroid``::

     sudo cp -v fdroid-icon.png /var/www/fdroid

#. Now create three(3) more directories inside ``/var/www/fdroid``::

     sudo mkdir /var/www/fdroid/repo

     sudo mkdir /var/www/fdroid/metadata

     sudo mkdir /var/www/fdroid/tmp

   - ``repo`` will hold all the apk's
   - ``metadata`` will hold all the extra information about apk's
   - ``tmp`` will have apk cache

#. Copy all your apk file to ```/var/www/fdroid/repo`` ::

     sudo cp -v *.apk /var/www/fdroid/repo

#. Your file hirarcy under ``/var/www/fdroid`` should look something like this ::

     metadata/
     repo/
     tmp/
     config.py
     fdroid.icon.png


Modifying ``config.py`` file
============================

#. Open ``config.py`` from ``/var/www/fdroid/`` and edit it. You can
   also refer to our config file ``my-config.py``

Setting up a keystore
=====================

#. When setting up the repository, one of the first steps should be to
   generate a signing key for the repository index. This will also
   create a keystore, which is a file that can be used to hold this
   and all other keys used. Consider the location, security and backup
   status of this file carefully, then create it as follows

   - You need to create a keystore file with the same name and
     location assigned to a variable ``keystore`` in ``config.py``
     file. For example if our ``keystore`` variable is::

       keystore = "/home/john/fdroid-keystore/my.keystore"

     then, visit that location::
       
       cd /home/john/fdroid-keystore/my.keystore

     and execute the command ::

       keytool -genkey -v -keystore my.keystore -alias repokey -keyalg
       RSA -keysize 2048 -validity 10000

   - Provide same values which you have assigned to variable
     ``keydname`` in ``config.py``

   - Please say `yes` when asked for confirmation and press ENTER

   - This should generate a file ``my.keystore`` in present directory

   - Now everyting is in place, visit the location ``/var/www/fdroid``
     and execute the command ::

       sudo fdroid update -c -v

     This should show output similar to screenshot below
   
   .. image::
      https://raw.github.com/androportal/f-droid-fdroidserver/master/fdroid-keystore.png

   - Now run ::

       sudo fdroid update -v

   - and finally ::

       sudo fdroid publish

     
Configure webserver to server your repo
---------------------------------------

#. Assuming you have installed a webserver, start it using ::

     sudo service apache2 start

   assuming you are using an Ubuntu distro

#. Dont forget to give access to web user ::

     sudo chown -R www-data.www-data /var/www/fdroid

   and ::

     sudo chmod -R 755 /var/www/fdroid

#. Only give root access to ``config.py`` file ::

     sudo chown root.root /var/www/fdroid/config.py

     sudo chmod 700 /var/www/fdroid/config.py


Testing your repo
=================

#. You can test your f-droid server by visiting
   ``http://localhost/fdroid/repo`` on a web-browser

#. If you have any problem, please make sure you have followed all
   above steps correctly OR raise an issue.



   
     

