@auth.requires_signature()
@auth.requires_login()
def insert_movie():
    #if request.vars.movieID == -1:
    # in this function, we take the data that the JavaScript sent us and insert it into the database!
    new_movie_id = db.movies.insert(
        user_email= auth.user.email,
        title=request.vars.title,
        description=request.vars.description,
        rating=request.vars.rating
    )
    """
    else:
        q = (((db.movies.id == request.vars.id) & (db.movies.user_email == auth.user.email)))
        db(q).delete()
        new_movie_id = db.movies.insert(
            user_email=auth.user.email,
            title=request.vars.title,
            description=request.vars.description,
            rating=request.vars.rating
        )
    """
    # JavaScript needs the id of the movie that was just created so that it can pass it to the clickThumbs function
    return response.json(dict(new_movie_id=new_movie_id))

 #backup of get_all_movies
def get_all_moviesSave():
    movies = db(db.movies).select() # this asks the database for all entries in the movies table
    thumbs = db(db.thumbs).select() # get all thumbs from the database
    movie_list = []

    for movie in movies:
        movie_to_send = dict(
            id=movie.id,
            title=movie.title,
            description=movie.description,
            rating=movie.rating,
            thumb=None # for now, set the thumb state to None, it will possibly get reassigned later
        )
        # if there is a thumb associated with this movie, change the thumb value to it's actual state
        for thumb in thumbs:
            if thumb.movie_id == movie.id:
                movie_to_send['thumb'] = thumb.thumb_state
        movie_list.append(movie_to_send)

    return response.json(dict(movies=movie_list)) # return all movies as a JSON object back to JavaScript

@auth.requires_login()
def get_all_movies():
    movies = db(db.movies).select() # this asks the database for all entries in the movies table
    thumbs = db(db.thumbs).select() # get all thumbs from the database
    movie_list = []

    for movie in movies:
        movie_to_send = dict(
            id=movie.id,
            title=movie.title,
            description=movie.description,
            rating=movie.rating,
            thumb=None, # for now, set the thumb state to None, it will possibly get reassigned later
            count=0,
            user = movie.user_email
        )

        # if there is a thumb associated with this movie, change the thumb value to it's actual state
        movie_to_send['count'] = 0
        for thumb in thumbs:
            thumb_state = thumb.thumb_state
            thumb_value = 0  # default state
            if thumb_state == "u":
                thumb_value = 1  # up rating
            elif thumb_state == "d":
                thumb_value = -1  # down rating

            if thumb.movie_id == movie.id:
                # count all user's rating in the count so don't bother to check thumb.user_email
                movie_to_send['count'] += thumb_value
                if thumb.user_email == auth.user.email:
                    # only get thumb for currently logged in user
                    movie_to_send['thumb'] = thumb.thumb_state

        movie_list.append(movie_to_send)

    return response.json(dict(movies=movie_list)) # return all movies as a JSON object back to JavaScript


@auth.requires_login()
def get_all_plans():
    q = (db.userPlan.user_email == auth.user.email) #gets all the userPlan for the current user
    plans = db(q).select() # this asks the database for ALL entries in the userPlan table
    plan_list = []

    for plan in plans:
        plan_to_send = dict(
            id=plan.id,
            name = plan.planName,
            user = plan.user_email
        )
        plan_list.append(plan_to_send)

    return response.json(dict(plans=plan_list)) # return all movies as a JSON object back to JavaScript as variable called plans


@auth.requires_login()
def get_all_workouts():
    q = (db.userWorkout.user_email == auth.user.email)  # gets all the userPlan for the current user
    workouts = db(q).select()  # this asks the database for ALL entries in the userPlan table
    workouts_list = []

    for workout in workouts:
        workouts_to_send = dict(
            id=workout.id,
            user=workout.user_email,
            dayOfWeek_id =workout.dayOfWeek_id,
            userPlan_id = workout.userPlan_id,
            workout_id = workout.workout_id,
            workoutName = workout.workoutName,
            workoutText = workout.workoutText,
            workoutLink = workout.workoutLink,
        )
        workouts_list.append(workouts_to_send)

    return response.json(
        dict(workouts=workouts_list))  # return all movies as a JSON object back to JavaScript as variable called workoutss


@auth.requires_login()
def get_all_replies():
    replies = db(db.replies).select() # this asks the database for all entries in the replies table
    reply_list = []

    for reply in replies:
        reply_to_send = dict(
            id=reply.id,
            movieID = reply.movie_id,
            reply=reply.reply,
            user = reply.user_email
        )
        reply_list.append(reply_to_send)

    return response.json(dict(replies=reply_list)) # return all movies as a JSON object back to JavaScript

def get_thumb_counts():
    thumbs = db(db.thumbs).select()
    movie_thumb_counts = {}
    for thumb in thumbs:
        movie_id = thumb.movie_id
        thumb_state = thumb.thumb_state
        thumb_value = 0 # default state
        if thumb_state == "u":
            thumb_value = 1 #up rating
        elif thumb_state == "d":
            thumb_value = -1 #down rating
        if movie_id in movie_thumb_counts:
            movie_thumb_counts[movie_id] += thumb_value
        else:
            movie_thumb_counts[movie_id] = thumb_value
    return response.json(movie_thumb_counts)



@auth.requires_login()
def getcurUser():
    return response.json(dict(curUser=auth.user.email))

@auth.requires_signature()
def set_thumb():
    db.thumbs.update_or_insert(((db.thumbs.movie_id == request.vars.id) & (db.thumbs.user_email == auth.user.email)),
        user_email=auth.user.email,
        movie_id=request.vars.id,
        thumb_state=request.vars.thumb_state
    )
    # we don't have to send back the thumb's id because our JavaScript will never need to use it
    # instead, we will just respond with a success mesage.
    return "thumb updated!"

@auth.requires_login()
@auth.requires_signature()
def insert_reply():
    new_reply_id = db.replies.insert(
        user_email=auth.user.email,
        movie_id=request.vars.movieID,
        reply=request.vars.reply
    )


def add_user_workout(user_plan_id,day_Of_Week, workout_id, workout_name, workout_text, workout_link):
    new_user_workout_id = db.userWorkout.insert(
        userPlan_id= user_plan_id,
        dayOfWeek_id = day_Of_Week,
        workout_id = workout_id,
        workoutName = workout_name,
        workoutText = workout_text,
        workoutLink = workout_link
    )


def func1(x):
    return x*x

def Save_Plan():
    def add_user_workout(user_plan_id, day_Of_Week, workout_id, workout_name, workout_text, workout_link):
        new_user_workout_id = db.userWorkout.insert(
            userPlan_id=user_plan_id,
            dayOfWeek_id=day_Of_Week,
            workout_id=workout_id,
            workoutName=workout_name,
            workoutText=workout_text,
            workoutLink=workout_link
        )

    day_Of_Week = 1
    day_Of_Week2 = 2


    """
    db.userPlan.drop()
    db.userAnswers.drop()
    db.userWorkout.drop()
    """

    new_user_plan_id= db.userPlan.insert(
        user_email=auth.user.email,
        planName = request.vars.planname
    )


    new_user_answers_id = db.userAnswers.insert(
        userPlan_id = new_user_plan_id,
        question_id = 2,
        answer_id = request.vars.weight
    )

    new_user_answers_id = db.userAnswers.insert(
        userPlan_id=new_user_plan_id,
        question_id=2,
        answer_id=request.vars.weight
    )

    new_user_answers_id = db.userAnswers.insert(
        userPlan_id=new_user_plan_id,
        question_id=3,
        answer_id=request.vars.goals
    )

    new_user_answers_id = db.userAnswers.insert(
        userPlan_id=new_user_plan_id,
        question_id=4,
        answer_id=request.vars.type
    )

    new_user_answers_id = db.userAnswers.insert(
        userPlan_id=new_user_plan_id,
        question_id=5,
        answer_id=request.vars.freq
    )
    func1(2)
    #add_user_workout(new_user_plan_id, day_Of_Week, 1, "bStairmaster", "for 5 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"):

    new_user_workout_id = db.userWorkout.insert(
        userPlan_id=new_user_plan_id,
        dayOfWeek_id=day_Of_Week,
        workout_id=1,
        workoutName="Jump Rope",
        workoutText="for 3 minutes",
        workoutLink = "https://www.bodybuilding.com/exercises/rope-jumping"
    )

    new_user_workout_id = db.userWorkout.insert(
        userPlan_id=new_user_plan_id,
        dayOfWeek_id=day_Of_Week,
        workout_id=1,
        workoutName="Jumping Jacks",
        workoutText="for 3 minutes",
        workoutLink = "https://www.bodybuilding.com/exercises/rope-jumping"
    )

    new_user_workout_id = db.userWorkout.insert(
        userPlan_id=new_user_plan_id,
        dayOfWeek_id=day_Of_Week,
        workout_id=1,
        workoutName="Run",
        workoutText="for 10 minutes",
        workoutLink="https://www.bodybuilding.com/exercises/rope-jumping"
    )

    new_user_workout_id = db.userWorkout.insert(
        userPlan_id=new_user_plan_id,
        dayOfWeek_id=day_Of_Week2,
        workout_id=1,
        workoutName="Walk",
        workoutText="for 10 minutes",
        workoutLink="https://www.bodybuilding.com/exercises/rope-jumping"
    )

    return response.json(dict(plan_id = new_user_plan_id))
    #return new_user_plan_id

