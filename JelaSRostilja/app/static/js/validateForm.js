function validateForm() {
    var x = document.forms["myForm"]["kolicina"].value;
    if (x == null || x == "") {
        alert("Morate odrediti broj porcija (količinu) jela!");
        return false;
    }
}