yaml

sensor:
  - platform: webscrape_sensor
    name: Strompreis Sensor
    url: https://example.com/preise.html
    start_string: '<span class="preis">'
    end_string: '</span>'
    unit_of_measurement: "€/kWh"
