export function fibonacci(n) {
    
    let a = 0, b = 1, c

    for (let i = 0; i < n; i++) {
        c = a + b
        a = b
        b = c
        console.log(a)
    }
}


console.log(fibonacci(10))