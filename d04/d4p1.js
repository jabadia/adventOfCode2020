const INPUT = require('./d4_input');

function union(s1, s2) {
    // https://2ality.com/2015/01/es6-set-operations.html#union
    return new Set([...s1, ...s2]);
}

function difference(s1, s2) {
    // https://2ality.com/2015/01/es6-set-operations.html#difference
    return new Set([...s1].filter(x => !s2.has(x)));
}

const REQUIRED_FIELDS = new Set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']);
const ALLOWED_FIELDS = union(REQUIRED_FIELDS, ['cid']);

function isValid(passport) {
    const fields = new Set(passport.split(/\s/).map(field => field.split(':')[0]));
    const missingFields = difference(REQUIRED_FIELDS, fields);
    const unexpectedFields = difference(fields, ALLOWED_FIELDS);
    return missingFields.size === 0 && unexpectedFields.size === 0;
}

function main() {
    console.log(INPUT.trim().split('\n\n').filter(isValid).length);
}

main();
