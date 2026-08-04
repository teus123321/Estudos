const button = document.getElementById("button")
const email = document.getElementById("email")
const senha = document.getElementById("password")


button.addEventListener("click", (event) => {

    event.preventDefault();

    if (!email.value.endsWith("@gmail.com") || email.value.length <= 10) {
        alert("Email inválido ou senha inválida!");
    }
    else if (senha.value.length < 6) {
        alert("Senha inválida!");
    }
    else {
        alert("Login realizado com sucesso!");
        window.location.href = "index.html";
    }
})
