// Check if string is a whole number(digits only).
    var isWhole_re  = /^\s*\d+\s*$/;
    function isWhole (s) {
        return String(s).search (isWhole_re) != -1;
    };
    
    function checkform ( form )
    {
    // ** START **
        if (form.place.value == "" || form.car_number.value == "" || form.cost.value == "" || isWhole(form.cost.value) == true) {
            alert( "Please enter valid data" );
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
            var lang_code = document.URL.split('/')[3];
            $.ajax({
                url:'/'+lang_code+'/payment',
                type:'POST',
                data: JSON.stringify(formData, null),
                contentType: "application/json",
                success: function (st)
                {
                    document.getElementById('result').innerHTML = st;
                },

                error: function (st)
                {
                    alert('error in paying')
                },

                });

		return false;
    };
    return true;
};
is_valid_cost = function(value){
    value = $.trim(value);
    var isWhole_re  = /^\s*\d{1,3}\s*$/;
    if (String(value).search(isWhole_re) != -1){
        return true;
    };
    return false;
}


time_left = function(){
    cost = $.trim($("#cost").val());
    if (is_valid_cost(cost)){
        var formData = {
            "place": $("#place").val(),
            "cost": cost,
        };
        $.ajax({
                    url:'/en/time_left',
                    type:'POST',
                    data: JSON.stringify(formData, null),
                    contentType: "application/json",
                    success: function (time_till)
                    {
                        document.getElementById('time_left_label').className = " ";
                        document.getElementById('time_left_value').innerHTML = time_till;
                    },

                    error: function (st)
                    {
                        
                    },
                })
    }
};

is_not_empty = function(value){
    if (value){
        return true;
    };
    return false;
};


place_request = function(){
    var place = $.trim($("#place").val());
    
    if (is_not_empty(place)){
        var formData = {"place":place};
    
        $.ajax({
            url:'/en/dynamic_select',
            type:'POST',
            data: JSON.stringify(formData, null, '\t'),
            contentType: "application/json",
            success: function (response)
            {
                if (response["response"] == "OK"){
                    document.getElementById("placeValid").innerHTML = 
                        '<img src="../static/images/checked.png" alt="OK!">';
                } else { 
                    document.getElementById("placeValid").innerHTML = 
                        '<label>Please_enter_place_name_correctly</label>';
                };
            },
            error: function (request)
            {
                alert('Error!!!')
            },

        });
    } else {
         document.getElementById("placeValid").innerHTML = 
                        '<label>Please_enter_place_name_correctly</label>';
    };
};