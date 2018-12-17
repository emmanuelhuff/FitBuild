import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None

db.define_table('userPlan',
                Field('user_email', default=get_user_email()),
                Field('planName'),
                )

db.define_table('userAnswers',
                Field('userPlan_id'),
                Field('question_id', "integer"),
                Field('answer_id', "integer"),
                )

db.define_table('userWorkout',
                Field('user_email', default=get_user_email()),
                Field('userPlan_id'),
                Field('dayOfWeek_id', "integer"),
                Field('workout_id', "integer"),
                Field('workoutName', "string"),
                Field('workoutText', "string"),
                Field('workoutLink', "string"),
                )