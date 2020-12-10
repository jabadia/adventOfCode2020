const INPUT = require('./d8_input');

function parseProgram(input) {
    return input.trim().split('\n').map(line => {
        const [_, op, arg] = line.match(/(acc|jmp|nop) ([-+]?\d+)/);
        return { op, arg: parseInt(arg, 10) };
    });
}

function run(program) {
    let acc = 0;
    let pc = 0;

    const already_executed = new Set();

    while (true) {
        if (pc >= program.length)
            return acc;
        if (already_executed.has(pc))
            return false;
        already_executed.add(pc);
        const instruction = program[pc];
        switch (instruction.op) {
            case 'acc':
                acc += instruction.arg;
                pc += 1;
                break;
            case 'jmp':
                pc += instruction.arg;
                break;
            case 'nop':
                pc += 1;
                break;
            default:
                console.assert(false, 'bad instruction');
        }
    }
}

function main() {
    const program = parseProgram(INPUT);

    for (let i = 0; i < program.length; i++) {
        if (['nop', 'jmp'].includes(program[i].op)) {
            const modifiedProgram = [
                ...program.slice(0, i),
                { op: program[i].op === 'nop' ? 'jmp' : 'nop', arg: program[i].arg },
                ...program.slice(i + 1),
            ];
            const result = run(modifiedProgram);
            if (result) {
                console.log(result);
                return;
            }
        }
    }
    console.log('no result :-(');
}

main();
