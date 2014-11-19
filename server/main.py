# -*- coding: utf-8 -*-
import web
import service
import evernote.edam.type.ttypes as Types
        
urls = (
    '/i/connect', 'connect',
	'/i/loadall', 'loadall',
    '/i/update', 'update'
)
app = web.application(urls, globals())
dev_token = "S=s1:U=8fcf8:E=150da644ca6:C=14982b31da8:P=1cd:A=en-devtoken:V=2:H=a8defc28f091744b9ebfaea80f5c1d58"
ns = service.NoteService(dev_token)
ns.prepareNotebook()
ns.prepareNotes()

class connect:        
    def GET(self):
        return ns.connect()

class loadall:
    def GET(self):
        return ns.load_all_note_data()

class update:
    def POST(self):
        i = web.input()
        name = i.name
        if ns.is_allowed_name(name):
            content = i.content
            jsonString = ns.update_note_data(name, content)
            return '{"r":0, "data": ' + jsonString + '}'
        else:
            return '{"r":2}'


if __name__ == "__main__":
    app.run()
