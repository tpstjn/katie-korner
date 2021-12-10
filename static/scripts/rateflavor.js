let flavor = "";

window.addEventListener("DOMContentLoaded", function() {
    let rateForm = document.forms['formRateFlavor'];

    let submitRating = rateForm.elements[3];

    // An attempt to dynamically load comments but couldn't get CORS to function properly
    // const flavorRows = document.getElementsByClassName("FlavorRow");

    // for (let i = 0; i < flavorRows.length; i++) {
    //     flavorRows[i].addEventListener("click", loadComments);
    // }

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

// An attempt to dynamically load comments
// function loadComments() {
//     let flavorList = this.closest("tr").getElementsByClassName("flavor_label");
//     flavor = flavorList[0].innerHTML;
//     const baseURL = `http://localhost:5000/api/comments/${flavor}`
    
//     fetch(baseURL)
//         .then(validateJSON)
//         .then(data => {
//             console.log(data)
//         })
// }

// /**
//  * Validate a response to ensure the HTTP status code indcates success.
//  * 
//  * @param {Response} response HTTP response to be checked
//  * @returns {object} object encoded by JSON in the response
//  */
//  function validateJSON(response) {
//     if (response.ok) {
//         return response.json();
//     } else {
//         return Promise.reject(response);
//     }
// }
