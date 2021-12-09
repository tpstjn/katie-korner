window.addEventListener("DOMContentLoaded", function () {
    // attach an event listener to the later button
});

function displayCalendar() {
    document.getElementById('calendar').style.display = "block";
}

function hideCalendar() {
    document.getElementById('calendar').style.display = "none";
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
 function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}