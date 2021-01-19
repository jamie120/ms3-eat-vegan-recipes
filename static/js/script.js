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


  const range = document.querySelector(".range");
  const bubble = document.querySelector(".bubble");

  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);


range.addEventListener("input", () => {
  setBubble(range, bubble);
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

counter = 2

function add_ingredient() {
    console.log("pressed")
    var newInputHTML = $(document.createElement('div')).attr("id", 'recipe_ingredient_' + counter);
    newInputHTML.after().html('<input type="text" name="recipe_ingredient" + id="ingredient_' + counter + '" value="" >' + '<div class="border"></div>');
    newInputHTML.appendTo("#ingredient-inputs");
    counter ++
}

function remove_ingredient() {
    if (counter > 2) {
        $('#ingredient-inputs div:last-child').remove();
        counter --
    }
}

function reset_ingredients() {
    $('#ingredient-inputs div').not(':first').remove();
    $('#ingredient-inputs div').children('input').val('');
    counter = 2
}

function ClearField(field) {
    document.getElementById(field).value = "";
}