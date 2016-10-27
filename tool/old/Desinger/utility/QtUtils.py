# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
from controller.ProjectController import *

import shutil
import copy
import json

class QtUtils:
	@staticmethod
	def ContextMenu(arr,parent):
		menu = QMenu(parent.tr(arr[0]), parent);
		for c in arr[1:] : 
			if isinstance(c, list) :
				menu.addMenu(QtUtils.ContextMenu(c,parent));
			elif isinstance(c , basestring):
				menu.addAction(QAction(parent.tr(c), parent));
			else:
				menu.addSeparator();
		return menu

	@staticmethod
	def FileExtension(fileName):
		return ""

	@staticmethod
	def GetResourcePath(_parent,_filter=''):
		pc = ProjectController.getInstance()
		fileName,filt = QFileDialog.getOpenFileName(parent = _parent,dir = pc.path,filter=_filter)
		if len(fileName) > 0:
			if pc.path in fileName:
				return fileName.replace(pc.path,unicode(''))
			else:
				q = QMessageBox.question(_parent,_parent.trUtf8("파일 복사"),_parent.trUtf8("해당 파일을 프로젝트 폴더에 복사하시겠습니까?"),QMessageBox.Cancel,QMessageBox.Yes)
				if q == QMessageBox.Yes :
					fi = QFileInfo(fileName)
					destPath = os.path.join(pc.path,fi.fileName())

					shutil.copyfile(fileName,destPath)

					return os.sep + fi.fileName()
				return ''
	@staticmethod
	def JsonStringify(obj,bePretty=True,exceptList=[]):
		obj = copy.copy(obj)
		if exceptList and len(exceptList) > 0:
			for exceptedKey in exceptList:
				if exceptedKey in obj.__dict__:
					delattr(obj,exceptedKey)

		encoderParams = {}
		encoderParams["default"] = lambda o: o.__dict__
		if bePretty:
			encoderParams["indent"]     = 4
			encoderParams["separators"] = (',', ': ')
			encoderParams["sort_keys"]  = True

		return json.JSONEncoder(**encoderParams).encode(obj)