[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

### Note:
**CHILD LOCK, CHANGE LIGHTS, AND LIKE THAT FEATURES WILL BE ADDED SOON**

### Installation:
Just copy paste the content of the `custom_components` folder in your `config/custom_components` directory.

### Usage:
```yaml
fan:
  platform: philips_airpurifier
  host: 192.168.0.17
```

### Configuration variables:
Field | Value | Necessity | Description
--- | --- | --- | ---
platform | `philips_airpurifier` | *Required* | The platform name.
host | 192.168.0.17 | *Required* | IP address of your Purifier.
name | Philips Air Purifier | Optional | Name of the Fan.

***
