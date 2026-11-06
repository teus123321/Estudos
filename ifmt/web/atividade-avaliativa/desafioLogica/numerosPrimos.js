export function ehPrimo(number) {
    
    if (number <= 1) return false;

    for (let i = 2; i < number; i++) {
        if (number % i === 0) {
            console.log(`${number} não é primo`)
            return false;
        }
    }
    console.log(`${number} é primo`)
    return true;

}




ehPrimo(7);