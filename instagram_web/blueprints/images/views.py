from flask import Flask, render_template, request, redirect, Blueprint, url_for, flash
from werkzeug import secure_filename
from flask_login import current_user
from helpers import *
from models.user import User
from models.image import Image

images_blueprint = Blueprint('images',
                                __name__,
                                template_folder='templates/images')




# ====== Functions ======

# Hybrid property
# @hybrid_property
# def profile_image_url(self):
#   return AWS_S3_DOMAIN + self.current_user.profile_picture

# @images_blueprint.route('/donations/<id>/new', methods=['GET'])
# def donate(id):
#     return render_template('braintree.html')


@images_blueprint.route('/post', methods=['GET','POST'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    
    if request.method == 'POST':
        if "post-image" not in request.files:
            flash(f"No post-image key in request.files", "warning")
            return redirect(url_for('users.show', username=current_user.username))
           

        file    = request.files.get("post-image")

        if file.filename == "":
            flash(f"Please select a file", "warning")
            return redirect(url_for('users.show', username=current_user.username))
            

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file, S3_BUCKET)  
            flash(f"Uploaded!", "success")
            
            new_image = Image(
                URL=str(output),
                user_id=current_user.id
                ).save()
            return redirect(url_for('users.show', image=new_image, username=current_user.username))
        
        else:
            flash('Upload failed', 'danger')
            return redirect("/")
    
         


@images_blueprint.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload_page.html')
 

@images_blueprint.route("/", methods=["POST"])
def upload_file():

	# A | check the request.files object for a user_file key. 
    # (user_file is the name of the file input on our form).
    if "user_file" not in request.files:
        return flash(f"No user_file key in request.files", "warning")

	# B | If the key is in the object, we save it in a variable called file
    file    = request.files.get("user_file")

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C. | check the filename attribute on the object 
    # and if it’s empty, it means the user sumbmitted an empty form
    if file.filename == "":
        return flash(f"Please select a file", "warning")

	# D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, S3_BUCKET)  
        flash(f"Success, your profile photo was updated!", "success")
        
        # We have to run 'update' on model User, NOT 'current_user' that is fixed. 
        # Then we have to pass current user's id (so we know what we are updating).
        # and don't forget to add .execute()
        User.update(profile_picture=str(output)).where(User.id == current_user.id).execute()
        return redirect(url_for('users.show', username=current_user.username))
        
    else:
        flash('Upload failed', 'danger')
        return redirect("/")
        

# UPLOAD POST
# @images_blueprint.route("/", methods=["POST"])
# def upload_post():

#     if "user_file" not in request.files:
#         return flash(f"No user_file key in request.files", "warning")

#     file    = request.files.get("user_file")

#     if file.filename == "":
#         return flash(f"Please select a file", "warning")

#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output   	  = upload_file_to_s3(file, S3_BUCKET)  
#         flash(f"Uploaded!", "success")

#         new_image = Image(
#             URL=str(output),
#             user_id=current_user.id

#         )
#         return redirect(url_for('users.show', image=new_image))
        
#     else:
#         flash('Upload failed', 'danger')
#         return redirect("/")
        

