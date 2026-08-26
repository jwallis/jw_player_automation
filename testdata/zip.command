cd "$(dirname "$0")"
rm -rf device_farm_extra_data device_farm_extra_data.zip
mkdir device_farm_extra_data
cp -R gen* device_farm_extra_data/
zip -X -r device_farm_extra_data.zip device_farm_extra_data
rm -rf device_farm_extra_data
