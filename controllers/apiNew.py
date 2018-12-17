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





def Save_Plan():
    day_Of_Week = 1
    day_Of_Week2 = 2

    """
    db.userPlan.drop()
    db.userAnswers.drop()
    db.userWorkout.drop()
    """


    workoutTypeIds=[1,2,3]
    workoutsTypes=["Benchpress","Jump Rope","Run"]
    dayOfWeekIds=[0,1,2,3,4,5,6]
    daysOfWeek=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    #  Add workouts here for each combination
    # [3,1,"Benchpress freq1, goal1, type1","3 sets of 10","https://www.bodybuilding.com/exercises/rope-jumping"],
    #  DayOfWeekId  3=Wed
    #    WorkoutId from above 1=Benchpress
    #      WorkoutName: String such as "Benchpress"
    #                                       WorkoutText: String such as "20 minutes"
    #                                                      WorkoutLink: String link to the bodybuilding site
    workouts=[
                [
                    [
                        [   #freq1, 1-1  Monday, Cardio, Lose Weight
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                            [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq1, 1-2  Monday, Cardio, Gain Muscle
                             [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                             [1,2,"Jump Squat","for 3 minutes","https://www.bodybuilding.com/exercises/freehand-jump-squat"],
                             [1,3,"Bodyweight Squat","3 sets 8 reps","https://www.bodybuilding.com/exercises/bodyweight-squat"],
                             [1,4,"Goblet Squat", "3 minutes 8 reps", "https://www.bodybuilding.com/exercises/goblet-squat"],
                             [1,5,"Russian Twist", "for 2 minutes","https://www.bodybuilding.com/exercises/russian-twist"],
                             [1,6,"Crunches", "30 reps","https://www.bodybuilding.com/exercises/crunches"],
                             [1,7,"Spider-Crawl", "30 reps","https://www.bodybuilding.com/exercises/spider-crawl"],
                             [1,8,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                             [1,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq1, 1-3  Monday, Cardio, Be Fit
                             [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                             [1,2,"Jump Squat","for 3 minutes","https://www.bodybuilding.com/exercises/freehand-jump-squat"],
                             [1,3,"Bodyweight Squat","3 sets 8 reps","https://www.bodybuilding.com/exercises/bodyweight-squat"],
                             [1,4,"Jumping Jacks", "for 3 minutes", "https://www.bodybuilding.com/exercises/jumping-jacks"],
                             [1,5,"Russian Twist", "for 2 minutes","https://www.bodybuilding.com/exercises/russian-twist"],
                             [1,6,"Crunches", "30 reps","https://www.bodybuilding.com/exercises/crunches"],
                             [1,7,"Stairmaster", "for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                             [1,8,"Spider-Crawl", "30 reps","https://www.bodybuilding.com/exercises/spider-crawl"],
                             [1,9,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                             [1,10,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq1, 2-1  Monday, Weightlifting, Lose Weight
                              [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                              [1,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                              [1,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                              [1,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                              [1,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                              [1,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                              [1,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                              [1,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                        ],
                        [    #freq1, 2-2  Monday, Weightlifting, Gain Muscle
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [1,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [1,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                        ],
                        [     #freq1, 2-3  Monday, Weightlifting, Be Fit
                                [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [1,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [1,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                [1,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                [1,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [1,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [1,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [1,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                        ],
                        [     #freq1, 3-1  Monday, A Mix, Lose Weight
                                [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [1,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [1,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [1,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [1,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [     #freq1, 3-2  Monday, A Mix, Gain Muscle
                                [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [     #freq1, 3-3  Monday, A Mix, Be Fit
                                [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [1,2,"Lat Pulldown","4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [1,3,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [1,4,"Barbell Curls", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [1,5,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ]
                    ]
                ],
                [
                    [
                        [   #freq2, 1-1  Monday + Friday, Cardio, Lose Weight
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                            [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq2, 1-2  Monday + Friday, Cardio, Gain Muscle
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Jump Squat","for 3 minutes","https://www.bodybuilding.com/exercises/freehand-jump-squat"],
                            [1,3,"Bodyweight Squat","3 sets 8 reps","https://www.bodybuilding.com/exercises/bodyweight-squat"],
                            [1,4,"Goblet Squat", "3 minutes 8 reps", "https://www.bodybuilding.com/exercises/goblet-squat"],
                            [1,5,"Russian Twist", "for 2 minutes","https://www.bodybuilding.com/exercises/russian-twist"],
                            [1,6,"Crunches", "30 reps","https://www.bodybuilding.com/exercises/crunches"],
                            [1,7,"Spider-Crawl", "30 reps","https://www.bodybuilding.com/exercises/spider-crawl"],
                            [1,8,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                            [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq2, 1-3  Monday + Friday, Cardio, Be Fit
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Jump Squat","for 3 minutes","https://www.bodybuilding.com/exercises/freehand-jump-squat"],
                            [1,3,"Bodyweight Squat","3 sets 8 reps","https://www.bodybuilding.com/exercises/bodyweight-squat"],
                            [1,4,"Jumping Jacks", "for 3 minutes", "https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,5,"Russian Twist", "for 2 minutes","https://www.bodybuilding.com/exercises/russian-twist"],
                            [1,6,"Crunches", "30 reps","https://www.bodybuilding.com/exercises/crunches"],
                            [1,7,"Stairmaster", "for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,8,"Spider-Crawl", "30 reps","https://www.bodybuilding.com/exercises/spider-crawl"],
                            [1,9,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,10,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [5,5,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                            [5,6,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [   #freq2, 2-1  Monday + Friday, Weightlifting: Lose Weight:
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                            [1,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                            [1,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,3,"Dumbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                            [5,4,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,5,"Dips", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,6,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,7,"Tricep Pulldown", "4 sets 12 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"]
                        ],
                        [   #freq2, 2-2  Monday + Friday, Weightlifting: Gain Muscle:
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                            [1,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                            [1,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,3,"Dumbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                            [5,4,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,5,"Dips", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,6,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"]
                        ],
                        [   #freq2, 2-3  Monday + Friday, Weightlifting: Be Fit:
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                            [1,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                            [1,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,3,"Dumbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                            [5,4,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,5,"Dips", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,6,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"]
                        ],
                        [  #freq2, 3-1  Monday + Friday, A mix: lose weight
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,3,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,4,"Dips","4 sets 10 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,5,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [  #freq2, 3-2  Monday + Friday, A mix: gain muscle
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"]
                        ],
                        [
                           #freq2, 3-3  Monday + Friday, A mix: Be Fit
                            [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [1,2,"Lat Pulldown","4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                            [1,3,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                            [1,4,"Barbell Curls", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                            [1,5,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                            [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                            [5,2,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                            [5,3,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                            [5,4,"Dips","4 sets 8 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                            [5,5,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                            [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"]
                         ]
                    ],
                    [
                        [   #freq3, 1-1  Monday + Friday + Wednesday, Cardio, Lose Weight
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                            [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #WEDNESDAY BEGIN
                            [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                            [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                            [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                            [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                         ],
                         [  #freq3, 1-2  Monday + Friday + Wednesday, Cardio, Gain Muscle:
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                            [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #WEDNESDAY BEGIN
                            [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                            [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                            [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                            [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                          ],
                          [  #freq3, 1-3  Monday + Friday + Wednesday, Cardio, Be Fit:
                            [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                            [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                            [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                            [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #FRIDAY BEGIN
                            [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [5,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                            [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                            [5,4,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                            [5,5,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                            [5,6,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [5,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            #WEDNESDAY BEGIN
                            [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                            [3,2,"Butt Kick","for 3 minutes","https://www.bodybuilding.com/exercises/butt-Kicks"],
                            [3,3,"Hip Circles","10 reps for each leg","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                            [3,4,"Butt Lift","5 reps 3 sets","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                            [3,5,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                            [3,6,"Knee Raise", "10 reps for each leg", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                            [3,7,"Leg Raises", "10 reps for each leg", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                            [3,8,"Knee Tuck", "10 reps 3 sets","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                            [3,9,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                            [3,10,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                           ],
                           [ #freq3, 2-1  Monday + Friday + Wednesday, Weightlifting: Lose Weight:
                             [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                             [1,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                             [1,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                             [1,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                             [1,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                             [1,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                             [1,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                             [1,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                             #FRIDAY BEGIN
                             [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                             [5,2,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                             [5,3,"Dumbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                             [5,4,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                             [5,5,"Dips", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                             [5,6,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                             [5,7,"Tricep Pulldown", "4 sets 12 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                             #WEDNESDAY BEGIN
                             [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                             [3,2,"One Arm Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                             [3,3,"Reverse Fly","3 sets 15 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                             [3,4,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                             [3,5,"Dumbell Shrug", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                             [3,6,"Face Pull", "3 sets 15 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                             [3,7,"Cable Lift", "3 sets 20 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                             [3,8,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"]
                            ],
                            [ #freq3, 2-2  Monday + Friday + Wednesday, Weightlifting: Gain Muscle:
                              [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                              [1,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                              [1,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                              [1,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                              [1,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                              [1,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                              [1,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                              [1,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                              #FRIDAY BEGIN
                              [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                              [5,2,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                              [5,3,"Dumbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                              [5,4,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                              [5,5,"Dips", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                              [5,6,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                              [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                              #WEDNESDAY BEGIN
                              [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                              [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                              [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                              [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                              [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                              [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                              [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                              [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"]
                             ],
                             [ #freq3, 2-3  Monday + Friday + Wednesday, Weightlifting: Be Fit:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [1,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [1,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,3,"Dumbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                               [5,4,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,5,"Dips", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,6,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                               [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                               [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                               [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                               [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"]
                             ],
                             [ #freq3, 3-1  Monday + Friday + Wednesday, Weightlifting: Lose Weight:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 10 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 15 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 20 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                             ],
                             [ #freq3, 3-2  Monday + Friday + Wednesday, Weightlifting: Gain Muscle:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 8 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 10 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                             ],
                             [ #freq3, 3-3  Monday + Friday + Wednesday, Weightlifting: Be Fit
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 8 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 12 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 15 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 15 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                             ],
                         ],
                         [
                            [ #freq4, 1-1  Monday + Friday + Wednesday + Saturday, Cardio, Lose Weight
                               [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                               [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                               [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                               [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                               [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                               [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                            ],
                            [  #freq4, 1-2  Monday + Friday + Wednesday + Saturday, Cardio, Gain Muscle:
                               [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                               [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                               [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                               [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                               [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                               [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                            ],
                            [   #freq4, 1-3  Monday + Friday + Wednesday + Saturday, Cardio, Be Fit:
                               [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [5,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                               [5,4,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                               [5,5,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                               [5,6,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [3,2,"Butt Kick","for 3 minutes","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Hip Circles","10 reps for each leg","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                               [3,4,"Butt Lift","5 reps 3 sets","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                               [3,5,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,6,"Knee Raise", "10 reps for each leg", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                               [3,7,"Leg Raises", "10 reps for each leg", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                               [3,8,"Knee Tuck", "10 reps 3 sets","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                               [3,9,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,10,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                               [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                               [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                               [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                               [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                            ],
                            [  #freq3, 2-1  Monday + Friday + Wednesday + Saturday, Weightlifting: Lose Weight:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [1,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [1,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,3,"Dumbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                               [5,4,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,5,"Dips", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,6,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,7,"Tricep Pulldown", "4 sets 12 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"One Arm Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Reverse Fly","3 sets 15 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                               [3,4,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                               [3,5,"Dumbell Shrug", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,6,"Face Pull", "3 sets 15 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                               [3,7,"Cable Lift", "3 sets 20 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                               [3,8,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [6,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [6,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                            ],
                            [  #freq4, 2-2  Monday + Friday + Wednesday + Saturday, Weightlifting: Gain Muscle:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [1,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [1,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,3,"Dumbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                               [5,4,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,5,"Dips", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,6,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                               [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                               [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                               [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                               [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [6,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [6,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                            ],
                            [  #freq4, 2-3  Monday + Friday + Wednesday + Saturday, Weightlifting: Be Fit:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [1,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [1,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,3,"Dumbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                               [5,4,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,5,"Dips", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,6,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                               [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                               [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                               [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                               [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                               [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                               [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                               [6,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                               [6,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"]
                            ],
                            [  #freq4, 3-1  Monday + Friday + Wednesday + Saturday, Weightlifting: Lose Weight:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 10 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 15 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 20 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                            ],
                            [  #freq4, 3-2  Monday + Friday + Wednesday + Saturday, Weightlifting: Gain Muscle:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 8 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 10 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            ],
                            [  #freq4, 3-3  Monday + Friday + Wednesday + Saturday, Weightlifting: Be Fit:
                               [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [1,2,"Lat Pulldown","4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [1,3,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [1,4,"Barbell Curls", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [1,5,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #FRIDAY BEGIN
                               [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [5,2,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                               [5,3,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                               [5,4,"Dips","4 sets 8 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                               [5,5,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                               [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                               [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #WEDNESDAY BEGIN
                               [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [3,2,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                               [3,3,"Dumbell Shrug","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                               [3,4,"Face Pull","3 sets 12 reps","https://www.bodybuilding.com/exercises/face-pull"],
                               [3,5,"Cable Lift", "3 sets 15 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                               [3,6,"Cable Crunch", "3 sets 15 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                               [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                               [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               #SATURDAY BEGIN
                               [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                               [6,2,"Lat Pulldown","4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                               [6,3,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                               [6,4,"Barbell Curls", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                               [6,5,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                               [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                               [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                               [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                            ]
                        ],
                        [
                            [  #freq5, 1-1  Monday + Friday + Wednesday + Saturday + Tuesday, Cardio, Lose Weight
                                [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #FRIDAY BEGIN
                                [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #WEDNESDAY BEGIN
                                [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                                [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #SATURDAY BEGIN
                                [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #TUESDAY BEGIN
                                [2,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [2,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [2,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [2,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [2,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [2,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            ],
                            [   #freq5, 1-2  Monday + Friday + Wednesday + Saturday + Tuesday, Cardio, Gain Muscle:
                                [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #FRIDAY BEGIN
                                [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [5,2,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [5,4,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [5,5,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [5,6,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #WEDNESDAY BEGIN
                                [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [3,2,"Butt Kick","for 50 feet","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                [3,3,"Frog Jump","for 50 feet","https://www.bodybuilding.com/exercises/frog-hops"],
                                [3,4,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                [3,5,"Speed Skipping", "for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [3,6,"High Knee Jog", "for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [3,7,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [3,8,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #SATURDAY BEGIN
                                [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #TUESDAY BEGIN
                                [2,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [2,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [2,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [2,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [2,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [2,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [2,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            ],
                            [   #freq5, 1-3  Monday + Friday + Wednesday + Saturday + Tuesday, Cardio, Be Fit:
                                [1,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [1,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [1,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [1,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [1,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [1,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [1,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #FRIDAY BEGIN
                                [5,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [5,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                                [5,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [5,4,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [5,5,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                                [5,6,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [5,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #WEDNESDAY BEGIN
                                [3,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [3,2,"Butt Kick","for 3 minutes","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                [3,3,"Hip Circles","10 reps for each leg","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                                [3,4,"Butt Lift","5 reps 3 sets","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                                [3,5,"Lunges", "for 50 feet", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                [3,6,"Knee Raise", "10 reps for each leg", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                                [3,7,"Leg Raises", "10 reps for each leg", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                                [3,8,"Knee Tuck", "10 reps 3 sets","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                                [3,9,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [3,10,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                #SATURDAY BEGIN
                                [6,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [6,2,"Stairmaster","for 10 minutes","https://www.bodybuilding.com/exercises/stairmaster"],
                                [6,3,"Jumping Jacks","for 3 minutes","https://www.bodybuilding.com/exercises/jumping-jacks"],
                                [6,4,"Jump Rope", "for 3 minutes", "https://www.bodybuilding.com/exercises/rope-jumping"],
                                [6,5,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                [6,6,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [6,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"]
                                #TUESDAY BEGIN
                                [2,1,"Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.bodybuilding.com/content/5-stretches-every-lifter-needs-to-do.html"],
                                [2,2,"Lunges","10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                                [2,3,"High Knee Jog","for 50 feet","https://www.bodybuilding.com/exercises/high-knee-jog"],
                                [2,4,"Speed Skipping","for 100 feet","https://www.bodybuilding.com/exercises/fast-skipping"],
                                [2,5,"Bodyweight Squat", "3 sets 8 reps", "https://www.bodybuilding.com/exercises/bodyweight-squat"],
                                [2,6,"Run", "for 15 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                [2,7,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                            ],
                            [   #freq5, 2-1  Monday + Friday + Wednesday + Saturday + Tuesday,
                                [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [1,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [1,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                [1,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                [1,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [1,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [1,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [1,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                #FRIDAY BEGIN
                                [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [5,2,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                [5,3,"Dumbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                [5,4,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                [5,5,"Dips", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                [5,6,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                [5,7,"Tricep Pulldown", "4 sets 12 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                                #WEDNESDAY BEGIN
                                [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [3,2,"One Arm Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                [3,3,"Reverse Fly","3 sets 15 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                                [3,4,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                                [3,5,"Dumbell Shrug", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                [3,6,"Face Pull", "3 sets 15 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                                [3,7,"Cable Lift", "3 sets 20 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                                [3,8,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                                #SATURDAY BEGIN
                                [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [6,2,"Barbell Rows","4 sets 10 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                [6,3,"T-Bar Row","4 sets 10 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                [6,4,"Hyperextensions", "4 sets 15 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                [6,5,"Lat Pulldown", "4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                [6,6,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                [6,7,"Barbell Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                [6,8,"Spider Curl", "4 sets 12 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                #TUESDAY BEGIN
                                [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                [2,2,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                [2,3,"Dumbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                [2,4,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                [2,5,"Dips", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                [2,6,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                [2,7,"Tricep Pulldown", "4 sets 12 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"]
                            ],
                            [    #freq5, 2-2  Monday + Friday + Wednesday + Saturday + Tuesday,
                                 [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [1,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [1,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                 [1,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                 [1,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [1,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [1,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [1,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                 #FRIDAY BEGIN
                                 [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [5,2,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [5,3,"Dumbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                 [5,4,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [5,5,"Dips", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [5,6,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                                 #WEDNESDAY BEGIN
                                 [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                 [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                                 [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                                 [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                 [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                                 [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                                 [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                                 #SATURDAY BEGIN
                                 [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [6,2,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [6,3,"T-Bar Row","4 sets 6 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                 [6,4,"Hyperextensions", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                 [6,5,"Lat Pulldown", "4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [6,6,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [6,7,"Barbell Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [6,8,"Spider Curl", "4 sets 6 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                 #TUESDAY BEGIN
                                 [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [2,2,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [2,3,"Dumbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                 [2,4,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [2,5,"Dips", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [2,6,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [2,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"]
                            ],
                            [    #freq5, 2-3  Monday + Friday + Wednesday + Saturday + Tuesday,
                                 [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [1,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [1,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                 [1,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                 [1,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [1,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [1,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [1,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                 #FRIDAY BEGIN
                                 [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [5,2,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [5,3,"Dumbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                 [5,4,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [5,5,"Dips", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [5,6,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [5,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                                 #WEDNESDAY BEGIN
                                 [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [3,2,"One Arm Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/butt-Kicks"],
                                 [3,3,"Reverse Fly","3 sets 8 reps","https://www.bodybuilding.com/exercises/hip-circles-prone"],
                                 [3,4,"Seated Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/butt-lift-bridge"],
                                 [3,5,"Dumbell Shrug", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/bodyweight-walking-lunge"],
                                 [3,6,"Face Pull", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/step-up-with-knee-raise"],
                                 [3,7,"Cable Lift", "3 sets 10 reps", "https://www.bodybuilding.com/exercises/front-leg-raises"],
                                 [3,8,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/knee-tuck-jump"],
                                 #SATURDAY BEGIN
                                 [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [6,2,"Barbell Rows","4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [6,3,"T-Bar Row","4 sets 8 reps","https://www.bodybuilding.com/exercises/t-bar-row-with-handle"],
                                 [6,4,"Hyperextensions", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/hyperextensions-back-extensions"],
                                 [6,5,"Lat Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [6,6,"Incline Hammer Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [6,7,"Barbell Curls", "4 sets 8 reps","https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [6,8,"Spider Curl", "4 sets 8 reps","https://www.bodybuilding.com/exercises/spider-curl"],
                                 #TUESDAY BEGIN
                                 [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [2,2,"Incline Dumbell Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [2,3,"Dumbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/dumbbell-bench-press"],
                                 [2,4,"Barbell Bench Press","4 sets 8 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [2,5,"Dips", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [2,6,"Triceps Extension", "4 sets 8 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [2,7,"Tricep Pulldown", "4 sets 8 reps","https://www.bodybuilding.com/exercises/reverse-grip-triceps-pushdown"],
                            ],
                            [    #freq5, 3-1  Monday + Friday + Wednesday + Saturday + Tuesday,
                                 [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [1,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [1,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [1,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [1,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #FRIDAY BEGIN
                                 [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [5,2,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [5,3,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [5,4,"Dips","4 sets 10 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [5,5,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #WEDNESDAY BEGIN
                                 [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [3,2,"Seated Dumbell Press","4 sets 12 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                                 [3,3,"Dumbell Shrug","4 sets 10 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                                 [3,4,"Face Pull","3 sets 15 reps","https://www.bodybuilding.com/exercises/face-pull"],
                                 [3,5,"Cable Lift", "3 sets 20 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                                 [3,6,"Cable Crunch", "3 sets 20 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                                 [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                                 [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #SATURDAY BEGIN
                                 [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [6,2,"Lat Pulldown","4 sets 10 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [6,3,"Barbell Rows","4 sets 15 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [6,4,"Barbell Curls", "4 sets 12 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [6,5,"Incline Hammer Curls", "4 sets 12 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #TUESDAY BEGIN
                                 [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [2,2,"Barbell Bench Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [2,3,"Incline Dumbell Press","4 sets 10 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [2,4,"Dips","4 sets 10 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [2,5,"Triceps Extension", "4 sets 10 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [2,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [2,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [2,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],

                            ],
                            [    #freq5, 3-2  Monday + Friday + Wednesday + Saturday + Tuesday,
                                 [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],                                       
                                 [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],                          
                                 [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],                   
                                 [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],                        
                                 [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],                                           
                                 [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],                                           
                                 [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],                                      
                                 #FRIDAY BEGIN                                                                                                                       
                                 [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [5,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],               
                                 [5,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],                      
                                 [5,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],                                         
                                 [5,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],              
                                 [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],                                          
                                 [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],                                          
                                 [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],                                     
                                 #WEDNESDAY BEGIN                                                                                                                    
                                 [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [3,2,"Seated Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],                        
                                 [3,3,"Dumbell Shrug","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],                                      
                                 [3,4,"Face Pull","3 sets 8 reps","https://www.bodybuilding.com/exercises/face-pull"],                                               
                                 [3,5,"Cable Lift", "3 sets 10 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],                                  
                                 [3,6,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/cable-crunch"],                                       
                                 [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],                                        
                                 [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],                                           
                                 [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],                                           
                                 #SATURDAY BEGIN                                                                                                                     
                                 [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [6,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],                                       
                                 [6,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],                          
                                 [6,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],                   
                                 [6,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],                        
                                 [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],                                           
                                 [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],                                           
                                 [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],                                      
                                 #TUESDAY BEGIN
                                 [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [2,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [2,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [2,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [2,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [2,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [2,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [2,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                            ],
                            [    #freq5, 3-3  Monday + Friday + Wednesday + Saturday + Tuesday,
                                 [1,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [1,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [1,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [1,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [1,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [1,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [1,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [1,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #FRIDAY BEGIN
                                 [5,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [5,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [5,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [5,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [5,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [5,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [5,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [5,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #WEDNESDAY BEGIN
                                 [3,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [3,2,"Seated Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/seated-dumbbell-press"],
                                 [3,3,"Dumbell Shrug","4 sets 6 reps","https://www.bodybuilding.com/exercises/dumbbell-shrug"],
                                 [3,4,"Face Pull","3 sets 8 reps","https://www.bodybuilding.com/exercises/face-pull"],
                                 [3,5,"Cable Lift", "3 sets 10 reps","https://www.bodybuilding.com/exercises/standing-cable-lift"],
                                 [3,6,"Cable Crunch", "3 sets 10 reps","https://www.bodybuilding.com/exercises/cable-crunch"],
                                 [3,7,"Lunges", "10 for each leg","https://www.bodybuilding.com/exercises/bodyweight-lunge"],
                                 [3,8,"Run", "for 20 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [3,9,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #SATURDAY BEGIN
                                 [6,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [6,2,"Lat Pulldown","4 sets 6 reps","https://www.bodybuilding.com/exercises/v-bar-pulldown"],
                                 [6,3,"Barbell Rows","4 sets 6 reps","https://www.bodybuilding.com/exercises/reverse-grip-bent-over-rows"],
                                 [6,4,"Barbell Curls", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/wide-grip-standing-barbell-curl"],
                                 [6,5,"Incline Hammer Curls", "4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-hammer-curls"],
                                 [6,6,"Walk", "for 5 minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [6,7,"Run", "for 10 minutes","https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [6,8,"Walk", "for 5 more minutes","https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 #TUESDAY BEGIN
                                 [2,1,"Rotator Cuff Stretch","THE MOST IMPORTANT PART OF EVERY WORKOUT IS STRETCHING","https://www.youtube.com/watch?v=bT8RNbaNd7U"],
                                 [2,2,"Barbell Bench Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/barbell-bench-press-medium-grip"],
                                 [2,3,"Incline Dumbell Press","4 sets 6 reps","https://www.bodybuilding.com/exercises/incline-dumbbell-press"],
                                 [2,4,"Dips","4 sets 6 reps","https://www.bodybuilding.com/exercises/dips-triceps-version"],
                                 [2,5,"Triceps Extension", "4 sets 6 reps", "https://www.bodybuilding.com/exercises/decline-ez-bar-triceps-extension"],
                                 [2,6,"Walk", "for 5 minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],
                                 [2,7,"Run", "for 15 minutes", "https://www.bodybuilding.com/exercises/running-treadmill"],
                                 [2,8,"Walk", "for 5 more minutes", "https://www.bodybuilding.com/exercises/walking-treadmill"],

                            ],
                            [










































                            ],





































                        [   #freq2, goal2, type1
                            [2,1,"Benchpress freq2, goal2, type1","3 sets of 10","https://www.bodybuilding.com/exercises/rope-jumping"],
                            [2,2,"Jumprope freq2, goal2, type1","20 minutes","https://www.bodybuilding.com/exercises/rope-jumping"],
                            [4,3,"Run freq2, goal2, type1","30 minutes","https://www.bodybuilding.com/exercises/rope-jumping"]
                        ],
                        [   #freq2, goal2, type2
                            [2,1,"Benchpress freq2, goal2, type2","3 sets of 10","https://www.bodybuilding.com/exercises/rope-jumping"],
                            [4,3,"Run freq2, goal2, type2","30 minutes","https://www.bodybuilding.com/exercises/rope-jumping"]
                        ]
                    ]
                ]
             ]

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

    for workout in workouts[int(request.vars.freq)-1][int(request.vars.goals)-1][int(request.vars.type)-1]:
        new_user_workout_id = db.userWorkout.insert(
	        userPlan_id=new_user_plan_id,
	        dayOfWeek_id = workout[0],
	        workout_id = workout[1],
	        workoutName = workout[2],
	        workoutText = workout[3],
	        workoutLink = workout[4]
        )
        

    return response.json(dict(plan_id = new_user_plan_id))
