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

    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_scan, this));
  }

private:
  void publish_scan()
  {
    auto scan_msg = sensor_msgs::msg::LaserScan();

    scan_msg.header.frame_id = "laser_frame";
  
    // Deine Winkelkonfiguration
    scan_msg.angle_min = -M_PI / 2.0;       // -90 Grad
    scan_msg.angle_max = M_PI / 2.0;        // +90 Grad
    scan_msg.angle_increment = M_PI / 180.0; // 1 Grad Schritte
    
    scan_msg.time_increment = 0.0f;
    scan_msg.scan_time = 0.1f;
    
    scan_msg.range_min = 0.12f;
    scan_msg.range_max = 10.0f;
    
    // TODO: use 360
    size_t num_readings = 181;
    
    scan_msg.ranges = std::vector<float>(num_readings, 3.5f);
    scan_msg.intensities = std::vector<float>(num_readings, 1.0f);

    scan_msg.header.stamp = this->now();
    publisher_->publish(scan_msg);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr publisher_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}