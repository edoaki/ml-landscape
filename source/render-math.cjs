// Run only during the build; readers need neither Node.js nor JavaScript.
const fs = require('node:fs');
const katex = require('./katex.min.cjs');
process.stdout.write(katex.renderToString(fs.readFileSync(0, 'utf8'), {
  displayMode: true,
  output: 'htmlAndMathml',
  throwOnError: true,
  strict: 'error',
  trust: false,
}));
