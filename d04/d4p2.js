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

const VALIDATORS = {
    byr: value => 1920 <=Number(value) && Number(value) <= 2002,
    iyr: value => 2010 <=Number(value) && Number(value) <= 2020,
    eyr: value => 2020 <=Number(value) && Number(value) <= 2030,
    hgt: value => {
        const [measurement, units] = [value.slice(0,-2), value.slice(-2)];
        return (units === 'cm' && 150 <= Number(measurement) && Number(measurement) <= 193) ||
            (units === 'in' && 59 <= Number(measurement) && Number(measurement) <= 76)
    },
    hcl: value => /^#[0-9a-f]{6}$/.test(value),
    ecl: value => ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'].includes(value),
    pid: value => /^\d{9}$/.test(value),
    cid: () => true,
}

console.assert(  VALIDATORS['byr']('2002'));
console.assert( !VALIDATORS['byr']('2003'));
console.assert(  VALIDATORS['hgt']('60in'));
console.assert(  VALIDATORS['hgt']('190cm'));
console.assert( !VALIDATORS['hgt']('190in'));
console.assert( !VALIDATORS['hgt']('190'));
console.assert(  VALIDATORS['hcl']('#123abc'));
console.assert( !VALIDATORS['hcl']('#123abz'));
console.assert( !VALIDATORS['hcl']('123abc'));
console.assert(  VALIDATORS['ecl']('brn'));
console.assert( !VALIDATORS['ecl']('wat'));
console.assert(  VALIDATORS['pid']('000000001'));
console.assert( !VALIDATORS['pid']('0123456789'));


function isValid(passport) {
    passport = Object.fromEntries(passport.split(/\s/).map(field => field.split(':')));
    const missingFields = difference(REQUIRED_FIELDS, new Set(Object.keys(passport)));
    const unexpectedFields = difference(new Set(Object.keys(passport)), ALLOWED_FIELDS);
    const validFields = Object.entries(passport)
        .every(([fieldName, value]) => VALIDATORS[fieldName] && VALIDATORS[fieldName](value))
    return missingFields.size === 0 && unexpectedFields.size === 0 && validFields;
}

function main() {
    console.log(INPUT.trim().split('\n\n').filter(isValid).length);
}

main();
