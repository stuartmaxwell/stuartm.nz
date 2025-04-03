const path = require('path');

module.exports = {
  entry: {
    main: './build/js/index.js',  // Entry point for the JavaScript
    markdown: './build/js/markdown.js',  // Entry point for the Markdown editor
  },
  output: {
    filename: '[name].bundle.min.js',
    path: path.resolve(__dirname, 'static/js'),  // Uses `path.resolve`
  },
  mode: 'production',  // Set to 'production' for production builds
};
