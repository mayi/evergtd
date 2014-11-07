import web
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient
        
urls = (
    '/connect', 'connect',
	'/preparenotebook', 'preparenotebook'
)
app = web.application(urls, globals())
dev_token = "S=s1:U=8fcf8:E=150da644ca6:C=14982b31da8:P=1cd:A=en-devtoken:V=2:H=a8defc28f091744b9ebfaea80f5c1d58"
client = EvernoteClient(token=dev_token)
class connect:        
    def GET(self):
        userStore = client.get_user_store()
        user = userStore.getUser()
        return user.username

class new:
    def POST(self):
        return 'new'

class preparenotebook:
	def GET(self):
		note_store = client.get_note_store()
		notebooks = note_store.listNotebooks()
		l = []
		for n in notebooks:
			if n.name == 'evergtd':
				return n.guid
		notebook = Types.Notebook()
		notebook.name = 'evergtd'
		notebook = note_store.createNotebook(notebook)
		return notebook.guid

if __name__ == "__main__":
    app.run()
