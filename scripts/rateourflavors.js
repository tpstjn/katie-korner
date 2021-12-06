// add a listener so that when the document loads . . .
// new listeners  can be attched to elements safely
window.addEventListener("DOMContentLoaded", function() {
	// attach a listener to call openFlavorTab when button is clicked
	const button = document.querySelector("input[type=button]");
	window.addEventListener("click", openFlavorTab);
});

// define a function to open flavor tab to fill out form
function openFlavorTab() {
    // TODO: ADD FLAVOR TAB
    // ??? Or just new page?
    

	// let lyrics = document.getElementsByName("lyrics");
	// let firstVerse = lyrics.firstElementChild;
	// let nextVerse = firstVerse.cloneNode(true);
	// lyrics.appendChild(nextVerse);
}