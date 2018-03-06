# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import base64
import face_recognition
import os
from gluon import current
from gluon.serializers import json
import numpy
from binascii import a2b_base64

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def camera():
    return dict(message=T('HELLO'))

def course_old():
    return dict(message=T('aaaa'))

def faculty_home():
    form = SQLFORM(db.Attendance)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    form.add_button('update form', URL('faculty_home'))
    return dict(message=form)

def add_std():
    form = SQLFORM(db.Student)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    form.add_button('update form', URL('faculty_home'))
    return dict(message=form)

def add_batches():
    form = SQLFORM(db.Batches)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    form.add_button('update form', URL('faculty_home'))
    return dict(message=form)


def upload_std():
    form = SQLFORM(db.image)
    if form.process().accepted:
        image_path = os.path.join(request.folder,'uploads',form.vars.image_file)
        reco = face_recognition.load_image_file(image_path)
        locations = face_recognition.face_locations(reco)
        reco_encodings = face_recognition.face_encodings(reco, locations)[0]
        db(db.image.id==form.vars.id).update(image_encod=",".join(map(str,reco_encodings)))
        form.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    form.add_button('update form', URL('upload_std'))
    return dict(message=form)


def course():
    form = SQLFORM(db.Course)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    form.add_button('update form', URL('course'))
    return dict(message=form)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

def test():

    image = open(os.path.join(current.request.folder, 'images', 'image1.jpeg'), 'rb')

    image_read = image.read()

    image_64_encode = base64.encodestring(image_read)

    image_64_decode = base64.decodestring(image_64_encode)
    """
    image_result = open(os.path.join(current.request.folder, 'images', 'image.jpeg'), 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    reco = face_recognition.load_image_file(os.path.join(current.request.folder, 'images', 'image.jpeg'))
    reco_encoding = face_recognition.face_encodings(reco)[0]

    return json(",".join(map(str,reco_encoding)))
    """
    return "hi"
#Image processing
def capture():

    reco_encodings = []
    #image = request.post_vars.value
    #print(image);
    
    # image = open(os.path.join(current.request.folder, 'images', 'image1.jpeg'), 'rb')
    # image_read = image.read()
    # image_64_encode = base64.encodestring(image_read)

    #image_64_decode = base64.b64decode(image)

   
    #imgData = base64.b64decode(image)

    filepath = os.path.join(current.request.folder, 'images', 'image.png')
    #fd = open(filepath, 'wb')
    #fd.write(imgData)
    #imgData = base64.b64decode(image)
    reco = face_recognition.load_image_file(filepath)
    locations = face_recognition.face_locations(reco)
    reco_encodings = face_recognition.face_encodings(reco, locations)

    rows = db().select(db.image.image_encod, db.image.student_id)
    known_encodings = []
    import numpy as np
    distance = ["test"]
    smallest = 10
    i=0
    for row in rows:
        # encodingsss = row.image_encod.split(" ")
        # print (encodingsss)
        tmp = np.array(row.image_encod.split(","))
        print (tmp)
        known_encodings.append(tmp.astype(np.float))

    if(len(reco_encodings)>0):
        for encoding in reco_encodings:
            distance = face_recognition.face_distance(known_encodings,encoding)
            
        for dist in distance:
            i=i+1
            if dist < smallest:
                smallest = dist
                id = i
    print(rows[id])            
    return smallest
    #return json(",".join(map(str,distance)))
    # rows = db().select(db.image.image_encod, db.image.student_id)
    # image_result = open(os.path.join(current.request.folder, 'images', 'image.jpeg'), 'wb') # create a writable image and write the decoding result
    # image_result.write(image_64_decode)
    # #
    # 
    # for face_location in locations:
    #     
    #     for row in rows:
    #       results = face_recognition.compare_faces(row.encod, reco_encoding)
    #       if results[0] == True:
    #         return row.id

    # reco_encoding = face_recognition.face_encodings(reco)

    # return json(",".join(map(str,reco_encoding)))
    # return json("[{id:1,name:abcd},{id:1,name:abcd}]")


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
