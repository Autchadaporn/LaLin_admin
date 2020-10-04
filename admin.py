from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt



# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='b1c419bc05a2f4'
app.config['MYSQL_PASSWORD']='4923446e'
app.config['MYSQL_HOST']='us-cdbr-east-02.cleardb.com'
app.config['MYSQL_DB']='heroku_afb54efb4938d74'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------------------------จัดการฐานความรู้-------------------------------------------------

@app.route('/Verify',methods=['GET', 'POST'])
def Verify():
    if request.method == "POST":
        username = request.form['username']
        passwods = request.form['password']
    print(username,passwods)
    return redirect(url_for("main"))

@app.route('/main')
def main():
    name = request.args.get('name')
    data = s.tranform_data_topic()
    pattern = s.tranform_data_topic_(s.select_name_tag(name))
    return render_template('main.html',row=data,pattern=pattern)

@app.route('/save',methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        topic = request.form['topic']
    # print(topic)
    return redirect(url_for("main"))


@app.route('/add_intent',methods=['GET', 'POST'])
def add_intent():
    if request.method == 'POST':
        topic = request.form['topic']
        pattern = request.form.getlist('pattern[]')
        # print(topic,pattern)
    return redirect(url_for("main"))



#------------------------------------------จัดการฐานข้อมูล---------------------------------------------------------
#---------- จัดการตาราง calendar ---------------------------------------
@app.route('/calendar')
def calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT calendar.calendar_row_id,topic.topic_id, topic.topic_name, calendar.term ,calendar.date_start, calendar.date_stop,calendar.year,calendar.year_id_name, calendar.case_id FROM topic INNER JOIN calendar ON topic.topic_id = calendar.topic_id ORDER BY calendar.term")
    data = cur.fetchall()
    # -------- เปลี่ยนจาก None เป็นเครื่องหมาย "-" ---------
    for i in range(len(data)):
        if data[i]['date_start'] == None :
            data[i]['date_start'] = "-"
            
        else:
            data[i]['date_start']

    for i in range(len(data)):
        if data[i]['date_stop'] == None :
            data[i]['date_stop'] = "-"
            
        else:
            data[i]['date_stop']

    # -------- แสดง case_name จาก database ------------
    for i in range(len(data)):
        if data[i]['case_id'] == '0' :
            data[i]['case_id'] = "ปกติ"
            
        elif data[i]['case_id'] == '1' :
            data[i]['case_id'] = "ล่าช้า"

    # -------- แสดง year_name จาก database ------------
    # for i in range(len(data)):
    #         if data[i]['year_id_name'] == '0' :
    #             data[i]['year_id_name'] = "all"
    #         elif data[i]['year_id_name'] == '1' :
    #             data[i]['year_id_name'] = "63"
    #         elif data[i]['year_id_name'] == '2' :
    #             data[i]['year_id_name'] = "62"
    #         elif data[i]['year_id_name'] == '3' :
    #             data[i]['year_id_name'] = "61"
    #         elif data[i]['year_id_name'] == '4' :
    #             data[i]['year_id_name'] = "60"
    #         elif data[i]['year_id_name'] == '5' :
    #             data[i]['year_id_name'] = "<60"

    return render_template('calendar_admin.html',data=data)
#---เพิ่มปฏิทินการศึกษา
@app.route('/addcalendar',methods=['GET','POST'])
def addcalendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topic")  #แสดงข้อมูลกิจกรรม
    topic = cur.fetchall()
    if request.method=='POST':
        topic_id = request.form['topic_id']
        term = request.form['term']
        date_start = request.form['date_start']
        date_stop = request.form['date_stop']
        year = request.form['year']
        year_id_name = request.form['year_id_name']
        case_id = request.form['case_id']

        print(topic_id,term,date_start,date_stop,year,year_id_name,case_id)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO calendar(topic_id,term,date_start,date_stop,year,year_id_name,case_id) VALUES('"+topic_id+"','"+term+"','"+date_start+"','"+date_stop+"','"+year+"','"+year_id_name+"','"+case_id+"')") #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
        mysql.connection.commit()
        return redirect(url_for('calendar'))

    return render_template('formAddCalendar.html',topic=topic) 
# ----เพิ่มกิจกรรม
@app.route('/addtopic',methods=['GET','POST'])
def addtopic():
    if request.method=='POST':
        topic_name = request.form['topic_name']
        print(topic_name)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO topic(topic_name) VALUES('"+topic_name+"')") #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
        mysql.connection.commit()
    return redirect(url_for('addcalendar'))
#--- ลบปฏิทิน
@app.route('/deletecalendar/<string:id>',methods=["GET","POST"])
def deletecalendar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM calendar WHERE calendar_row_id='"+id+"' ") #เลือกลบข้อมูลที่มีค่าเท่ากับ id รับค่ามาจาก หน้า calendar
    mysql.connection.commit()
    return redirect(url_for('calendar'))
#--- แก้ไขปฏิทิน
@app.route('/editcalendar',methods=["GET","POST"])
def editcalendar():
    if request.method == 'POST':
        calendar_row_id = request.form['calendar_row_id']
        topic_id = request.form['topic_id']
        term = request.form['term']
        date_start = request.form['date_start']
        date_stop = request.form['date_stop']
        year = request.form['year']
        year_id_name = request.form['year_id_name']
        case_id = request.form['case_id']
        print(topic_id,term,date_start,date_stop,year,year_id_name,case_id)
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE calendar SET  topic_id='"+topic_id+"', term= '"+term+"', date_start= '"+date_start+"', date_stop= '"+date_stop+"', year= '"+year+"' , year_id_name= '"+year_id_name+"' , case_id= '"+case_id+"'  WHERE calendar_row_id='"+calendar_row_id+"'" )
        mysql.connection.commit()

    return redirect(url_for('calendar'))


#---------- จัดการตาราง subject ---------------------------------------
@app.route('/subject')
def subject():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subject")
    data = cur.fetchall()
    # -------- เปลี่ยนจาก None เป็นเครื่องหมาย "-" ---------
    for i in range(len(data)):
        if data[i]['subject_nameEng'] == None :
            data[i]['subject_nameEng'] = "-"
            
        else:
            data[i]['subject_nameEng']
    return render_template('subject_admin.html',data=data)
# เพิ่มรายวิชา
@app.route('/addsubject',methods=['GET','POST'])
def addsubject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        subject_nameTh = request.form['subject_nameTh']
        subject_nameEng = request.form['subject_nameEng']
        unit = request.form['unit']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subject(subject_id,subject_nameTh,subject_nameEng,unit) VALUES('"+subject_id+"','"+subject_nameTh+"','"+subject_nameEng+"','"+unit+"')") #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
        mysql.connection.commit()
        return redirect(url_for('subject'))
    return render_template('formAddSubject.html')
# ลบรายวิชา
@app.route('/deletesubject/<string:id>',methods=["GET","POST"])
def deletesubject(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM subject WHERE subject_id='"+id+"' ") #เลือกลบข้อมูลที่มีค่าเท่ากับ id รับค่ามาจาก หน้า calendar
    mysql.connection.commit()
    return redirect(url_for('subject'))
# แก้ไขรายวิชา
@app.route('/editsubject',methods=["GET","POST"])
def editsubject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        subject_nameTh = request.form['subject_nameTh']
        subject_nameEng = request.form['subject_nameEng']
        unit = request.form['unit']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE subject SET  subject_id='"+subject_id+"', subject_nameTh= '"+subject_nameTh+"',subject_nameEng= '"+subject_nameEng+"', unit= '"+unit+"' WHERE subject_id='"+subject_id+"'" )
        mysql.connection.commit()

    return redirect(url_for('subject'))

#---------- จัดการตาราง plan -----------------------------------
@app.route('/plan')
def plan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM plan")
    data = cur.fetchall()
    # -------- เปลี่ยนจาก None เป็นเครื่องหมาย "-" ---------
    return render_template('plan_admin.html',data=data)
# เพิ่มแผนการศึกษา
@app.route('/addplan',methods=['GET','POST'])
def addplan():
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        plan_name = request.form['plan_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO plan(plan_id,plan_name) VALUES('"+plan_id+"','"+plan_name+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('plan'))
    return render_template('formAddPlan.html')   

# ลบแผนการเรียน 
@app.route('/deleteplan/<string:id>',methods=["GET","POST"])
def deleteplan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM plan WHERE plan_id='"+id+"' ") #เลือกลบข้อมูลที่มีค่าเท่ากับ id รับค่ามาจาก หน้า calendar
    mysql.connection.commit()
    return redirect(url_for('plan'))
 
# แก้ไขแผนการเรียน
@app.route('/editplan',methods=["GET","POST"])
def editplan():
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        plan_name = request.form['plan_name']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE plan SET  plan_id='"+plan_id+"', plan_name= '"+plan_name+"' WHERE plan_id ='"+plan_id+"'" )
        mysql.connection.commit()

    return redirect(url_for('plan'))


#---------- จัดการตาราง case -----------------------------------
@app.route('/case')
def case():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM heroku_afb54efb4938d74.case;")
    data = cur.fetchall()
    # -------- เปลี่ยนจาก None เป็นเครื่องหมาย "-" ---------
    return render_template('case_admin.html',data=data)
# เพิ่มแผนการศึกษา
@app.route('/addcase',methods=['GET','POST'])
def addcase():
    if request.method == 'POST':
        case_id = request.form['case_id']
        case_name = request.form['case_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO heroku_afb54efb4938d74.case(case_id,case_name) VALUES('"+case_id+"','"+case_name+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('case'))
    return render_template('formAddCase.html')
# ลบกรณี 
@app.route('/deletecase/<string:id>',methods=["GET","POST"])
def deletecase(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM heroku_afb54efb4938d74.case WHERE case_id='"+id+"' ") #เลือกลบข้อมูลที่มีค่าเท่ากับ id รับค่ามาจาก หน้า calendar
    mysql.connection.commit()
    return redirect(url_for('case'))    
# แก้ไขcase 
@app.route('/editcase',methods=["GET","POST"])
def editcase():
    if request.method == 'POST':
        case_id = request.form['case_id']
        case_name = request.form['case_name']
        # print(case_id,case_name)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE heroku_afb54efb4938d74.case SET  case_id='"+case_id+"', case_name='"+case_name+"' WHERE case_id='"+case_id+"'" )
        mysql.connection.commit()

    return redirect(url_for('case'))

#---------- จัดการตาราง student -----------------------------------
@app.route('/student')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM plan;")
    plan = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student;")
    data = cur.fetchall()
    # -------- เปลี่ยนจาก None เป็นเครื่องหมาย "-" ---------
    return render_template('student_admin.html',data=data,plan=plan)

# เพิ่มนิสิต
@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM plan;")
    plan = cur.fetchall()
    if request.method == 'POST':
        student_id= request.form['student_id']
        student_name = request.form['student_name']
        student_lastName = request.form['student_lastName']
        plan_id = request.form['plan_id']
        year_id = request.form['year_id']
        # print(student_id,student_name,student_lastName,plan_id,year_id)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student(student_id,student_name,student_lastName,plan_id,year_id) VALUES('"+student_id+"','"+student_name+"','"+student_lastName+"','"+plan_id+"','"+year_id+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('student'))
    return render_template('formAddStudent.html',plan=plan)

# ลบนิสิต 
@app.route('/deletestudent/<string:id>',methods=["GET","POST"])
def deletestudent(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE student_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('student'))  

# แก้ไขนิสิต
@app.route('/editstudent',methods=["GET","POST"])
def editstudent():
    if request.method == 'POST':
        student_id= request.form['student_id']
        student_name = request.form['student_name']
        student_lastName = request.form['student_lastName']
        plan_id = request.form['plan_id']
        year_id = request.form['year_id']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student SET  student_id='"+student_id+"', student_name='"+student_name+"',student_lastName='"+student_lastName+"',plan_id='"+plan_id+"',year_id='"+year_id+"' WHERE student_id='"+student_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('student'))
  

#---------- จัดการตาราง teacher -----------------------------------
@app.route('/teacher')
def teacher():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM teacher;")
    data = cur.fetchall()
    return render_template('teacher_admin.html',data=data)   
# เพิ่มอาจารย์
@app.route('/addteacher',methods=['GET','POST'])
def addteacher():
    if request.method == 'POST':
        teacher_id= request.form['teacher_id']
        teacher_name = request.form['teacher_name']
        teacher_lastName = request.form['teacher_lastName']
        print(teacher_id,teacher_name,teacher_lastName)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO teacher(teacher_id,teacher_name,teacher_lastName) VALUES('"+teacher_id+"','"+teacher_name+"','"+teacher_lastName+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('teacher'))
    return render_template('formAddTeacher.html')
# ลบอาจารย์ 
@app.route('/deleteteacher/<string:id>',methods=["GET","POST"])
def deleteteacher(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM teacher WHERE teacher_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('teacher'))
# แก้ไขอาจารย์
@app.route('/editteacher',methods=["GET","POST"])
def editteacher():
    if request.method == 'POST':
        teacher_id= request.form['teacher_id']
        teacher_name = request.form['teacher_name']
        teacher_lastName = request.form['teacher_lastName']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE teacher SET  teacher_id='"+teacher_id+"', teacher_name='"+teacher_name+"',teacher_lastName='"+teacher_lastName+"' WHERE teacher_id='"+teacher_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('teacher'))  

#---------- จัดการตาราง year -----------------------------------
@app.route('/year')
def year():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM year;")
    data = cur.fetchall()
    return render_template('year_admin.html',data=data) 
# เพิ่มปี
@app.route('/addyear',methods=['GET','POST'])
def addyear():
    if request.method == 'POST':
        year_id_name= request.form['year_id_name']
        year_name = request.form['year_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO year(year_id_name,year_name) VALUES('"+year_id_name+"','"+year_name+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('year'))
    return render_template('formAddYear.html')
# ลบปี 
@app.route('/deleteyear/<string:id>',methods=["GET","POST"])
def deleteyear(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM year WHERE year_id_name='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('year'))
# แก้ไขปี
@app.route('/edityear',methods=["GET","POST"])
def edityear():
    if request.method == 'POST':
        year_id_name= request.form['year_id_name']
        year_name = request.form['year_name']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE year SET  year_id_name='"+year_id_name+"', year_name='"+year_name+"' WHERE year_id_name='"+year_id_name+"'" )
        mysql.connection.commit()
    return redirect(url_for('year')) 

#---------- จัดการตาราง adviser -----------------------------------
@app.route('/adviser')
def adviser():
    cur = mysql.connection.cursor()
    cur.execute("select * from adviser left join student on student.student_id = adviser.student_id left join teacher on teacher.teacher_id = adviser.teacher_id;")
    # cur.execute("select adviser.adviser_row_id,student.student_name,student.student_lastName,teacher.teacher_name,teacher.teacher_lastName,adviser.adviser_status from adviser left join student on student.student_id = adviser.student_id left join teacher on teacher.teacher_id = adviser.teacher_id;")
    data = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("select * from student ;")
    student = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("select * from teacher ;")
    teacher = cur.fetchall()
    return render_template('adviser_admin.html',data=data,student=student,teacher=teacher)
# เพิ่มที่ปรึกษา
@app.route('/addadviser',methods=['GET','POST'])
def addadviser():
    cur = mysql.connection.cursor()
    cur.execute("select * from student ;")
    student = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("select * from teacher ;")
    teacher = cur.fetchall()
    if request.method == 'POST':
        student_id= request.form['student_id']
        teacher_id = request.form['teacher_id']
        adviser_status= request.form['adviser_status']
        print(student_id,teacher_id,adviser_status)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO adviser(student_id,teacher_id,adviser_status) VALUES('"+student_id+"','"+teacher_id+"','"+adviser_status+"')") #เพิ่ม
        mysql.connection.commit()
        return redirect(url_for('adviser'))
    return render_template('formAddAdviser.html',student=student,teacher=teacher)
# ลบที่ปรึกษา
@app.route('/deleteadviser/<string:id>',methods=["GET","POST"])
def deleteadviser(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM adviser WHERE adviser_row_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('adviser'))
# แก้ไขที่ปรึกษา
@app.route('/editadviser',methods=["GET","POST"])
def editadviser():
    if request.method == 'POST':
        adviser_row_id= request.form['adviser_row_id']
        student_id= request.form['student_id']
        teacher_id = request.form['teacher_id']
        adviser_status= request.form['adviser_status']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE adviser SET  student_id='"+student_id+"', teacher_id='"+teacher_id+"' ,adviser_status='"+adviser_status+"'WHERE adviser_row_id='"+adviser_row_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('adviser')) 

#---------- จัดการตาราง topic -----------------------------------
@app.route('/topic')
def topic():
    cur = mysql.connection.cursor()
    cur.execute("select * from topic;")
    data = cur.fetchall()
    return render_template('topic_admin.html',data=data)
# เพิ่มกิจกรรม
@app.route('/addtopictable',methods=['GET','POST'])
def addtopictable():
    if request.method=='POST':
        topic_name = request.form['topic_name']
        print(topic_name)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO topic(topic_name) VALUES('"+topic_name+"')") #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
        mysql.connection.commit()
        return redirect(url_for('topic'))
    return render_template('formAddTopic.html')
# ลบกิจกรรม
@app.route('/deletetopic/<string:id>',methods=["GET","POST"])
def deletetopic(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM topic WHERE topic_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('topic'))
# แก้ไขกิจกรรม
@app.route('/edittopic',methods=["GET","POST"])
def edittopic():
    if request.method == 'POST':
        topic_id= request.form['topic_id']
        topic_name= request.form['topic_name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE topic SET  topic_name='"+topic_name+"' WHERE topic_id='"+topic_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('topic'))

#---------- จัดการตาราง member -----------------------------------
@app.route('/members')
def members():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM members LEFT JOIN teacher ON teacher.teacher_id = members.member_id LEFT JOIN student ON student.student_id = members.member_id;")
    data = cur.fetchall()
    return render_template('members_admin.html',data=data) 
# ลบmember
@app.route('/deletemember/<string:id>',methods=["GET","POST"])
def deletemember(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM members WHERE members_row_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('members'))


#---------- จัดการตาราง studyplan -----------------------------------
# ดูแผนการเรียน
@app.route('/study_plan',methods=['GET','POST'])
def study_plan():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM plan ;")
        plan = cur.fetchall()

        plan_id = request.form['plan_id']
        print(plan_id)
        cur = mysql.connection.cursor()
        cur.execute("SELECT study_plan.study_plan_row_id,study_plan.plan_id, subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '"+plan_id+"' order by year,term;")
        data = cur.fetchall()
        for i in range(len(data)):
            if data[i]['subject_nameEng'] == None :
                data[i]['subject_nameEng'] = "-"
                
            else:
                data[i]['subject_nameEng']
        return render_template('study_plan_admin.html',plan=plan,data=data)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM plan ;")
        plan = cur.fetchall()
        return render_template('study_plan_admin.html',plan=plan) 
# เพิ่มวิชาลงแผนการเรียน
@app.route('/addstudy_plan',methods=['GET','POST'])
def addstudy_plan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM plan ;")
    plan = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subject ;")
    subject = cur.fetchall()
    for i in range(len(subject)):
            if subject[i]['subject_nameEng'] == None :
                subject[i]['subject_nameEng'] = " "
                
            else:
                subject[i]['subject_nameEng']
    if request.method=='POST':
        plan_id = request.form['plan_id']
        subject_id = request.form['subject_id']
        year = request.form['year']
        term = request.form['term']
        print(plan_id,subject_id,year,term)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO study_plan(plan_id,subject_id,year,term) VALUES('"+plan_id+"','"+subject_id+"','"+year+"','"+term+"')") #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
        mysql.connection.commit()
        return redirect(url_for('study_plan'))
    return render_template('formAddStudy_plan.html',plan=plan,subject=subject)
# ลบmember
@app.route('/deletestudy_plan/<string:id>',methods=["GET","POST"])
def deletestudy_plan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM study_plan WHERE study_plan_row_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('study_plan'))

#---------- จัดการตาราง student_grade -----------------------------------
@app.route('/student_grade',methods=['GET','POST'])
def student_grade():
    if request.method == 'POST' :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student ;")
        student = cur.fetchall()

        student_id = request.form['student_id']
        print(student_id)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_grade WHERE student_id='"+student_id+"' ")
        data = cur.fetchall()
        return render_template('student_grade_admin.html',student=student,data=data)

    if request.method == 'GET' : #รัยค่าแบบ GET เพื่อเรียกดูหลังจากเพิ่มเกรดของนิสิตคนนั้นแล้ว 
        student_id = request.args.get('student_id')
        print('student_id:',student_id)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_grade WHERE student_id='"+student_id+"' ")
        data = cur.fetchall()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student ;")
        student = cur.fetchall()
        return render_template('student_grade_admin.html',student=student,data=data)


@app.route('/student_grade_show',methods=['GET','POST'])
def student_grade_show():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student ") 
    student = cur.fetchall()
    return render_template('student_grade_admin.html',student=student)

# เพิ่มวิชาลงแผนข้อมูลเกรดของนิสิต
@app.route('/addstudent_grade',methods=['GET','POST'])
def addstudent_grade():
    if request.method =='POST':
        student_id = request.form.getlist('student_id')
        subject_id = request.form.getlist('subject_id')
        grade = request.form.getlist('grade')
        year = request.form.getlist('year')
        term = request.form.getlist('term')
        unit = request.form.getlist('unit')
        print(subject_id,grade,year,term,unit)

        for index in range(len(unit)):
            # print(index)
            # cur = mysql.connection.cursor()
            # cur.execute (" INSERT INTO student_grade(student_id,subject_id,grade,term,year,unit) VALUES (%s,%s,%s,%s,%s,%s)",(student_id[index],subject_id[index],grade[index],term[index],year[index],unit[index])) 
            # print(cur.execute)
            # mysql.connection.commit()
            x=str(student_id[0])
        return redirect(url_for('student_grade',student_id=x))
    return render_template('formAddStudent_grade.html')

# ลบรายวิชาออกจากตาราง student_grade
@app.route('/deletestudent_grade/<string:id>',methods=["GET","POST"])
def deletestudent_grade(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_id FROM student_grade WHERE student_grade_row_id='"+id+"' ") #เลือกลบข้อมูล
    student_id = cur.fetchall()
    student_id=student_id[0]['student_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student_grade WHERE student_grade_row_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('student_grade',student_id=student_id))

# แก้ไขตาราง studenst_grade
@app.route('/editstudent_grade',methods=["GET","POST"])
def editstudent_grade():
    if request.method == 'POST':
        student_grade_row_id =  request.form['student_grade_row_id']
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        grade = request.form['grade']
        year = request.form['year']
        term = request.form['term']
        unit = request.form['unit']
        print(student_grade_row_id,student_id,subject_id,grade,year,term,unit)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student_grade SET  student_id='"+student_id+"',subject_id='"+subject_id+"',grade='"+grade+"',year='"+year+"',term='"+term+"',unit='"+unit+"' WHERE student_grade_row_id='"+student_grade_row_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('student_grade',student_id=student_id))

#---------- จัดการตาราง student_grade_cal -----------------------------------
@app.route('/student_grade_cal_show',methods=['GET','POST'])
def student_grade_cal_show():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student ") 
    student = cur.fetchall()
    return render_template('student_grade_cal_admin.html',student=student)

@app.route('/student_grade_cal',methods=['GET','POST'])
def student_grade_cal():
    if request.method == 'POST' :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student ;")
        student = cur.fetchall()

        student_id = request.form['student_id']
        print(student_id)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_grade_cal WHERE student_id='"+student_id+"' ")
        data = cur.fetchall()
        return render_template('student_grade_cal_admin.html',student=student,data=data,student_id=student_id)

    if request.method == 'GET' : #รัยค่าแบบ GET เพื่อเรียกดูหลังจากเพิ่มเกรดของนิสิตคนนั้นแล้ว 
        student_id = request.args.get('student_id')
        print('student_id:',student_id)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_grade_cal WHERE student_id='"+student_id+"' ")
        data = cur.fetchall()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student ;")
        student = cur.fetchall()
        return render_template('student_grade_cal_admin.html',student=student,data=data,student_id=student_id)
# แก้ไขตาราง student_grade_cal
@app.route('/editstudent_grade_cal',methods=["GET","POST"])
def editstudent_grade_cal():
    if request.method == 'POST':
        student_grade_row_id =  request.form['student_grade_row_id']
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        grade = request.form['grade_cal']
        year = request.form['year']
        term = request.form['term']
        unit = request.form['unit']
        print(student_grade_row_id,student_id,subject_id,grade_cal,year,term,unit)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student_grade_cal SET  student_id='"+student_id+"',subject_id='"+subject_id+"',grade_cal='"+grade_cal+"',year='"+year+"',term='"+term+"',unit='"+unit+"' WHERE student_grade_row_id='"+student_grade_row_id+"'" )
        mysql.connection.commit()
    return redirect(url_for('student_grade_cal',student_id=student_id))
# ลบรายวิชาออกจากตาราง student_grade_cal
@app.route('/deletestudent_grade_cal/<string:id>',methods=["GET","POST"])
def deletestudent_grade_cal(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_id FROM student_grade WHERE student_grade_row_id='"+id+"' ") #เลือกลบข้อมูล
    student_id = cur.fetchall()
    student_id=student_id[0]['student_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student_grade_cal WHERE student_grade_row_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('student_grade_cal',student_id=student_id))

#---------- จัดการตาราง /student_gpax -----------------------------------
@app.route('/student_gpax',methods=['GET','POST'])
def student_gpax():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_gpax ") 
    data = cur.fetchall()
    return render_template('student_gpax_admin.html',data=data)
# ลบรายวิชาออกจากตาราง /student_gpax
@app.route('/deletestudent_gpax/<string:id>',methods=["GET","POST"])
def deletestudent_gpax(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student_gpax WHERE student_id='"+id+"' ") #เลือกลบข้อมูล
    mysql.connection.commit()
    return redirect(url_for('student_gpax'))


if __name__== "__main__" :
    app.run(debug=True)