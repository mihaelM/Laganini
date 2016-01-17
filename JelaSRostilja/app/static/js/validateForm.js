function isInt(value) {
    return !isNaN(value) &&
           parseInt(Number(value)) == value &&
           !isNaN(parseInt(value, 10));
}

function validateForm(f) {
    ime = f.name;
    var x = document.forms[ime]["kolicina"].value;
    if (!isInt(x)) {
        alert("Morate unjeti broj!");
        return false;
    }
    if (x == null || x == "") {
        alert("Morate odrediti broj porcija!");
        return false;
    }
    if (x > 10 || x < 1) {
        alert("Broj porcija mora biti između 1 i 10!");
        return false;
    }
}