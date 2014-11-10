# -*- coding: utf-8 -*-
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NTypes
import json
import StringIO

from evernote.api.client import EvernoteClient
from xml.dom import minidom

class NoteService():
    def __init__(self, dev_token):
    	if dev_token is not None:
            self._dev_token = dev_token
            self._client = EvernoteClient(token=self._dev_token)
            self._notebookGuid = None
            self._note_names = ["task1", "task2", "task3", "task4"]
            self._notes = None
        else:
            raise Error

    def connect(self):
        userStore = self._client.get_user_store()
        user = userStore.getUser()
        return user.username

    def prepareNotebook(self):
        note_store = self._client.get_note_store()
        notebooks = note_store.listNotebooks()
        l = []
        for n in notebooks:
            if n.name == 'evergtd':
                self._notebookGuid = n.guid
                return
        notebook = Types.Notebook()
        notebook.name = 'evergtd'
        notebook = note_store.createNotebook(notebook)
        self._notebookGuid = notebook.guid

    def prepareNotes(self):
        note_store = self._client.get_note_store()

        note_filter = NTypes.NoteFilter()
        note_filter.notebookGuid = self._notebookGuid
        result_spec = NTypes.NotesMetadataResultSpec(includeTitle=True, includeNotebookGuid=True)
        meta_list = note_store.findNotesMetadata(note_filter, 0, 4, result_spec)

        self._notes = {}
        for meta in meta_list.notes:
            if meta.title in self._note_names:
                self._notes[meta.title] = meta.guid

        for name in self._note_names:
            if name not in self._notes:
                note = Types.Note()
                note.title = name
                note.notebookGuid = self._notebookGuid
                note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
                note.content += '<en-note></en-note>'
                self._notes[name] = note_store.createNote(note).guid

        return len(self._notes)

    def load_node_data(self, name):
        guid = self._notes[name]
        note_store = self._client.get_note_store()
        note = note_store.getNote(guid, True, False, False, False)
        print note.content
        return self.convert_content_json(note.content)

    def convert_json_content(self, json_string):
        objs = json.loads(json_string)
        output = StringIO.StringIO()
        output.write('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">')
        output.write('<en-note>')
        for obj in objs:
            if obj['c'] == 1:
                output.write('<div><en-todo checked="true"></en-todo>')
            else:
                output.write('<div><en-todo></en-todo>')
            output.write(obj['t'])
            output.write('</div>')
        output.write('</en-note>')
        content = output.getvalue()
        output.close()
        return content

    def convert_content_json(self, content):
        dom = minidom.parseString(content)
        el_divs = dom.getElementsByTagName('div')
        objs = []
        for el_div in el_divs:
            obj = {}
            obj['t'] = getText(el_div.childNodes)
            checked = el_div.getElementsByTagName('en-todo')[0].getAttribute('checked')
            if checked and checked == "true":
                obj['c'] = 1
            else:
                obj['c'] = 0
            objs.append(obj)
        return json.dumps(objs)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__ == '__main__':
    dev_token = "S=s1:U=8fcf8:E=150da644ca6:C=14982b31da8:P=1cd:A=en-devtoken:V=2:H=a8defc28f091744b9ebfaea80f5c1d58"
    ns = NoteService(dev_token)
    ns.prepareNotebook()
    print ns.prepareNotes()
    #print ns.convert_json_content('[{"t": "测试招聘人员", "c": 1}, {"t": "研发招聘人员", "c": 0}]')
    #print ns.convert_content_json('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note><div><en-todo checked="true"></en-todo>测试招聘人员</div><div><en-todo></en-todo>研发招聘人员</div></en-note>')
    print ns.convert_json_content(ns.load_node_data('task1'))