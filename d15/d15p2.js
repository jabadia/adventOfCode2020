const TEST_CASES = [
    // { input: '0,3,6', expected: 175594 },
]


function solve(input) {
    const starting_numbers = input.trim().split(',').map(Number);
    const spoken = new Map();
    starting_numbers.slice(0,-1).forEach((n,i) => spoken.set(n, i+1));
    let last_spoken = starting_numbers[starting_numbers.length -1];

    for(let turn=starting_numbers.length; turn < 30000000; turn+=1) {
        if (spoken.has(last_spoken)) {
            next = turn - spoken.get(last_spoken);
        } else {
            next = 0
        }
        spoken.set(last_spoken, turn);
        last_spoken = next;
    }
    return last_spoken;
}

function main() {
    TEST_CASES.forEach(({input, expected}) => {
        console.assert(expected === solve(input));
        console.log('OK');
    });
    console.log(solve('15,5,1,4,7,0'))
}

main();
