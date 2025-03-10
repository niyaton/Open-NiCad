# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2010 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a typing completer for Ruby.
"""

from PyQt4.QtCore import QObject, SIGNAL, QRegExp
from PyQt4.Qsci import QsciLexerRuby

from CompleterBase import CompleterBase

import Preferences

class CompleterRuby(CompleterBase):
    """
    Class implementing typing completer for Ruby.
    """
    def __init__(self, editor, parent = None):
        """
        Constructor
        
        @param editor reference to the editor object (QScintilla.Editor)
        @param parent reference to the parent object (QObject)
        """
        CompleterBase.__init__(self, editor, parent)
        
        self.__beginRX = QRegExp(r"""^=begin """)
        self.__beginNlRX = QRegExp(r"""^=begin\r?\n""")
        self.__hereRX = QRegExp(r"""<<-?['"]?(\w*)['"]?\r?\n""")
        
        self.readSettings()
    
    def readSettings(self):
        """
        Public slot called to reread the configuration parameters.
        """
        self.setEnabled(Preferences.getEditorTyping("Ruby/EnabledTypingAids"))
        self.__insertClosingBrace = \
            Preferences.getEditorTyping("Ruby/InsertClosingBrace")
        self.__indentBrace = \
            Preferences.getEditorTyping("Ruby/IndentBrace")
        self.__skipBrace = \
            Preferences.getEditorTyping("Ruby/SkipBrace")
        self.__insertQuote = \
            Preferences.getEditorTyping("Ruby/InsertQuote")
        self.__insertBlank = \
            Preferences.getEditorTyping("Ruby/InsertBlank")
        self.__insertHereDoc = \
            Preferences.getEditorTyping("Ruby/InsertHereDoc")
        self.__insertInlineDoc = \
            Preferences.getEditorTyping("Ruby/InsertInlineDoc")

    def charAdded(self, charNumber):
        """
        Public slot called to handle the user entering a character.
        
        @param charNumber value of the character entered (integer)
        """
        char = unichr(charNumber)
        if char not in ['(', ')', '{', '}', '[', ']', ',', "'", '"', '\n', ' ']:
            return  # take the short route
        
        line, col = self.editor.getCursorPosition()
        
        if self.__inComment(line, col) or \
           self.__inDoubleQuotedString() or \
           self.__inSingleQuotedString() or \
           self.__inHereDocument() or \
           self.__inInlineDocument():
            return
        
        # open parenthesis
        # insert closing parenthesis and self
        if char == '(':
            txt = self.editor.text(line).left(col)
            if self.__insertClosingBrace:
                self.editor.insert(')')
        
        # closing parenthesis
        # skip matching closing parenthesis
        elif char in [')', '}', ']']:
            if char == self.editor.text(line).mid(col, 1):
                if self.__skipBrace:
                    self.editor.setSelection(line, col, line, col + 1)
                    self.editor.removeSelectedText()
        
        # space
        # complete inline documentation
        elif char == ' ':
            txt = self.editor.text(line).left(col)
            if self.__insertInlineDoc and self.__beginRX.exactMatch(txt):
                self.editor.insert('=end')
        
        # comma
        # insert blank
        elif char == ',':
            if self.__insertBlank:
                self.editor.insert(' ')
                self.editor.setCursorPosition(line, col + 1)
        
        # open curly brace
        # insert closing brace
        elif char == '{':
            if self.__insertClosingBrace:
                self.editor.insert('}')
        
        # open bracket
        # insert closing bracket
        elif char == '[':
            if self.__insertClosingBrace:
                self.editor.insert(']')
        
        # double quote
        # insert double quote
        elif char == '"':
            if self.__insertQuote:
                self.editor.insert('"')
        
        # quote
        # insert quote
        elif char == '\'':
            if self.__insertQuote:
                self.editor.insert('\'')
        
        # new line
        # indent to opening brace, complete inline documentation
        elif char == '\n':
            txt = self.editor.text(line - 1)
            if self.__insertInlineDoc and self.__beginNlRX.exactMatch(txt):
                self.editor.insert('=end')
            elif self.__insertHereDoc and self.__hereRX.exactMatch(txt):
                self.editor.insert(self.__hereRX.cap(1))
            elif self.__indentBrace and txt.lastIndexOf(QRegExp(":\r?\n")) == -1:
                    openCount = txt.count(QRegExp("[({[]"))
                    closeCount = txt.count(QRegExp("[)}\]]"))
                    if openCount > closeCount:
                        lastOpenIndex = 0
                        openCount = 0
                        closeCount = 0
                        while lastOpenIndex > -1 and openCount == closeCount:
                            lastOpenIndex = \
                                txt.lastIndexOf(QRegExp("[({[]"), lastOpenIndex - 1)
                            txt2 = txt.mid(lastOpenIndex)
                            openCount = txt2.count(QRegExp("[({[]"))
                            closeCount = txt2.count(QRegExp("[)}\]]"))
                        if lastOpenIndex > -1 and lastOpenIndex > col:
                            self.editor.insert(' ' * (lastOpenIndex - col + 1))
                            self.editor.setCursorPosition(line, lastOpenIndex + 1)
    
    def __inComment(self, line, col):
        """
        Private method to check, if the cursor is inside a comment
        
        @param line current line (integer)
        @param col current position within line (integer)
        @return flag indicating, if the cursor is inside a comment (boolean)
        """
        txt = self.editor.text(line)
        while col >= 0:
            if txt.mid(col, 1) == "#":
                return True
            col -= 1
        return False
    
    def __inDoubleQuotedString(self):
        """
        Private method to check, if the cursor is within a double quoted string.
        
        @return flag indicating, if the cursor is inside a double 
            quoted string (boolean)
        """
        return self.editor.currentStyle() == QsciLexerRuby.DoubleQuotedString
    
    def __inSingleQuotedString(self):
        """
        Private method to check, if the cursor is within a single quoted string.
        
        @return flag indicating, if the cursor is inside a single 
            quoted string (boolean)
        """
        return self.editor.currentStyle() == QsciLexerRuby.SingleQuotedString
    
    def __inHereDocument(self):
        """
        Private method to check, if the cursor is within a here document.
        
        @return flag indicating, if the cursor is inside a here document (boolean)
        """
        return self.editor.currentStyle() == QsciLexerRuby.HereDocument
    
    def __inInlineDocument(self):
        """
        Private method to check, if the cursor is within an inline document.
        
        @return flag indicating, if the cursor is inside an inline document (boolean)
        """
        return self.editor.currentStyle() == QsciLexerRuby.POD
