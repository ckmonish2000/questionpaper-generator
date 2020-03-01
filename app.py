from flask import Flask,render_template,request,redirect
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,ForeignKey,text
import random


app=Flask(__name__)

engine = create_engine('sqlite:///questionpaper.db', echo = True)

meta=MetaData()

five=Table(
    "five",meta,
    Column("Qid",Integer,primary_key=True),
    Column("Question",String),
    Column("subject",String)
)

meta.create_all(engine)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get",methods=["POST","GET"])
def getdata():
    if request.method=="POST":
        subjects=request.form.get("subject")
        question=request.form.get("question")
        ins=five.insert().values(subject=subjects,Question=question)
        conn=engine.connect()
        conn.execute(ins)
        return "question uploaded"
    return render_template("submit.htm")

@app.route("/view")
def view():
    check=text("select count(Qid) from five")
    conn=engine.connect()
    value=conn.execute(check)
    result=value.fetchall()
    print(result[0][0])
    maxx=result[0][0]
    
    ran=random.randint(1,maxx)
    check1=five.select().where(five.c.Qid==ran)
    value=conn.execute(check1)
    result1=value.fetchall()
    

    ran2=random.randint(1,maxx)
    check2=five.select().where(five.c.Qid==ran2)
    value2=conn.execute(check2)
    result2=value2.fetchall()
    
    
    return render_template("view.html",x=result1,y=result2)

if __name__=="__main__":
    app.run(debug=True)