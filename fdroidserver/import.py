#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# import.py - part of the FDroid server tools
# Copyright (C) 2010-12, Ciaran Gultnieks, ciaran@ciarang.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import shutil
import subprocess
import re
import urllib
from optparse import OptionParser


# Get the repo type and address from the given web page. The page is scanned
# in a rather naive manner for 'git clone xxxx', 'hg clone xxxx', etc, and
# when one of these is found it's assumed that's the information we want.
# Returns repotype, address, or None, reason
def getrepofrompage(url):

    req = urllib.urlopen(url)
    if req.getcode() != 200:
        return (None, 'Unable to find source at ' + sourcecode + ' - return code ' + str(req.getcode()))
    page = req.read()

    # Works for Google Code and BitBucket...
    index = page.find('hg clone')
    if index != -1:
        repotype = 'hg'
        repo = page[index + 9:]
        index = repo.find('<')
        if index == -1:
            return (None, "Error while getting repo address")
        repo = repo[:index]
        return (repotype, repo)

    # Works for Google Code and BitBucket...
    index=page.find('git clone')
    if index != -1:
        repotype = 'git'
        repo = page[index + 10:]
        index = repo.find('<')
        if index == -1:
            return (None, "Error while getting repo address")
        repo = repo[:index]
        return (repotype, repo)

    # Google Code only...
    index=page.find('svn checkout')
    if index != -1:
        repotype = 'git-svn'
        repo = page[index + 13:]
        prefix = '<strong><em>http</em></strong>'
        if not repo.startswith(prefix):
            return (None, "Unexpected checkout instructions format")
        repo = 'http' + repo[len(prefix):]
        index = repo.find('<')
        if index == -1:
            return (None, "Error while getting repo address - no end tag? '" + repo + "'")
            sys.exit(1)
        repo = repo[:index]
        index = repo.find(' ')
        if index == -1:
            return (None, "Error while getting repo address - no space? '" + repo + "'")
        repo = repo[:index]
        return (repotype, repo)

    return (None, "No information found." + page)


def main():

    # Read configuration...
    execfile('config.py', globals())

    import common

    # Parse command line...
    parser = OptionParser()
    parser.add_option("-u", "--url", default=None,
                      help="Project URL to import from.")
    parser.add_option("-s", "--subdir", default=None,
                      help="Path to main android project subdirectory, if not in root.")
    parser.add_option("-r", "--repo", default=None,
                      help="Allows a different repo to be specified for a multi-repo google code project")
    (options, args) = parser.parse_args()

    if not options.url:
        print "Specify project url."
        sys.exit(1)
    url = options.url

    tmp_dir = 'tmp'
    if not os.path.isdir(tmp_dir):
        print "Creating temporary directory"
        os.makedirs(tmp_dir)

    # Get all apps...
    apps = common.read_metadata()

    # Figure out what kind of project it is...
    projecttype = None
    issuetracker = None
    license = None
    website = url #by default, we might override it
    if url.startswith('git://'):
        projecttype = 'git'
        repo = url
        repotype = 'git'
        sourcecode = ""
        website = ""
    if url.startswith('https://github.com'):
        if url.endswith('/'):
            url = url[:-1]
        if url.endswith('.git'):
            print "A github URL should point to the project, not the git repo"
            sys.exit(1)
        projecttype = 'github'
        repo = url + '.git'
        repotype = 'git'
        sourcecode = url
    elif url.startswith('https://gitorious.org/'):
        projecttype = 'gitorious'
        repo = 'https://git.gitorious.org/' + url[22:] + '.git'
        repotype = 'git'
        sourcecode = url
    elif url.startswith('https://bitbucket.org/'):
        if url.endswith('/'):
            url = url[:-1]
        projecttype = 'bitbucket'
        sourcecode = url + '/src'
        issuetracker = url + '/issues'
        # Figure out the repo type and adddress...
        repotype, repo = getrepofrompage(sourcecode)
        if not repotype:
            print "Unable to determine vcs type. " + repo
            sys.exit(1)
    elif url.startswith('http://code.google.com/p/'):
        if not url.endswith('/'):
            url += '/';
        projecttype = 'googlecode'
        sourcecode = url + 'source/checkout'
        if options.repo:
            sourcecode += "?repo=" + options.repo
        issuetracker = url + 'issues/list'

        # Figure out the repo type and adddress...
        repotype, repo = getrepofrompage(sourcecode)
        if not repotype:
            print "Unable to determine vcs type. " + repo
            sys.exit(1)

        # Figure out the license...
        req = urllib.urlopen(url)
        if req.getcode() != 200:
            print 'Unable to find project page at ' + sourcecode + ' - return code ' + str(req.getcode())
            sys.exit(1)
        page = req.read()
        index = page.find('Code license')
        if index == -1:
            print "Couldn't find license data"
            sys.exit(1)
        ltext = page[index:]
        lprefix = 'rel="nofollow">'
        index = ltext.find(lprefix)
        if index == -1:
            print "Couldn't find license text"
            sys.exit(1)
        ltext = ltext[index + len(lprefix):]
        index = ltext.find('<')
        if index == -1:
            print "License text not formatted as expected"
            sys.exit(1)
        ltext = ltext[:index]
        if ltext == 'GNU GPL v3':
            license = 'GPLv3'
        elif ltext == 'GNU GPL v2':
            license = 'GPLv2'
        elif ltext == 'Apache License 2.0':
            license = 'Apache2'
        elif ltext == 'MIT License':
            license = 'MIT'
        elif ltext == 'GNU Lesser GPL':
            license = 'LGPL'
        elif ltext == 'Mozilla Public License 1.1':
            license = 'MPL'
        elif ltext == 'New BSD License':
            license = 'NewBSD'
        else:
            print "License " + ltext + " is not recognised"
            sys.exit(1)

    if not projecttype:
        print "Unable to determine the project type."
        print "The URL you supplied was not in one of the supported formats. Please consult"
        print "the manual for a list of supported formats, and supply one of those."
        sys.exit(1)

    # Get a copy of the source so we can extract some info...
    print 'Getting source from ' + repotype + ' repo at ' + repo
    src_dir = os.path.join(tmp_dir, 'importer')
    if os.path.exists(src_dir):
        shutil.rmtree(src_dir)
    vcs = common.getvcs(repotype, repo, src_dir, sdk_path)
    vcs.gotorevision(None)
    if options.subdir:
        root_dir = os.path.join(src_dir, options.subdir)
    else:
        root_dir = src_dir

    # Check AndroidManiifest.xml exists...
    if not os.path.exists(root_dir + '/AndroidManifest.xml'):
        print "AndroidManifest.xml did not exist in the expected location. Specify --subdir?"
        sys.exit(1)

    # Extract some information...
    version, vercode, package = common.parse_androidmanifest(root_dir)
    if not package:
        print "Couldn't find package ID"
        sys.exit(1)
    if not version:
        print "Couldn't find latest version name"
        sys.exit(1)
    if not vercode:
        print "Couldn't find latest version code"
        sys.exit(1)

    # Make sure it's actually new...
    for app in apps:
        if app['id'] == package:
            print "Package " + package + " already exists"
            sys.exit(1)

    # Construct the metadata...
    app = common.parse_metadata(None)
    app['id'] = package
    app['Web Site'] = website
    app['Source Code'] = sourcecode
    if issuetracker:
        app['Issue Tracker'] = issuetracker
    if license:
        app['License'] = license
    app['Repo Type'] = repotype
    app['Repo'] = repo

    # Create a build line...
    build = {}
    build['version'] = version
    build['vercode'] = vercode
    build['commit'] = '?'
    if options.subdir:
        build['subdir'] = options.subdir
    if os.path.exists(os.path.join(root_dir, 'jni')):
        build['buildjni'] = 'yes'
    app['builds'].append(build)
    app['comments'].append(('build:' + version,
        "#Generated by import.py - check this is the right version, and find the right commit!"))

    # Keep the repo directory to save bandwidth...
    if not os.path.exists('build'):
        os.mkdir('build')
    shutil.move(src_dir, os.path.join('build', package))

    metafile = os.path.join('metadata', package + '.txt')
    common.write_metadata(metafile, app)
    print "Wrote " + metafile


if __name__ == "__main__":
    main()

