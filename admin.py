from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


@admin.route('/admin_view_users')
def admin_view_users():
    data={}
    q="select * from user"
    data['res']=select(q)
    
    return render_template('admin_view_users.html',data=data)


@admin.route('/adminviewmostplayer')
def adminviewmostplayer():
    data={}
    q="select * from user"
    data['res']=select(q)
    
    return render_template('adminviewmostplayer.html',data=data)



@admin.route('/adminmanagecaterogy',methods=['get','post'])
def adminmanagecaterogy():
    data={}
    if 'btn' in request.form:
        place=request.form['place']
        
    
        q="insert into category values (null,'%s')"%(place)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.adminmanagecaterogy"))

    data={}
    q="select * from category"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        cid=request.args['cid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from category where category_id='%s'"%(cid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            place=request.form['place']

            q="update category set category='%s' where category_id='%s' "%(place,cid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.adminmanagecaterogy"))
    if action == "delete":
        q="delete from category where category_id='%s' "%(cid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.adminmanagecaterogy"))
    return render_template('adminmanagecaterogy.html',data=data) 

import uuid

@admin.route('/adminmanagemusic',methods=['get','post'])
def adminmanagemusic():
    data={}
    q="select * from category"
    data['cat']=select(q)
    if 'btn' in request.form:
        cat=request.form['cat']
        name=request.form['name']
        music=request.files['music']
        path="static/music/"+str(uuid.uuid4())+music.filename
        music.save(path)
        lyrics=request.form['lyrics']
        
    
        q="insert into music values (null,'%s','%s','%s','%s')"%(cat,name,path,lyrics)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.adminmanagemusic"))

   
    q="select * from music inner join category using (category_id)"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        mid=request.args['mid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from music where music_id='%s'"%(mid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
           
            name=request.form['name']
            lyrics=request.form['lyrics']
            if request.files['music']:

                music=request.files['music']
                path="static/music/"+str(uuid.uuid4())+music.filename
                music.save(path)
                q="update music set music='%s', path='%s', lyrics='%s' where music_id='%s' "%(name,path,lyrics,mid)
            else:
                q="update music set music='%s',  lyrics='%s' where music_id='%s' "%(name,lyrics,mid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.adminmanagemusic"))
    if action == "delete":
        q="delete from music where music_id='%s' "%(mid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.adminmanagemusic"))
    return render_template('adminmanagemusic.html',data=data) 