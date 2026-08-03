const button = document.getElementById("button")
const email = document.getElementById("email")
const senha = document.getElementById("password")


button.addEventListener("click", function (event) {

    event.preventDefault();

    if (email.value.trim() === "" || senha.value.trim() === "") {
        alert("Por favor, preencha todos os campos.");

    } else {
        alert("Login realizado com sucesso!");
        window.location.href = "index.html";
    }

})

