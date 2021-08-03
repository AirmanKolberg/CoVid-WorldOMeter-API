const request = require('request');
const cheerio = require('cheerio');
const fs = require('fs');
const writeStream = fs.createWriteStream('post.csv');

// Write Headers
writeStream.write(`Title,Link,Date \n`);

request('https://www.worldometers.info/coronavirus/', (error, response, html) => {
  if (!error && response.statusCode == 200) {
    const $ = cheerio.load(html);

    $('.post-main_table_countries_div').each((i, el) => {
      const title = $(el)

      console.log(title)

      // Write Row To CSV
      writeStream.write(`${title}, ${link}, ${date} \n`);
    });

    // console.log('Scraping Done...');
  }
});