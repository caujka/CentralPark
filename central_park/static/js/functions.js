// Check if string is a whole number(digits only).
    var isWhole_re  = /^\s*\d+\s*$/;
    function isWhole (s) {
        return String(s).search (isWhole_re) != -1;
    };
    
    function checkform ( form )
    {
    // ** START **
        if (form.place.value == "" || form.car_number.value == "" || isWhole(form.cost.value) != true) {
            alert( "Please enter valid data" );
            // form.username.focus();
            return false ;
        }
    // ** END **
        return true ;
    };

GetInfo  = function() {
       if (checkform(this))
        {
            var formData = {
                "place":$("#place").val(),
                "car_number":$("#car_number").val(),
                "cost":$("#cost").val(),
                };
            $.ajax({
                url:'/<lang_code>/payment',
                type:'POST',
                data: JSON.stringify(formData, null),
                contentType: "application/json",
                success: function (st)
                {

                    document.getElementById('result').innerHTML = st;
                    $("#place").val("");
                    $("#car_number").val("");
                    $("#cost").val("");
                },

                error: function (st)
                {
                    alert('erorr')
                },

                });

		return false;
    };
    return true;
};

time_left = function(){
    var formData = {
        "place":$("#place").val(),
        "cost":$("#cost").val(),
    };
    $.ajax({
                url:'/en/time_left',
                type:'POST',
                data: JSON.stringify(formData, null),
                contentType: "application/json",
                success: function (time_till)
                {
                    document.getElementById(time_left_label).className = "";
                    document.getElementById('time_left_value').innerHTML = time_till;
                },

                error: function (st)
                {
                    alert('erorr')
                },
            })
};

place_request = function(){
    var formData = {"place":$("#place").val()};
    $.ajax({
        url:'/en/dynamic_select',
        type:'POST',
        data: JSON.stringify(formData, null, '\t'),
        contentType: "application/json",
        success: function (response)
        {
            if (response["response"] == "OK"){
                document.getElementById("place_not_valid").className = "hidden";
                document.getElementById("place_valid").className = "";
            } else { 
                document.getElementById("place_not_valid").className = ""; 
                document.getElementById("place_valid").className = "hidden";
            }
        },
        error: function (request)
        {
            alert('Error!!!')
        },

    });
};