// Renders docs/pitch-deck.html to per-slide PNGs (for visual QA) + a PDF.
// Run via the puppeteer Docker image (see the bash invocation).
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const outDir = '/work/.deckshots';
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-color-profile=srgb'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
  await page.goto('file:///work/docs/pitch-deck.html', { waitUntil: 'networkidle0' });

  const slides = await page.$$('.slide');
  console.log('slides found:', slides.length);
  const heights = await page.$$eval('.slide', els => els.map(e => e.scrollHeight));
  heights.forEach((h, i) => {
    const flag = h > 720 ? '  <-- OVERFLOW' : '';
    console.log(`slide ${String(i + 1).padStart(2, '0')}: ${h}px${flag}`);
  });

  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: `${outDir}/slide-${String(i + 1).padStart(2, '0')}.png` });
  }

  await page.pdf({
    path: '/work/docs/pitch-deck.pdf',
    width: '1280px', height: '720px',
    printBackground: true, pageRanges: '',
  });
  console.log('PDF + screenshots written.');
  await browser.close();
})();
