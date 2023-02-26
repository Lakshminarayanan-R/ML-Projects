
function OnClickEstimatePrice() {
    var carmodel = document.getElementById("uicarmodel");
    var city = document.getElementById("uicity");
    var kms = document.getElementById("uikms");
    var fuel = document.getElementById("uifuel");
    var type = document.getElementById("uicartype");
    var owner = document.getElementById("uiowner");
    var car_life = document.getElementById("uicarlife");
    var estimate_price = document.getElementById("uiEstimatePrice");

    var url = "http://127.0.0.1:5000/car_price_prediction";

    $.post(url,{
        kms: parseInt(kms.value),
        owner: parseInt(owner.value),
        car_life: parseInt(car_life.value),
        car_model: carmodel.value,
        type: type.value,
        fuel: fuel.value,
        city: city.value
    },function(data,status){
        estimate_price.innerHTML = "<h2>" + data.estimated_car_price.toString() + "INR</h2>";
        console.log(status);
    });
}




function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/get_all_model_details"; // Use this if you are NOT using nginx which is first 7 tutorials
    //var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
    $.get(url,function(data, status) {
        console.log("got response for get_location_names request");
        if(data) {
            var carmodel = data.car_model;
            var city = data.city;
            var uicarmodel = document.getElementById("uicarmodel");
            var uicity = document.getElementById("uicity")
            $('#uicarmodel').empty();
            $('#uicarvarient').empty();
            $('#uicity').empty();
            for(var i in carmodel) {
                var opt = new Option(carmodel[i]);
                $('#uicarmodel').append(opt);
            }
            for(var i in city) {
                var opt = new Option(city[i]);
                $('#uicity').append(opt);
            }
        }
    });
  }
  
  window.onload = onPageLoad;