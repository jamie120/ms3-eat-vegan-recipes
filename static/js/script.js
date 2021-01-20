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

    /* Script for add_review range rating */
    
    if (window.location.href.indexOf("get_recipe") > -1) {
        console.log("connected");
        const range = document.querySelector(".range");
        const bubble = document.querySelector(".bubble");

        range.addEventListener("input", () => {
            setBubble(range, bubble);
        });
        setBubble(range, bubble);


        range.addEventListener("input", () => {
            setBubble(range, bubble);
        });
    }
});

function setBubble(range, bubble) {
  const val = range.value;
  const min = 0;
  const max = 5;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;

  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

/* Add ingredient functions */ 

ingredientCounter = 2

function add_ingredient() {
    console.log("pressed")
    var newInputHTML = $(document.createElement('div')).attr("id", 'recipe_ingredient_' + ingredientCounter);
    newInputHTML.after().html('<input type="text" name="recipe_ingredient" + id="ingredient_' + ingredientCounter + '" value="" >' + '<div class="border"></div>');
    newInputHTML.appendTo("#ingredient-inputs");
    ingredientCounter ++
}

function remove_ingredient() {
    if (ingredientCounter > 2) {
        $('#ingredient-inputs div:last-child').remove();
        ingredientCounter --
    }
}

function reset_ingredients() {
    $('#ingredient-inputs div').not(':first').remove();
    $('#ingredient-inputs div').children('input').val('');
    ingredientCounter = 2
}

/* Step method functions */

stepCounter = 2

function add_step() {
    console.log("pressed")
    var newInputHTML = $(document.createElement('div')).attr("id", 'recipe_step_' + stepCounter);
    newInputHTML.after().html('<textarea name="recipe_step" + id="step_' + stepCounter + '" rows="5" cols="90"></textarea>' + '<div class="border"></div>');
    newInputHTML.appendTo("#method-steps");
    stepCounter ++
}

function remove_step() {
    if (stepCounter > 2) {
        $('#method-steps div:last-child').remove();
        stepCounter --
    }
}

function reset_steps() {
    $('#method-steps div').not(':first').remove();
    $('#method-steps div').children('input').val('');
    stepCounter = 2
}




function ClearField(field) {
    document.getElementById(field).value = "";
}