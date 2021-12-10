let flavor = "";

window.addEventListener("DOMContentLoaded", function() {
    let rateForm = document.forms['formRateFlavor'];

    let submitRating = rateForm.elements[3];

    //Set event listener for rate button pressed to get pressed flavor tab
    const ratemeBtns = document.getElementsByClassName("RateMeBtn");

    for (let i = 0; i < ratemeBtns.length; i++) {
        ratemeBtns[i].addEventListener("click", getFlavor);
    }
    submitRating.addEventListener("click", submitFlavor);
});

function getFlavor() {
    //Get necessary variables from table
    let flavorList = this.closest("tr").getElementsByClassName("flavor_label");
    flavor = flavorList[0].innerHTML;

    let header = document.getElementById("rate");
    header.innerText = flavor;
}

function submitFlavor() {
    //Set query string for flavor
    const params = new URLSearchParams(location.search);
    params.set('flavor', flavor);
    //alert(params.toString()); // => test=123&cheese=yummy
    window.history.replaceState({}, '', `${location.pathname}?${params.toString()}`);
}
