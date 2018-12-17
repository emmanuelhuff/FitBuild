var curPlanid = -1;

// this is a global variable that we will use to tell python to submit None
// undefined translates to None in python
// null translates to "", so it is IMPORTANT to use undefined when you want Python to read None
const None = undefined;

// Enumerates an array.
// this will give an _idx attribute to each movie
// the _idx will be assigned 0, 1, 2, 3 ...
var enumerate = function(arr) {
    var k=0; return arr.map(function(e) {
        e._idx = k++;
    });
};

var processMovies = function() {
    enumerate(app.movies);
    app.movies.map(function(movie) {
        // we need to use vue.set here so that the variable responds to changes in the view
        Vue.set(movie, 'hoverThumb', null);
    });
};

var onPageLoad = function() {
    var urlParams = new URLSearchParams(window.location.search);

   $.post(getcurUser,
       function(response) {
           app.curUser = response.curUser;
       }
   );
   var params = {
       curUser: app.curUser,
   };
   $.post(get_all_plans, params,
       function(response) {
           app.plans = response.plans;
           if (app.plans.length > 0) {
               app.selected = app.plans[0].name;
           }

           var i;
           document.getElementById("planName").value = "Plan " + (app.plans.length + 1)
           for (i = 0; i < app.plans.length; i++) {
               if (app.plans[i].id == urlParams.get('planId')) {
                   curPlanid = app.plans[i].id;
                   document.getElementById("planName").value = app.plans[i].name;
               }
           }

           $.post (get_all_answers, { planID: curPlanid},
               function(response) {
                   var i;
                   for (i = 0; i < response.answers.length; i++) {
                       if (response.answers[i].userplan_id == curPlanid) {
                            if (response.answers[i].question_id == 1){
                               document.getElementById("height").value = response.answers[i].answer_id;
                            }
                       }
                       if (response.answers[i].userplan_id == curPlanid) {
                            if (response.answers[i].question_id == 2){
                               document.getElementById("weight").value = response.answers[i].answer_id;
                            }
                       }
                       if (response.answers[i].userplan_id == curPlanid) {
                            if (response.answers[i].question_id == 3){
                               app.pickedType = response.answers[i].answer_id;
                            }
                       }
                       if (response.answers[i].userplan_id == curPlanid) {
                            if (response.answers[i].question_id == 4){
                               app.pickedGoals = response.answers[i].answer_id;
                            }
                       }
                       if (response.answers[i].userplan_id == curPlanid) {
                            if (response.answers[i].question_id == 5){
                               document.getElementById("freq").value = response.answers[i].answer_id;
                            }
                       }
                   }
               }
           );
       }
   );
   $.post(get_all_workouts, params,
       function(response) {
           app.workouts = response.workouts;
       }
   );
};

var insertMovie = function() {
    if ( document.getElementById("movieID").value != -1){
        if(app.movies[document.getElementById("movieID").value].user == app.curUser){
            $.post(delete_post, { id: app.movies[document.getElementById("movieID").value].id}, function(response) {
            });
        } else {
            alert("ERROR: You can't edit other individuals' posts");
            window.location.reload();
        }
    }

    var newMovie = {
        title: app.newMovieTitle,
        description: app.newMovieDescription,
        rating: app.newMovieRating,
        //movieID: app.movies[document.getElementById("movieID").value].id
    };
    $.post(insert_movie, newMovie, function(response) {
        // the server responded with the id number of the new movie in the database. make sure to add this to the
        // new movie object before we add it to the view
        newMovie['id'] = response.new_movie_id;
        newMovie.thumb = null; // the new movie should start off with no thumb value
        newMovie.user = app.curUser;
        newMovie.count = 0;
        app.movies.push(newMovie);
        processMovies(); // need to re-index the movies now that a new one has been added to thea array
    });
    var x = document.getElementById("newPost");
    var y = document.getElementById("insert-movie");
    x.style.display = "block";
    y.style.display = "none";
    window.location.reload();
};

var showPost = function() {
    document.getElementById("movieID").value=-1;
    var x = document.getElementById("newPost");
    var y = document.getElementById("insert-movie");
    x.style.display = "none";
    y.style.display = "block";
};

var handlethumbTap = function(movieIdx, newThumbState) {
    // if we call this function, and the thumb has the same value, we want to de-select it's
    // so we set the new thumb state to null! (this translates to None in python)
    var jsThumbValue = newThumbState;
    var pythonThumbValue = newThumbState
    if(app.movies[movieIdx].thumb == newThumbState) {
        jsThumbValue = null;
        pythonThumbValue = None; // remember, this is a global variable that was declared at the top. None == undefined
    }
    $.post(set_thumb, { id: app.movies[movieIdx].id, thumb_state: pythonThumbValue }, function(response) {
        // after the web2py server responds, we know the thumb as been updated in the database
        // now, we just have to display the new thumb on the screen
        app.movies[movieIdx].thumb = jsThumbValue;
        window.location.reload();
    });

};

var handleThumbMouseOver = function(movieIdx, newHoverThumbState) {
    app.movies[movieIdx].hoverThumb = newHoverThumbState;
};

var handleThumbMouseOut = function(movieIdx) {
    app.movies[movieIdx].hoverThumb = null;
};

var handlePostDelete = function(movieIdx) {
    if(app.movies[movieIdx].user == app.curUser){
        $.post (delete_post, { id: app.movies[movieIdx].id}, function(response) {
        window.location.reload();
        });
    } else {
        alert("ERROR: You can't delete other individuals' posts");
    }
};

var handlePostEdit = function(movieIdx) {
    document.getElementById("postDescriptionBox").value=app.movies[movieIdx].description;
    document.getElementById("movieID").value=movieIdx;

    var x = document.getElementById("newPost");
    var y = document.getElementById("insert-movie");
    x.style.display = "none";
    y.style.display = "block";
};

var handleShowReply = function(movieIdx) {
    if (app.isShowReplies){
        app.isShowReplies = false;
    } else {
        app.isShowReplies = true;
    }
};

var handleAddReply = function(movieIdx) {
    var newReply = {
        reply: app.newReplyDescription,
        movieID: app.movies[movieIdx].id
    };

    $.post(insert_reply, newReply, function(response) {
        // the server responded with the id number of the new movie in the database. make sure to add this to the
        // new movie object before we add it to the view
        newReply['id'] = response.new_reply_id;
        newReply.user = app.curUser;
        app.replies.push(newReply);

    });
};

var handleReplyTap = function(movieIdx) {
    // if we call this function, and the thumb has the same value, we want to de-select it's
    // so we set the new thumb state to null! (this translates to None in python)
    var jsReplyValue = newReplyState;
    var pythonReplyValue = newReplyState;
    if(app.movies[movieIdx].reply == newReplyState) {
        jsReplyValue = null;
        pythonReplyValue = None; // remember, this is a global variable that was declared at the top. None == undefined
    }
    $.post(set_reply, { id: app.movies[movieIdx].id, reply_state: pythonReplyValue }, function(response) {
        // after the web2py server responds, we know the thumb as been updated in the database
        // now, we just have to display the new thumb on the screen
        app.movies[movieIdx].reply = jsReplyValue;
        window.location.reload();
    });
};

var handleShowReply = function(movieIdx) {
    document.getElementById("showReply").style.display = "none";
    document.getElementById("replyForm").style.display = "block";
};

var handlesavePlan = function() {

    var newPlan = {
        planid: curPlanid,
        planname: document.getElementById("planName").value,
        height: document.getElementById("height").value,
        weight: document.getElementById("weight").value,
        freq: document.getElementById("freq").value,
        goals: app.pickedGoals,
        type: app.pickedType,
    };

    $.post(Save_Plan, newPlan, function(response) {
    });
    window.location.href = "account.html"
};

var checkDayOfWeekChanged = function (dayOfWeekId) {
    if (dayOfWeekId != app.prevDay) {
        app.prevDay = dayOfWeekId;
        return true;
    }
    else {
        return false;
    }
};

var handleReplyEdit = function(movieIdx) {
};

var initNewPlan = function () {
    app.prevDay = 8; //invalid value so that first comparison in dayOfWeekChanged will work
    return true;
};

// here, we define the Vue variable. Remember, only the fields defined here (in data and methods) are
// available inside the html
var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        plans: [],
        workouts: [],
        weekdays:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
        prevDays:-1,
        selected: "",
        height: "",
        weight: "",
        freq: "",
        pickedGoals: "",
        pickedType: "",


        newMovieDescription: "",
        newReplyDescription: "",
        movies: [],
        replies: [],
        curUser: "",
        isShowReplies: true,
        isMakeReplies: true
    },
    methods: {
        savePlan: handlesavePlan,
        dayOfWeekChanged: checkDayOfWeekChanged,
        startNewPlan: initNewPlan,

        submitMovie: insertMovie,
        addPost: showPost,
        tapThumb: handlethumbTap,
        hoverOverThumb: handleThumbMouseOver,
        unhoverOverThumb: handleThumbMouseOut,
        deletePost: handlePostDelete,
        editPost: handlePostEdit,
        showReply: handleShowReply,
        addReply: handleAddReply,
        tapReply: handleReplyTap,
        showReplyForm: handleShowReply,
        editReply: handleReplyEdit
    }
});

onPageLoad();