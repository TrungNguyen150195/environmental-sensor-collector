from dataclasses import dataclass
import numpy as np


@dataclass
class SensorData:
    sensor_id: np.str_
    timestamp: np.datetime64
    temperature: np.float32
    humidity: np.float32
    co2: np.float32

    @classmethod
    def load_csv(cls, filename):
        # Load CSV file (skip header row)
        data = np.genfromtxt(
            filename,
            delimiter=",",
            names=True,
            dtype=None,
            encoding="utf-8"
        )

        return cls(
            sensor_id=data["sensor_id"],
            timestamp=data["timestamp"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            co2=data["co2"]
        )

    # Average temperature
    def average_temperature(self):
        return np.mean(self.temperature)

    # Maximum humidity
    def max_humidity(self):
        return np.max(self.humidity)

    # Minimum humidity
    def min_humidity(self):
        return np.min(self.humidity)

    # Total CO2 emissions
    def total_co2(self):
        return np.sum(self.co2)

    # Median temperature
    def median_temperature(self):
        return np.median(self.temperature)

    # Average temperature per sensor
    def average_temperature_per_sensor(self):
        sensors = np.unique(self.sensor_id)

        result = {}
        for sensor in sensors:
            avg_temp = np.mean(
                self.temperature[self.sensor_id == sensor]
            )
            result[sensor] = avg_temp

        return result


def main():
    sensor_data = SensorData.load_csv("sensor_data.csv")

    print("Average Temperature:", sensor_data.average_temperature())
    print("Maximum Humidity:", sensor_data.max_humidity())
    print("Minimum Humidity:", sensor_data.min_humidity())
    print("Total CO2:", sensor_data.total_co2())
    print("Median Temperature:", sensor_data.median_temperature())

    print("\nAverage Temperature Per Sensor:")
    for sensor, avg in sensor_data.average_temperature_per_sensor().items():
        print(f"{sensor}: {avg:.2f} °C")


if __name__ == "__main__":
    main()