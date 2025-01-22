/* eslint-env node */

var Mocha = require('mocha');
var fs = require('fs');
var path = require('path');

var basePath = './media/js/tests';
var mocha = new Mocha();

// eslint-disable-next-line security/detect-non-literal-fs-filename
fs.readdirSync(basePath).filter(function(file) {
    return file !== __filename && file.substr(-3) === '.js';
}).forEach(function(file) {
    mocha.addFile(path.join(basePath, file));
});

mocha.run(function(failures) {
    process.on('exit', function() {
        process.exit(failures);
    });
});
