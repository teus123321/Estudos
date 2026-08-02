const button = document.getElementById("button")

if (button) {
    button.addEventListener('click', () => {

        event.preventDefault();

        const textoOriginal = button.textContent

        button.textContent = "Carregando...";
        button.disabled = true;
        button.style.opacity = "0.5";
        button.style.cursor = "not-allowed";

        setTimeout(() => {
            button.textContent = textoOriginal
            button.disabled = false
            button.style.opacity = "1"
            button.style.cursor = "pointer"
            alert("Você está na página do poema !")

            window.location.href=button.href
        }, 2000)
    })
}
