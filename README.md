# TraderMap

TraderMap is the official information and support website for the TraderMap apps on Apple platforms.

The site provides a product overview, privacy policy, technical support, terms of use, disclaimer, and operator information for:

- **TraderMap for iOS/iPadOS** — `com.17class.TraderMap`
- **TraderMapTV for tvOS** — `com.17class.TraderMapTV`

## Live site

- [Language selector](https://17classdeveloper-design.github.io/TraderMap/)
- [English](https://17classdeveloper-design.github.io/TraderMap/en/)
- [简体中文](https://17classdeveloper-design.github.io/TraderMap/zh-hans/)

## Pages

Each supported language contains the following pages:

- Marketing overview
- Privacy policy
- Technical support
- Terms of use and disclaimer
- Operator information

Supported languages:

| Code | Language |
| --- | --- |
| `en` | English |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `zh-hans` | 简体中文 |
| `zh-hant` | 繁體中文 |
| `de` | Deutsch |
| `fr` | Français |

## Project structure

```text
TraderMap/
├── assets/             Shared stylesheet and favicon
├── de/                 German pages
├── en/                 English pages
├── fr/                 French pages
├── ja/                 Japanese pages
├── ko/                 Korean pages
├── zh-hans/            Simplified Chinese pages
├── zh-hant/            Traditional Chinese pages
├── 404.html            GitHub Pages fallback
├── index.html          Language selector
├── robots.txt
└── sitemap.xml
```

Every language directory contains:

```text
<language>/
├── index.html
├── operator/index.html
├── privacy/index.html
├── support/index.html
└── terms/index.html
```

## Local preview

The site is static and has no build dependencies. Serve the parent directory so the production `/TraderMap/` base path works locally:

```bash
cd /path/to/parent-directory
python3 -m http.server 4312
```

Then open:

```text
http://localhost:4312/TraderMap/
```

## Deployment

GitHub Pages publishes the `gh-pages` branch. After changes have been reviewed and committed to `main`, deploy the same commit with:

```bash
git push origin main
git push origin main:gh-pages
```

The `.nojekyll` file keeps GitHub Pages in static-file mode.

## Support

Use the repository's [issue tracker](https://github.com/17classdeveloper-design/TraderMap/issues) for technical support, feedback, and feature requests. Do not include passwords, API tokens, seed phrases, private keys, or confidential financial information in public issues.

## Disclaimer

TraderMap provides market information for informational and educational purposes only. It does not provide investment advice, connect wallets, execute orders, or take custody of assets. Refer to the published terms and privacy policy for the complete notices.

## Operator

Developed and operated by **17ClassDeveloper** through the GitHub account [17classdeveloper-design](https://github.com/17classdeveloper-design).
