import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NTypes

from evernote.api.client import EvernoteClient

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
                self._notes[meta.title] = meta

        for name in self._note_names:
            if name not in self._notes:
                note = Types.Note()
                note.title = name
                note.notebookGuid = self._notebookGuid
                note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
                note.content += '<en-note></en-note>'
                self._notes[name] = note_store.createNote(note)

        return len(self._notes)

if __name__ == '__main__':
    dev_token = "S=s1:U=8fcf8:E=150da644ca6:C=14982b31da8:P=1cd:A=en-devtoken:V=2:H=a8defc28f091744b9ebfaea80f5c1d58"
    ns = NoteService(dev_token)
    ns.prepareNotebook()
    print ns.prepareNotes()
