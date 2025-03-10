# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2010 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an abstract base class to be subclassed by all specific 
VCS interfaces.
"""

import os

from PyQt4.QtCore import QObject, QThread, QMutex, QProcess, \
    QString, QStringList, SIGNAL, Qt
from PyQt4.QtGui import QApplication

from KdeQt import KQMessageBox

import Preferences

class VersionControl(QObject):
    """
    Class implementing an abstract base class to be subclassed by all specific 
    VCS interfaces.
    
    It defines the vcs interface to be implemented by subclasses
    and the common methods.
    
    @signal vcsStatusMonitorData(QStringList) emitted to update the VCS status
    @signal vcsStatusMonitorStatus(QString, QString) emitted to signal the status of the
        monitoring thread (ok, nok, op, off) and a status message
    """
    
    canBeCommitted = 1  # Indicates that a file/directory is in the vcs.
    canBeAdded = 2      # Indicates that a file/directory is not in vcs.
    
    def __init__(self, parent=None, name=None):
        """
        Constructor
        
        @param parent parent widget (QWidget)
        @param name name of this object (string or QString)
        """
        QObject.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.defaultOptions = {
            'global' : [''],
            'commit' : [''],
            'checkout' : [''],
            'update' : [''],
            'add' : [''],
            'remove' : [''],
            'diff' : [''],
            'log' : [''],
            'history' : [''],
            'status' : [''],
            'tag' : [''],
            'export' : ['']
        }
        self.interestingDataKeys = []
        self.options = {}
        self.otherData = {}
        self.canDetectBinaries = True
        self.autoCommit = False
        
        self.statusMonitorThread = None
        self.vcsExecutionMutex = QMutex()
        
    def vcsShutdown(self):
        """
        Public method used to shutdown the vcs interface.
        """
        raise RuntimeError('Not implemented')
        
    def vcsExists(self):
        """
        Public method used to test for the presence of the vcs.
        
        It must return a bool to indicate the existance and a QString giving
        an error message in case of failure.
        
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsInit(self, vcsDir, noDialog = False):
        """
        Public method used to initialize the vcs.
        
        It must return a boolean to indicate an execution without errors.
        
        @param vcsDir name of the VCS directory (string)
        @param noDialog flag indicating quiet operations (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsConvertProject(self, vcsDataDict, project):
        """
        Public method to convert an uncontrolled project to a version controlled project.
        
        @param vcsDataDict dictionary of data required for the conversion
        @param project reference to the project object
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsImport(self, vcsDataDict, projectDir, noDialog = False):
        """
        Public method used to import the project into the vcs.
        
        @param vcsDataDict dictionary of data required for the import
        @param projectDir project directory (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating an execution without errors (boolean)
            and a flag indicating the version controll status (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsCheckout(self, vcsDataDict, projectDir, noDialog = False):
        """
        Public method used to check the project out of the vcs.
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating an execution without errors (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsExport(self, vcsDataDict, projectDir):
        """
        Public method used to export a directory from the vcs.
        
        It must return a boolean to indicate an execution without errors.
        
        @param vcsDataDict dictionary of data required for the export
        @param projectDir project directory to create (string)
        @return flag indicating an execution without errors (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsCommit(self, name, message, noDialog = False):
        """
        Public method used to make the change of a file/directory permanent in the vcs.
        
        It must return a boolean to indicate an execution without errors.
        
        @param name file/directory name to be committed (string)
        @param message message for this operation (string)
        @param noDialog flag indicating quiet operations
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsUpdate(self, name, noDialog = False):
        """
        Public method used to update a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to be updated (string)
        @param noDialog flag indicating quiet operations (boolean)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsAdd(self, name, isDir = False, noDialog = False):
        """
        Public method used to add a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @param noDialog flag indicating quiet operations (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsAddBinary(self, name, isDir = False):
        """
        Public method used to add a file/directory in binary mode in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsAddTree(self, path):
        """
        Public method to add a directory tree rooted at path in the vcs.
        
        It must not return anything.
        
        @param path root directory of the tree to be added (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsRemove(self, name, project = False, noDialog = False):
        """
        Public method used to add a file/directory in the vcs.
        
        It must return a flag indicating successfull operation
        
        @param name file/directory name to be removed (string)
        @param project flag indicating deletion of a project tree (boolean)
        @param noDialog flag indicating quiet operations
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsMove(self, name, project, target = None, noDialog = False):
        """
        Public method used to move a file/directory.
        
        @param name file/directory name to be moved (string)
        @param project reference to the project object
        @param target new name of the file/directory (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating successfull operation (boolean)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsLog(self, name):
        """
        Public method used to view the log of a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to show the log for (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsDiff(self, name):
        """
        Public method used to view the diff of a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to be diffed (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsHistory(self, name):
        """
        Public method used to view the history of a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to show the history for (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsStatus(self, name):
        """
        Public method used to view the status of a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to show the status for (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsTag(self, name):
        """
        Public method used to set the tag of a file/directory in the vcs.
        
        It must not return anything.
        
        @param name file/directory name to be tagged (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsRevert(self, name):
        """
        Public method used to revert changes made to a file/directory.
        
        It must not return anything.
        
        @param name file/directory name to be reverted (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsSwitch(self, name):
        """
        Public method used to switch a directory to a different tag/branch.
        
        It must not return anything.
        
        @param name directory name to be switched (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsMerge(self, name):
        """
        Public method used to merge a tag/branch into the local project.
        
        It must not return anything.
        
        @param name file/directory name to be merged (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsRegisteredState(self, name):
        """
        Public method used to get the registered state of a file in the vcs.
        
        @param name filename to check (string)
        @return a combination of canBeCommited and canBeAdded or
            0 in order to signal an error
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsAllRegisteredStates(self, names, dname):
        """
        Public method used to get the registered states of a number of files in the vcs.
        
        @param names dictionary with all filenames to be checked as keys
        @param dname directory to check in (string)
        @return the received dictionary completed with a combination of 
            canBeCommited and canBeAdded or None in order to signal an error
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsName(self):
        """
        Public method returning the name of the vcs.
        
        @return name of the vcs (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsCleanup(self, name):
        """
        Public method used to cleanup the local copy.
        
        @param name directory name to be cleaned up (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsCommandLine(self, name):
        """
        Public method used to execute arbitrary vcs commands.
        
        @param name directory name of the working directory (string)
        @exception RuntimeError not implemented
        """
        raise RuntimeError('Not implemented')
        
    def vcsOptionsDialog(self, project, archive, editable = False, parent = None):
        """
        Public method to get a dialog to enter repository info.
        
        @param project reference to the project object
        @param archive name of the project in the repository (string)
        @param editable flag indicating that the project name is editable (boolean)
        @param parent parent widget (QWidget)
        """
        raise RuntimeError('Not implemented')
        
    def vcsNewProjectOptionsDialog(self, parent = None):
        """
        Public method to get a dialog to enter repository info for getting a new project.
        
        @param parent parent widget (QWidget)
        """
        raise RuntimeError('Not implemented')
        
    def vcsRepositoryInfos(self, ppath):
        """
        Public method to retrieve information about the repository.
        
        @param ppath local path to get the repository infos (string)
        @return string with ready formated info for display (QString)
        """
        raise RuntimeError('Not implemented')
        
    def vcsGetProjectBrowserHelper(self, browser, project, isTranslationsBrowser = False):
        """
        Public method to instanciate a helper object for the different project browsers.
        
        @param browser reference to the project browser object
        @param project reference to the project object
        @param isTranslationsBrowser flag indicating, the helper is requested for the
            translations browser (this needs some special treatment)
        @return the project browser helper object
        """
        raise RuntimeError('Not implemented')
        
    def vcsGetProjectHelper(self, project):
        """
        Public method to instanciate a helper object for the project.
        
        @param project reference to the project object
        @return the project helper object
        """
        raise RuntimeError('Not implemented')
    
    #####################################################################
    ## methods above need to be implemented by a subclass
    #####################################################################
    
    def clearStatusCache(self):
        """
        Public method to clear the status cache.
        """
        pass
        
    def vcsDefaultOptions(self):
        """
        Public method used to retrieve the default options for the vcs.
        
        @return a dictionary with the vcs operations as key and
            the respective options as values. The key 'global' must contain
            the global options. The other keys must be 'commit', 'update',
            'add', 'remove', 'diff', 'log', 'history', 'tag', 'status' and 'export'.
        """
        return self.defaultOptions
        
    def vcsSetOptions(self, options):
        """
        Public method used to set the options for the vcs.
        
        @param options a dictionary of option strings with keys as
                defined by the default options
        """
        for key in options.keys():
            try:
                self.options[key] = options[key]
            except KeyError:
                pass
        
    def vcsGetOptions(self):
        """
        Public method used to retrieve the options of the vcs.
        
        @return a dictionary of option strings that can be passed to
            vcsSetOptions.
        """
        return self.options
        
    def vcsSetOtherData(self, data):
        """
        Public method used to set vcs specific data.
        
        @param data a dictionary of vcs specific data
        """
        for key in data.keys():
            try:
                self.otherData[key] = data[key]
            except KeyError:
                pass
        
    def vcsGetOtherData(self):
        """
        Public method used to retrieve vcs specific data.
        
        @return a dictionary of vcs specific data
        """
        return self.otherData
        
    def vcsSetData(self, key, value):
        """
        Public method used to set an entry in the otherData dictionary.
        
        @param key the key of the data (string)
        @param value the value of the data
        """
        if key in self.interestingDataKeys:
            self.otherData[key] = value
        
    def vcsSetDataFromDict(self, dict):
        """
        Public method used to set entries in the otherData dictionary.
        
        @param dict dictionary to pick entries from
        """
        for key in self.interestingDataKeys:
            if dict.has_key(key):
                self.otherData[key] = dict[key]
        
    #####################################################################
    ## below are some utility methods
    #####################################################################
    
    def startSynchronizedProcess(self, proc, program, arguments, workingDir = None):
        """
        Public method to start a synchroneous process
        
        This method starts a process and waits
        for its end while still serving the Qt event loop.
        
        @param proc process to start (QProcess)
        @param program path of the executable to start (string or QString)
        @param arguments list of arguments for the process (QStringList)
        @param workingDir working directory for the process (string or QString)
        @return flag indicating normal exit (boolean)
        """
        if proc is None:
            return
            
        if workingDir:
            proc.setWorkingDirectory(workingDir)
        proc.start(program, arguments)
        procStarted = proc.waitForStarted()
        if not procStarted:
            KQMessageBox.critical(None,
                self.trUtf8('Process Generation Error'),
                self.trUtf8(
                    'The process %1 could not be started. '
                    'Ensure, that it is in the search path.'
                ).arg(program))
            return False
        else:
            while proc.state() == QProcess.Running:
                QApplication.processEvents()
                QThread.msleep(300)
                QApplication.processEvents()
            return (proc.exitStatus() == QProcess.NormalExit) and (proc.exitCode() == 0)
        
    def splitPath(self, name):
        """
        Public method splitting name into a directory part and a file part.
        
        @param name path name (string)
        @return a tuple of 2 strings (dirname, filename).
        """
        fi = unicode(name)
        if os.path.isdir(fi):
            dn = os.path.abspath(fi)
            fn = "."
        else:
            dn, fn = os.path.split(fi)
        return (dn, fn)
    
    def splitPathList(self, names):
        """
        Public method splitting the list of names into a common directory part and 
        a file list.
        
        @param names list of paths (list of strings)
        @return a tuple of string and list of strings (dirname, filenamelist)
        """
        li = [unicode(n) for n in names]
        dname = os.path.commonprefix(li)
        if dname:
            if not dname.endswith(os.sep):
                dname = os.path.dirname(dname) + os.sep
            fnames = [n.replace(dname, '') for n in li]
            dname = os.path.dirname(dname)
            return (dname, fnames)
        else:
            return ("/", li)

    def addArguments(self, args, argslist):
        """
        Protected method to add an argument list to the already present arguments.
        
        @param args current arguments list (QStringList)
        @param argslist list of arguments (list of strings or list of QStrings or
            a QStringList)
        """
        for arg in argslist:
            if unicode(arg) != '':
                args.append(arg)
    
    ############################################################################
    ## VCS status monitor thread related methods
    ############################################################################
    
    def __statusMonitorStatus(self, status, statusMsg):
        """
        Private method to receive the status monitor status.
        
        It simply reemits the received status.
        
        @param status status of the monitoring thread (QString, ok, nok or off)
        @param statusMsg explanotory text for the signaled status (QString)
        """
        self.emit(SIGNAL("vcsStatusMonitorStatus(QString, QString)"), status, statusMsg)
        QApplication.flush()

    def __statusMonitorData(self, statusList):
        """
        Private method to receive the status monitor status.
        
        It simply reemits the received status list.
        
        @param statusList list of status records (QStringList)
        """
        self.emit(SIGNAL("vcsStatusMonitorData(QStringList)"), statusList)
        QApplication.flush()

    def startStatusMonitor(self, project):
        """
        Public method to start the VCS status monitor thread.
        
        @param project reference to the project object
        @return reference to the monitor thread (QThread)
        """
        if project.pudata["VCSSTATUSMONITORINTERVAL"]:
            vcsStatusMonitorInterval = project.pudata["VCSSTATUSMONITORINTERVAL"][0]
        else:
            vcsStatusMonitorInterval = Preferences.getVCS("StatusMonitorInterval")
        if vcsStatusMonitorInterval > 0:
            self.statusMonitorThread = \
                self._createStatusMonitorThread(vcsStatusMonitorInterval, project)
            if self.statusMonitorThread is not None:
                self.connect(self.statusMonitorThread, 
                             SIGNAL("vcsStatusMonitorData(QStringList)"),
                             self.__statusMonitorData, Qt.QueuedConnection)
                self.connect(self.statusMonitorThread, 
                             SIGNAL("vcsStatusMonitorStatus(QString, QString)"),
                             self.__statusMonitorStatus, Qt.QueuedConnection)
                self.statusMonitorThread.setAutoUpdate(
                    Preferences.getVCS("AutoUpdate"))
                self.statusMonitorThread.start()
        else:
            self.statusMonitorThread = None
        return self.statusMonitorThread
    
    def stopStatusMonitor(self):
        """
        Public method to stop the VCS status monitor thread.
        """
        if self.statusMonitorThread is not None:
            self.__statusMonitorData(QStringList("--RESET--"))
            self.disconnect(self.statusMonitorThread, 
                SIGNAL("vcsStatusMonitorData(QStringList)"),
                self.__statusMonitorData)
            self.disconnect(self.statusMonitorThread, 
                SIGNAL("vcsStatusMonitorStatus(QString, QString)"),
                self.__statusMonitorStatus)
            self.statusMonitorThread.stop()
            self.statusMonitorThread.wait(10000)
            if not self.statusMonitorThread.isFinished():
                self.statusMonitorThread.terminate()
                self.statusMonitorThread.wait(10000)
            self.statusMonitorThread = None
            self.__statusMonitorStatus(QString("off"), 
                self.trUtf8("Repository status checking is switched off"))
    
    def setStatusMonitorInterval(self, interval, project):
        """
        Public method to change the monitor interval.
        
        @param interval new interval in seconds (integer)
        @param project reference to the project object
        """
        if self.statusMonitorThread is not None:
            if interval == 0:
                self.stopStatusMonitor()
            else:
                self.statusMonitorThread.setInterval(interval)
        else:
            self.startStatusMonitor(project)
    
    def getStatusMonitorInterval(self):
        """
        Public method to get the monitor interval.
        
        @return interval in seconds (integer)
        """
        if self.statusMonitorThread is not None:
            return self.statusMonitorThread.getInterval()
        else:
            return 0
    
    def setStatusMonitorAutoUpdate(self, auto):
        """
        Public method to enable the auto update function.
        
        @param auto status of the auto update function (boolean)
        """
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.setAutoUpdate(auto)
    
    def getStatusMonitorAutoUpdate(self):
        """
        Public method to retrieve the status of the auto update function.
        
        @return status of the auto update function (boolean)
        """
        if self.statusMonitorThread is not None:
            return self.statusMonitorThread.getAutoUpdate()
        else:
            return False
    
    def checkVCSStatus(self):
        """
        Public method to wake up the VCS status monitor thread.
        """
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.checkStatus()
    
    def clearStatusMonitorCachedState(self, name):
        """
        Public method to clear the cached VCS state of a file/directory.
        
        @param name name of the entry to be cleared (QString or string)
        """
        if self.statusMonitorThread is not None:
            self.statusMonitorThread.clearCachedState(name)
        
    def _createStatusMonitorThread(self, interval, project):
        """
        Protected method to create an instance of the VCS status monitor thread.
        
        Note: This method should be overwritten in subclasses in order to support
        VCS status monitoring.
        
        @param interval check interval for the monitor thread in seconds (integer)
        @param project reference to the project object
        @return reference to the monitor thread (QThread)
        """
        return None
