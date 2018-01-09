from flask import Flask,redirect,request,url_for,session,render_template,send_from_directory
import dailymotion

app=Flask(__name__)

d = dailymotion.Dailymotion()
d.set_grant_type('password', api_key='879b2eb629c135f5280d', api_secret='58fccdb81da919abd0a2143a68b8b2ff4e3afc0e',scope=['manage_videos'], info={'username': 'ahmed_yousef136@zhorachu.com', 'password': '123456789z!'})
@app.route('/index')
def index():
    return render_template('index.html',message="upload to dailymotion")

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    work_path = os.path.dirname(os.path.realpath(__file__))+"\\tmp"
    file=os.path.join(work_path,local_filename)
    r = requests.get(url, stream=True)
    with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename
   
@app.route('/upload',methods=['GET','POST'])
def upload():
    file_url=request.form['url']
    work_path = os.path.dirname(os.path.realpath(__file__))+"\\tmp"
    file_name=download_file(file_url)
    path=os.path.join(work_path, file_name)
    url = d.upload(path)
    message='please auth'
    d.post('/me/videos',{'url': url, 'title': file_name, 'published': 'true', 'explicit': 'false'})
    return render_template('index.html',message=message)

if __name__=='__main__':
    app.run(threaded=True)




