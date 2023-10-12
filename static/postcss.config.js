// postcss.config.js
module.exports = {
    plugins: [
      require('tailwindcss'),
      require('autoprefixer'),
      process.env.NODE_ENV === 'production' &&
        require('@fullhuman/postcss-purgecss')({
          content: ['./templates/**/*.html'], // Adjust the path as needed
          defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
        }),
    ],
  };
  