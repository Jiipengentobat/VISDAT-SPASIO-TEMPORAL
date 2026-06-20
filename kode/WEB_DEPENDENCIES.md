# Web Dependencies (CDN)

Aplikasi web menggunakan library dari CDN (Content Delivery Network), sehingga tidak memerlukan npm atau build step.

## Libraries yang Digunakan:

### Mapping & Geospatial
- **Leaflet.js** v1.9.4 - Interactive map library
  - URL: https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/
  - Components: leaflet.min.js, leaflet.min.css
  
- **Leaflet.markercluster** v1.5.1 - Marker clustering for performance
  - URL: https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.1/
  - Components: leaflet.markercluster.min.js, MarkerCluster.min.css, MarkerCluster.Default.min.css

### Data Visualization
- **Chart.js** v3.9.1 - Interactive charts and graphs
  - URL: https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/
  - Components: chart.min.js

### Data Formats
- **GeoJSON** - Geographic JSON format (native JS support, no library needed)
- **TopoJSON** - Compressed geographic data (optional, for future optimization)

## No Backend Required
Aplikasi ini adalah pure front-end HTML5 + JavaScript yang dapat berjalan di:
- Static HTTP server (python -m http.server)
- GitHub Pages
- Vercel, Netlify
- Apache/Nginx server
- Bahkan local file system (dengan limitations)

## Internet Requirement
Aplikasi memerlukan internet connection untuk:
1. Load CDN libraries (Leaflet, Chart.js)
2. Load base map tiles dari OpenStreetMap
3. Load GeoJSON data files dari server

Jika ingin work offline, download semua CDN files dan host secara lokal.
