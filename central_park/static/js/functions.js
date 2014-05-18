// Check if string is a whole number(digits only).
    
function checkform ( form )
{
        var fields_to_check = "";
        if (!is_valid_place(form.place.value)) {fields_to_check += "place name, "};
        if (!is_valid_car_number(form.car_number.value)) {fields_to_check += "car number, "};
        if (!is_valid_cost(form.cost.value)) {fields_to_check += "cost"};
        console.log("cf", form.cost.value, form.cost.value );
        if (fields_to_check != "") {
            alert("You entered not correct information. Please, check next fields: ".concat(fields_to_check));
            return false;
        };
    return true;
};

is_valid_cost = function(value){
    value = $.trim(value);
    console.log(value);
    var isWhole_re  = /^\s*\d{1,3}\s*$/;
    if (String(value).search(isWhole_re) != -1){
        console.log("True");
        return true;
    };
    console.log("False");
    return false;
}

is_valid_place = function(value){
    value = $.trim(value);
    var isWhole_re  = /^\s*\w{1,8}\s*$/;
    if (String(value).search(isWhole_re) != -1){
        return true;
    };
    return false;
}

is_valid_car_number = function(value){
    value = $.trim(value);
    var isWhole_re  = /^\s*\w{3,10}\s*$/;
    if (String(value).search(isWhole_re) != -1){
        return true;
    };
    return false;
}

is_not_empty = function(value){
    if (value){
        return true;
    };
    return false;
};

GetInfo  = function() {
       if (checkform(this))
        {
            var formData = {
                "place":$("#details").val(),
                "car_number":$("#ext_details").val(),
                "cost":$("#amt").val(),
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
                    alert('Server do not respond. Please, try again...')
                },

                });

		return false;
    };
    return true;
};





time_left = function(){
    var cost = $.trim($("#amt").val());
    if (is_valid_cost(cost)){
        var formData = {
            "place": $("#details").val(),
            "car_number": $("#ext_details").val(),
            "cost": cost,
        }; 
        $.ajax({
                    url:'/en/time_left',
                    type:'POST',
                    data: JSON.stringify(formData, null),
                    contentType: "application/json",
                    success: function (response)
                    {
                        document.getElementById("parkingTimeLeft").innerHTML = 
                            '<label> Parking till: ' + response["time_left"] + '</label>';
                    },

                    error: function (st)
                    {
                        document.getElementById("parkingTimeLeft").innerHTML =
                            '<label> Error on server! Please, check parking place name! </label>';
                    },
                })
    } else {
        document.getElementById("parkingTimeLeft").innerHTML = 
                            '<label> Please, insert correct cost! </label>';
    }
};




place_request = function(){
    var place = $.trim($("#details").val());
    
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
                        '<label> 1st hour: '+response["first_hour_tariff"]+'hrn/h, 2nd: '+response["second_hour_tariff"]+'hrn/h</label>';
                } else { 
                    document.getElementById("placeValid").innerHTML = 
                        '<label>No such parking place. <br> Please enter place name correctly!</label>';
                };
            },
            error: function (request)
            {
                document.getElementById("placeValid").innerHTML =
                        '<label>No such parking place. <br> Please enter place name correctly!</label>';
            },

        });
    } else {
         document.getElementById("placeValid").innerHTML = 
                        '<label>Please enter place name correctly</label>';
    };
};