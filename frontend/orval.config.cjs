const { defineConfig } = require('orval')

module.exports = defineConfig({
  bookReview: {
    input: {
      target: 'http://localhost:9000/openapi.json'
    },
    output: {
      target: 'src/api/index.ts',
      client: 'vue-query',
      mode: 'single'
    }
  },
})
