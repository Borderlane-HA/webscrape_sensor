# Web Scrape Sensor (Home Assistant Custom Component)

A custom sensor platform for [Home Assistant](https://www.home-assistant.io/) that extracts a numeric value from any webpage using simple start and end delimiters.

## 🔧 Features

- Fetch data from any HTTP(S) URL
- Extract number using two delimiters (`start_string` and `end_string`)
- Set custom unit of measurement
- Update periodically

## 📦 Installation via HACS

1. Go to **HACS → Integrations → Custom repositories**
2. Add this repository URL: `https://github.com/yourusername/webscrape_sensor`
3. Select **Integration**
4. Click **Add** and install the `Web Scrape Sensor`

## 🛠️ Manual Configuration (`configuration.yaml`)

```yaml
sensor:
  - platform: webscrape_sensor
    name: Strompreis Sensor
    url: https://example.com/preise.html
    start_string: '<span class="preis">'
    end_string: '</span>'
    unit_of_measurement: "€/kWh"
