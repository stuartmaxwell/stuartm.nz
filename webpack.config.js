const path = require('path');

module.exports = {
  entry: './build/js/index.js',  // Entry point for the JavaScript
  output: {
    filename: 'bundle.min.js',
    path: path.resolve(__dirname, 'static/js'),  // Uses `path.resolve`
  },
  mode: 'production',  // Set to 'production' for production builds
};
