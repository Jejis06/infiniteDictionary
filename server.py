from flask import Flask, request, send_from_directory
import requests as rq
import os
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
def catch_all(path):
    path = path.replace('?','').replace('!','').replace('.','').replace(',','').replace(';','').replace(':','').replace('(','').replace(')','').replace('[','').replace(']','')
    print(path)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{path}"
    raw = rq.get(url)
    print(url)

    print(raw.json())
    try:
        base = raw.json()[0]
        meanings = base['meanings']
        inner = ""

        for m in meanings:
            inner += f'<h3>{m["partOfSpeech"]}</h3><ul>'
            for d in m['definitions']:
                 ex = ""
                 try:                     
                    ex = "<p>"
                    rawEx = d['example'].split(' ')
                    
                    for u in rawEx:                                                  
                         ex += f"<a href='{request.base_url.split('/')[0]}/{u}'> {u}</a>"
                    ex += "</p>"
                    
                 except :
                      ex = ""
                      
                 defini = "<p>"
                 rawdef = d['definition'].split(' ')
                 for u in rawdef:                                                  
                    defini += f"<a href='{request.base_url.split('/')[0]}/{u}'> {u}</a>"
                 defini += "</p>"
                      
                 inner += f"<li><div> {defini}<b>{ex}</b> </div></li><br>"
            inner += "</ul>"

        phon = ""
        if "phonetic" in base:
            phon = base["phonetic"]
        else:
             for it in base["phonetics"]:
                  if "text" in it:
                       phon = it["text"]
                       break
        return f'''
            <body>
                <div style="display:flex">
                    <h1>{base["word"]}</h1>
                    <h5>{phon}</h2>
                </div>
                {inner}
            </body>
        '''
    except:
         return f"dead end sr for {path}"
    


if __name__ == '__main__':
	app.run()
