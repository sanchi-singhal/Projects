from flask import Flask, render_template, request
from fin import job_application_admitter

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze',methods=['GET','POST'])
def analyze():
    if request.method=="POST":
        path=request.form['path']
        skills=request.form['skills']
        count=request.form['count']
        ids=request.form['ids']
        
        # print(count)
        l=job_application_admitter(path,skills,count,ids)
        return render_template('l.html',path=path,skills=skills,count=count,ids=ids,l=l)



if __name__=="__main__":
    app.run(debug=True)