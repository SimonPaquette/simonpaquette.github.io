/*
    My presentation, resume and projects
    Simon Paquette - Portfolio
    Author: Simon Paquette
    Latest update: 2022/06
*/

/*
 * Show/Hide the language select by the user (EN/FR)
 * To keep preference between pages, keep it on sessionStorage
 */
function start() {
  //Set default language to english for each new tab
  if (sessionStorage.length == 0) {
    sessionStorage.setItem("lang", "en");
  }

  //Display language
  var lang = sessionStorage.getItem("lang");
  if (lang === "en") {
    $("[lang=fr]").hide();
  } else if (lang === "fr") {
    $("[lang=en]").hide();
  }

  //Associate the toggleLang button to the function
  $("#toggleLang").click(function () {
    $("[lang=fr]").toggle();
    $("[lang=en]").toggle();

    if (lang === "en") {
      sessionStorage.setItem("lang", "fr");
    } else if (lang === "fr") {
      sessionStorage.setItem("lang", "en");
    }
  });
}

window.addEventListener("load", start, false);
