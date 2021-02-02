$(document).ready(function () {

    // ADD/EDIT RECIPE FORM STYLING LOGIC - Adds and removes custom style on form elements //

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

    $('.mat-input-outer textarea').focusin(function () {
        $(this).next('label').addClass('active');
    });

    $('.mat-input-outer textarea').focusout(function () {
        if (!$(this).val()) {
            $(this).next('label').removeClass('active');
        } else {
            $(this).next('label').addClass('active');
        }
    });

    // -------- //

    // Script for nav-bar recipes expand links //

    $('#recipes-navlink').click(function () {
        $('#breakfast-navlink').toggleClass('hide-link');
        $('#dessert-navlink').toggleClass('hide-link');
        $('#dinner-navlink').toggleClass('hide-link');
        $('#lunch-navlink').toggleClass('hide-link');
        $('#chev-up').toggleClass('hide-link');
        $('#chev-down').toggleClass('hide-link');
        $('#nav-hr').toggleClass('hide-link');
    });

    // -------- //

    /* Script for add_review range rating */
    
    if (window.location.href.indexOf("get-recipe") > -1) {
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
    // -------- //

});


// Copyright dynamic year for footer //

$("#copyright").text(new Date().getFullYear());

// ------- //

function setBubble(range, bubble) {
  const val = range.value;
  const min = 0;
  const max = 5;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;

  // Sets distance of range label 
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

// -------- //


// RECIPE FORM LOGIC //

// Counter Variables //

let ingredientCounter = 0
let stepCounter = 0

// -------- //

// Script for edit-recipe page - Add Ingredients //
    
    if (window.location.href.indexOf("edit-recipe") > -1) {
        let inputFormDiv = document.getElementById('ingredient-inputs');
        ingredientCounter = (inputFormDiv.getElementsByTagName('input').length);
    } else {
        ingredientCounter = 2;
    }

// Add ingredient functions // 

function add_ingredient() {
    let newInputHTML = $(document.createElement('div')).attr("id", 'recipe_ingredient_' + ingredientCounter);
    newInputHTML.after().html('<input type="text" name="recipe_ingredient" + id="ingredient_' + ingredientCounter + '" value="" required>' + '<div class="border"></div>');
    newInputHTML.appendTo("#ingredient-inputs");
    ingredientCounter ++;
}

function remove_ingredient() {
    if (ingredientCounter > 2) {
        $('#ingredient-inputs > div:last-child').remove();
        ingredientCounter --;
    }
}

function reset_ingredients() {
    $('#ingredient-inputs > div').not(':first').remove();
    $('#ingredient-inputs div').children('input').val('');
    ingredientCounter = 2;
}

// -------- //

// Script for edit-recipe page only - Add steps //
    
    if (window.location.href.indexOf("edit-recipe") > -1) {
        let methodDiv = document.getElementById('method-steps');
        stepCounter = (methodDiv.getElementsByTagName('textarea').length);
    } else {
        stepCounter = 2;
    }

// Add steps functions // 

function add_step() {
    let newInputHTML = $(document.createElement('div')).attr("id", 'recipe_step_' + stepCounter);
    newInputHTML.after().html('<textarea class="form-textarea" name="recipe_step" + id="step_' + stepCounter + '" rows="2" cols="90" required></textarea>' + '<div class="border"></div>');
    newInputHTML.appendTo("#method-steps");
    stepCounter ++;
}

function remove_step() {
    if (stepCounter > 2) {
        $('#method-steps > div:last-child').remove();
        stepCounter --;
    }
}

function reset_steps() {
    $('#method-steps > div').not(':first').remove();
    $('#method-steps div').children('textarea').val('');
    stepCounter = 2;
}

function ClearField(field) {
    document.getElementById(field).value = "";
}

// -------- //