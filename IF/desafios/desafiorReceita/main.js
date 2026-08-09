const cardOne = document.getElementById("inner-card-1")
const cardTwo = document.getElementById("inner-card-2")

cardOne.addEventListener("click",() => {
    cardOne.classList.toggle("virado")
})

cardTwo.addEventListener("click", () =>{
    cardTwo.classList.toggle("virado")
})