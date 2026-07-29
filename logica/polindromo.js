console.log("Hoje iremos testar se uma palavra é um palíndromo ! ")


const isPalindrome = (str) => {
    const reversedStr = str.split('').reverse().join('');
    return str === reversedStr;
}

console.log(isPalindrome("arara")); // true
console.log(isPalindrome("ovo")); // true
console.log(isPalindrome("javascript")); // false