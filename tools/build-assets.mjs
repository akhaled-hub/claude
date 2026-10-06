// Pulls real brand marks from Iconify / Simple Icons into brochure/assets/logos
import { readFileSync, writeFileSync } from 'node:fs';
import QRCode from 'qrcode';

const out = new URL('../brochure/assets/', import.meta.url);
const logos = JSON.parse(readFileSync(new URL('./node_modules/@iconify-json/logos/icons.json', import.meta.url)));
const si = JSON.parse(readFileSync(new URL('./node_modules/@iconify-json/simple-icons/icons.json', import.meta.url)));

const svg = (set, name, fill) => {
  const icon = set.icons[name];
  if (!icon) throw new Error(`missing ${name}`);
  const w = icon.width ?? set.width ?? 24, h = icon.height ?? set.height ?? 24;
  let body = icon.body;
  if (fill) body = body.replace(/currentColor/g, fill);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">${body}</svg>`;
};

const colour = {
  sap: [logos, 'sap'], oracle: [logos, 'oracle'], linkedin: [logos, 'linkedin-icon'],
  whatsapp: [logos, 'whatsapp-icon'], gmail: [logos, 'google-gmail'], teams: [logos, 'microsoft-teams'],
  zoom: [logos, 'zoom-icon'], meet: [logos, 'google-meet'], slack: [logos, 'slack-icon'],
  samsung: [logos, 'samsung'], udemy: [logos, 'udemy-icon'],
};
for (const [k, [set, n]] of Object.entries(colour)) writeFileSync(new URL(`logos/${k}.svg`, out), svg(set, n));

const mono = { docusign: ['docusign', '#1B1B1F'], indeed: ['indeed', '#003A9B'] };
for (const [k, [n, c]] of Object.entries(mono)) writeFileSync(new URL(`logos/${k}.svg`, out), svg(si, n, c));

for (const n of ['linkedin', 'x', 'instagram', 'youtube', 'facebook'])
  writeFileSync(new URL(`logos/social-${n}.svg`, out), svg(si, n, 'currentColor'));

writeFileSync(new URL('img/qr-elevatus.svg', out),
  await QRCode.toString('https://www.elevatus.io/', { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#0A0F2E', light: '#0000' } }));
console.log('assets written');
