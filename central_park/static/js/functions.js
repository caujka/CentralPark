// Check if string is a whole number(digits only).
    var isWhole_re  = /^\s*\d+\s*$/;
    function isWhole (s) {
        return String(s).search (isWhole_re) != -1;
    };
    
    function checkform ( form )
    {
  // ** START **
        if (form.lot_id.value == "" || form.place_id.value == "" || form.car_number.value == "" || form.car_number.value == "" || isWhole(form.cost.value) != true) {
            alert( "Please enter valid data" );
            // form.username.focus();
            return false ;
        }
  // ** END **
        return true ;
    };

    GetInfo  = function() {
        if (checkform(this)){
        var formData = {
            "lot_id":$("#lot_id").val(),
            "place_id":$("#place_id").val(),
            "car_number":$("#car_number").val(),
            "cost":$("#cost").val(),
            };
        console.log(formData);
        $.ajax({
            url:'http://localhost:5000/payment',
            type:'POST',
            data: JSON.stringify(formData, null, '\t'),
            contentType: "application/json",
            success: function (response)
            {
                var myDiv = $('#result'); // The place where you want to insert the template
                myDiv.html(response);
            },

            error: function (request)
            {
            
            },

            });

		return false;
    };
    return true;
    };

place_request = function(){
    var formData = {"lot_id":$("#lot_id").val()};
    console.log(formData);
    $.ajax({
        url:'/dynamic_select',
        type:'POST',
        data: JSON.stringify(formData, null, '\t'),
        contentType: "application/json",
        success: function (response)
        {
            var list = response["response"];
            var places = ""
            for (var i=0; i<list.length; i++){
                places += '<option value=' + list[i] + '>' + list[i] + '</option>'
            };
            document.getElementById('place_id').innerHTML = places;

        },
        error: function (request)
        {
            alert('Error!!!')
        },

    });


};