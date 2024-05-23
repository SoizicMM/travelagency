// Fonction permettant de charger toute la page html avant d'exécuter le js
$(document).ready(function() {
  // Fonction s'exécutant à chaque fois qu'une touche est relachée
  $('#password').on('keyup', function() {
    var password = $(this).val(); 
    var lowerCaseLetters = /[a-z]/g;
    var upperCaseLetters = /[A-Z]/g;
    var numbers = /[0-9]/g;

    // Vérifier et mettre a jour les conditions du mdp
    var lowercasePassed = password.match(lowerCaseLetters) ? true : false;
    var uppercasePassed = password.match(upperCaseLetters) ? true : false;
    var numberPassed = password.match(numbers) ? true : false;

    // On passe en vert les variables qui ont une valeur de stockée dedans (true)
    if (lowercasePassed) {
      $('#lowercase').css('color', 'green');
    } else {
      $('#lowercase').css('color', 'red');
    }
    if (uppercasePassed) {
      $('#uppercase').css('color', 'green');
    } else {
      $('#uppercase').css('color', 'red');
    }
    if (numberPassed) {
      $('#number').css('color', 'green');
    } else {
      $('#number').css('color', 'red');
    }

    // Activer le bouton de soumission si toutes les conditions sont remplies 
    if (lowercasePassed && uppercasePassed && numberPassed){
      $('#submit-btn').prop('disabled', false);
    } else {
      $('#submit-btn').prop('disabled', true);
    }
  });
});