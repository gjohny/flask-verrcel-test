from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from datetime import datetime
from sqlalchemy import and_

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.calories:
        today_calories = 0
        yesterday = datetime.now().strftime("%Y-%m-%d 00:00:00")
        todays_user_log = db.session.query(Log).filter(
            and_(Log.user_id == current_user.id, Log.date > yesterday)).all()
        for log in todays_user_log:
            today_calories += int(log.food.calories)
        cal_percent = today_calories / current_user.calories * 100
        return render_template("home.html", user=current_user, tc = today_calories, cal_percent = round(cal_percent,1))
    else:
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 
        
    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')

        return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/createfood', methods=['GET','POST'])
@login_required
def createfood():
    if request.method == 'POST':
        food_name = request.form.get('foodname')
        cals = request.form.get('cals')
        protein_ = request.form.get('protein')
        carbs = request.form.get('carbs')
        fat = request.form.get('fat')
        new_food = Food(calories = cals,name=food_name,  protien=protein_,carbs=carbs,fat=fat)
        try:
            db.session.add(new_food)
            db.session.commit()
            m = f"\"{food_name}\" sucessfully added to database!"
            flash(m, category='success')
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        return render_template("createfood.html", user=current_user)
    
@views.route('/logfood', methods=['GET','POST'])
@login_required
def logfood():
    if request.method == 'GET':
        food = Food.query.all()
        return render_template("logfood.html", user=current_user, food=food)
    elif request.method == 'POST':
        food_to_log = request.form.get('food_option')
        servings_ = request.form.get('servings')
        curr_date = datetime.now()
        foodObj = Food.query.filter_by(name = food_to_log).first()
        log_add = Log(food_id=foodObj.id, date = curr_date, 
                    user_id = current_user.id, servings = servings_)
        try:
            db.session.add(log_add)
            db.session.commit()
            m = f"\"{food_to_log}\" was sucessfully logged for {curr_date.strftime("%B-%d ") }"
            flash(m, category='success')
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        return render_template("logfood.html", user=current_user)
    
@views.route('/history')
@login_required
def history():
    log = Log.query.order_by(Log.date.desc()).filter_by(user_id = current_user.id)

    return render_template("history.html", user=current_user, log=log)
    

@views.route('/delete/<int:id>')
def delete(id:int):
    delete_task = Log.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        flash("Log sucessfully deleted")
        return redirect("/history")
    except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    
@views.route('/edit_log/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_log(id:int):
    log = Log.query.get_or_404(id)
    if request.method == 'POST':
        log.servings = request.form['new_serving']
        try:
            db.session.commit()
            m = f"Servings for \"{log.food.name}\" was sucessfully updated to {log.servings}"
            flash(m, category='success')
            return redirect("/history")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:   
        return render_template("edit_log.html", user=current_user, log=log)

@views.route('/goals')
@login_required
def goals():
   return render_template("goals.html", user=current_user)


@views.route('/edit_goals', methods=['GET', 'POST'])
@login_required
def edit_goals():
    pr_color = request.form.get('choose_pr_color')
    if request.method == 'POST':
        # COLOR CHANGE
        pr_color = request.form.get('choose_pr_color')
        print(pr_color)

        #INFO CHANGE
        cu = current_user
        old_list = [cu.first_name, cu.email, cu.height, cu.weight, 
                    cu.calories, cu.protein, cu.carbs, cu.fat]
        new_list = [request.form['new_name'], request.form['new_email'],
                    request.form['new_height'], request.form['new_weight'],
                    request.form['new_calories'], request.form['new_protein'],
                    request.form['new_carbs'], request.form['new_fat']]
        for item in range(len(old_list)):
            if old_list[item] != new_list[item]:
                if item == 0: cu.first_name = new_list[item]
                elif item == 1: cu.email = new_list[item]
                elif item == 2: cu.height = new_list[item]
                elif item == 3: cu.weight = new_list[item]
                elif item == 4: cu.calories = new_list[item]
                elif item == 5: cu.protein = new_list[item]
                elif item == 6: cu.carbs = new_list[item]
                elif item == 7: cu.fat = new_list[item]
        db.session.commit()
        flash('Changes saved sucessfully!')
        return redirect("/goals")
    else:
        return render_template("edit_goals.html", user=current_user, pr_color = pr_color)


    


