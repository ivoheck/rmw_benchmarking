#include <chrono>
#include <memory>
#include <cmath>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

using namespace std::chrono_literals;

class BasePublisher : public rclcpp::Node
{
public:
  BasePublisher()
  : Node("base_publisher")
  {
    publisher_ = this->create_publisher<sensor_msgs::msg::LaserScan>("/scan", rclcpp::SensorDataQoS());
    auto period = std::chrono::duration<double>(1.0 / 30.0);

    prepare_lidar_msg();

    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_scan, this));
  }

private:
  void prepare_lidar_msg()
    {
      msg_.header.frame_id = "laser_frame";

      msg_.angle_min = -3.0 * M_PI / 4.0;      
      msg_.angle_max = 3.0 * M_PI / 4.0;       

      msg_.angle_increment = (0.25 * M_PI) / 180.0; 

      msg_.time_increment = 0.030f / 1081.0f;
      
      msg_.scan_time = 1.0f / 30.0f;
      
      msg_.range_min = 0.10f;
      msg_.range_max = 30.0f;
      
      size_t num_readings = 1081;
      
      msg_.ranges = std::vector<float>(num_readings, 3.5f);
      msg_.intensities = std::vector<float>(num_readings, 1.0f);
    }
  void publish_scan()
  {
    auto now_steady = std::chrono::steady_clock::now();
    uint64_t nanoseconds_since_epoch = std::chrono::duration_cast<std::chrono::nanoseconds>(
      now_steady.time_since_epoch()
    ).count();

    msg_.header.stamp.sec = static_cast<int32_t>(nanoseconds_since_epoch / 1'000'000'000ULL);
    msg_.header.stamp.nanosec = static_cast<uint32_t>(nanoseconds_since_epoch % 1'000'000'000ULL);

    publisher_->publish(msg_);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr publisher_;
  sensor_msgs::msg::LaserScan msg_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}