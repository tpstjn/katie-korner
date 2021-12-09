let id = -1;
fname = "";
lname = "";

window.addEventListener("DOMContentLoaded", function() {
    //Set event listener for remove user buttons in manage.j2
    const removeButtons = document.getElementsByClassName("btnRemoveUser");
    for (let i = 0; i < removeButtons.length; i++) {
        removeButtons[i].addEventListener("click", removeEmployeePrompt);
    }
    const confirmRemoveButton = document.getElementById("btnConfirmRemoveUser")
    confirmRemoveButton.addEventListener("click", removeUser)
    
    const editButtons = document.getElementsByClassName("clickable")
    for (let i = 0; i < editButtons.length; i++) {
      editButtons[i].addEventListener("click", editEmployeePrompt);
    }

});

function removeUser() {
    if(id == -1) {
        alert("An error occured");
        return;
    }
    let url = "/removeEmployee/" + id + "/";
    this.href = url;
}

function removeEmployeePrompt() {
    if(checkCookie("employeeName")) {
        document.cookie = "employeeName=; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    //Get necessary variables from table
    let fnamelist = this.closest("tr").getElementsByClassName("fname");
    let lnamelist = this.closest("tr").getElementsByClassName("lname");
    let idlist = this.closest("tr").getElementsByClassName("id");
    fname = fnamelist[0].innerHTML;
    lname = lnamelist[0].innerHTML;
    id = idlist[0].innerHTML;
    
    let fullname = fname + " " + lname;
    let prompt = document.getElementById("removeEmployeePrompt");
    prompt.innerText = "Are you sure you want to remove " + fullname + "?";
}

function editEmployeePrompt() {
  //Get necessary variables from table
  let fnamelist = this.closest("tr").getElementsByClassName("fname");
  let lnamelist = this.closest("tr").getElementsByClassName("lname");
  let idlist = this.closest("tr").getElementsByClassName("id");
  let rolelist = this.closest("tr").getElementsByClassName("role");
  fname = fnamelist[0].innerHTML;
  lname = lnamelist[0].innerHTML;
  id = idlist[0].innerHTML;
  let role = rolelist[0].innerHTML;

  //Set query string for id
  const params = new URLSearchParams(location.search);
  params.set('id', id);
  // alert(params.toString()); // => test=123&cheese=yummy
  window.history.replaceState({}, '', `${location.pathname}?${params.toString()}`);

  //Get the form
  let editForm = document.forms['formEditEmployee'];

  //Get applicable form fields
  let formName = editForm.elements[1];
  let formRole = editForm.elements[2];

  //Fill with applicable value
  formName.value = fname + " " + lname;
  switch(role) {
    case "Cashier":
      formRole.value = 1;
      break;
    case "Kitchen":
      formRole.value = 2;
      break;
    case "Cleaner":
      formRole.value = 4;
      break;
    case "Manager":
      formRole.value = 8;
      break;
    case "Boss":
      formRole.value = 16;
      break;
  }
}

function getCookie(cookieName) {
    let name = cookieName + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function checkCookie(cookieName) {
    let cookie = getCookie(cookieName);
    if (cookie != "") {
      return true;
    } else {
      return false;
    }
}