import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NTypes

from evernote.api.client import EvernoteClient

class NoteService():
    def __init__(self, dev_token):
    	if dev_token is not None:
            self.dev_token = dev_token
            self.client = EvernoteClient(token=self.dev_token)
        else:
            raise Error

    def connect(self):
        userStore = self.client.get_user_store()
        user = userStore.getUser()
        return user.username

    def prepareNotebook(self):
        note_store = self.client.get_note_store()
        notebooks = note_store.listNotebooks()
        l = []
        for n in notebooks:
            if n.name == 'evergtd':
                return n.guid
        notebook = Types.Notebook()
        notebook.name = 'evergtd'
        notebook = note_store.createNotebook(notebook)
        return notebook.guid

    def prepareNotes(self, notebookGuid):
        note_filter = NTypes.NoteFilter(notebookGuid=notebookGuid)
        result_spec = NTypes.NotesMetadataResultSpec(includeTitle=True, includeNotebookGuid=True)
        note_store = self.client.get_note_store()
        meta_list = note_store.findNotesMetadata(note_filter, 0, 4, result_spec)
        return meta_list.totalNotes()

if __name__ == '__main__':
    dev_token = "S=s1:U=8fcf8:E=150da644ca6:C=14982b31da8:P=1cd:A=en-devtoken:V=2:H=a8defc28f091744b9ebfaea80f5c1d58"
    ns = NoteService(dev_token)
    print ns.prepareNotes(ns.prepareNotebook)
