const fs              = require('fs');
const { spawn, fork } = require('child_process');

const path_a = 'pipe_a';
const path_b = 'pipe_b';
let fifo_b   = spawn('mkfifo', [path_b]);  // Create Pipe B

fifo_b.on('exit', function(status) {
    console.log('Created Pipe B');

    const fd   = fs.openSync(path_b, 'r+');
    let fifoRs = fs.createReadStream(null, { fd });
    let fifoWs = fs.createWriteStream(path_a);

    console.log('Ready to write')

    s = 'cousin hero'
    fifoWs.write(s + '\n');
    console.log('-----   Send packet   -----');
    console.log('    ' + s);

    s = 'note most of these a currently are of print'
    fifoWs.write(s + '\n');
    console.log('-----   Send packet   -----');
    console.log('    ' + s);

    fifoRs.on('data', data => {
        console.log('----- Received packet -----');
        console.log('    ' + data.toString());
    });

});
