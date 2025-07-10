# Scientific MCPs Website

This directory contains the GitHub Pages website for the Scientific MCPs collection.

## 🌐 Live Website

Visit the live website at: **https://iowarp.github.io/scientific-mcps**

## 📁 Structure

- `index.html` - Homepage with MCP directory
- `_config.yml` - Jekyll configuration
- `assets/` - CSS, JavaScript, and other assets
- `mcps/` - Individual MCP detail pages
- `.github/workflows/` - GitHub Actions for deployment

## 🔧 Local Development

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Serve locally:
   ```bash
   bundle exec jekyll serve
   ```

3. Visit `http://localhost:4000/scientific-mcps`

## 🚀 Deployment

The website is automatically deployed via GitHub Actions when changes are pushed to the main branch.

## 📝 Adding New MCPs

See the main integration guide in the repository root for detailed instructions on adding new MCPs to the website.

## 🎨 Features

- Interactive MCP directory with search and filtering
- Responsive design for all devices
- GitHub API integration for live repository stats
- Detailed installation and usage documentation for each MCP
- Clean, professional design inspired by modern developer tools

## 📊 MCP Categories

- **Data Processing**: Adios, ArXiv, HDF5, Pandas, Parquet
- **Analysis & Visualization**: Plot, Darshan
- **System Management**: Slurm, Lmod, Node Hardware
- **Utilities**: Compression, Parallel Sort, Jarvis