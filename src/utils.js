const { toBufferLE, toBigIntLE } = require('bigint-buffer');

// Helper functions
function checkIfValidHexString(hexString) {
    if(typeof hexString !== 'string')
        return false;
    let re = new RegExp('^(0x|0X)?[a-fA-F0-9]+$');
    return re.test(hexString);
}

function decimalToLittleEndianHexString(number) {
    if(typeof(number) !== 'bigint' && isNaN(number))
        throw ("Error: Argument %s should be a Number or BigInt", number);
    let length = 1+number.toString(16).length*0.5;// We gotta figure out how long this string will be
    let hexStr = toBufferLE(number,length).toString('hex');
    // Strip any final null bytes
    if(hexStr.endsWith('00'))hexStr = hexStr.slice(0, hexStr.length-2);
    return '0x'+hexStr;
}

function littleEndianHexStringToDecimal(hexString){
    if (!checkIfValidHexString(hexString))
        throw ("Error: Hex %s should be hexadecimal with or without '0x' at the beginning.", hexString);
    // Remove 0x from string if necessary
    hexString = hexString.replace('0x', '');
    return toBigIntLE(Buffer.from( hexString, 'hex' ));
}

// Test functions
/**
 * Returns a random integer between min (inclusive) and max (inclusive).
 * The value is no lower than min (or the next integer greater than min
 * if min isn't an integer) and no greater than max (or the next integer
 * lower than max if max isn't an integer).
 * Using Math.round() will give you a non-uniform distribution!
 */
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Random hex string generator
function getRandomHex(len) {
    let output = '';
    for (let i = 0; i < len; ++i) {
        output += (Math.floor(Math.random() * 16)).toString(16);
    }
    return output;
}

function sign(value) {
    if (value > 0n) {
        return 1n;
    }
    if (value < 0n) {
        return -1n;
    }
    return 0n;
}

function bigIntAbsoluteValue(value) {
    if (sign(value) === -1n) {
        return -value;
    }
    else return value;
}

module.exports = {
    checkIfValidHexString,
    decimalToLittleEndianHexString,
    littleEndianHexStringToDecimal,
    bigIntAbsoluteValue,
    getRandomInt,
    getRandomHex
}
