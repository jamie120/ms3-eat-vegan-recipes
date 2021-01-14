$(document).ready(function () {

    $('.mat-input-outer label').click(function () {
        $(this).prev('input').focus();
    });
    $('.mat-input-outer input').focusin(function () {
        $(this).next('label').addClass('active');
    });
    $('.mat-input-outer input').focusout(function () {
        if (!$(this).val()) {
            $(this).next('label').removeClass('active');
        } else {
            $(this).next('label').addClass('active');
        }
    });

});

ingredient_list = []

function add_ingredient() {
    var ingredient = document.getElementById("recipe_ingredient").value;
    document.getElementById("ingredients_list").innerHTML += "<li>" + ingredient + "</li>";
    ingredient_list.push(ingredient)
    console.log(ingredient_list)
    ClearField("recipe_ingredient");
}

function remove_ingredient() {
    $('#ingredients_list li:last-child').remove();
    ingredient_list.pop()
}


function ClearField(field) {
    document.getElementById(field).value = "";
}

$('#submit').click(function() {
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "/add_recipe",
      traditional: "true",
      data: JSON.stringify({ingredient_list}),
      dataType: "json"
      });
});
