#include <chrono>
#include <memory>
#include <cmath>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

using namespace std::chrono_literals;

class BasePublisher : public rclcpp::Node
{
public:
  BasePublisher()
  : Node("base_publisher")
  {
    publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("/imu", rclcpp::SensorDataQoS());
    auto period = std::chrono::duration<double>(1.0 / 500.0);

    prepare_imu_msg();

    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_msg, this));
  }

private:
  void prepare_imu_msg()
    {
      msg_.header.frame_id = "imu_link";

      msg_.orientation.w = 1.0;
      msg_.orientation.x = 0.0;
      msg_.orientation.y = 0.0;
      msg_.orientation.z = 0.0;

      msg_.orientation_covariance[0] = 0.01;

      msg_.angular_velocity.x = 0.0;
      msg_.angular_velocity.y = 0.0;
      msg_.angular_velocity.z = 0.1;

      msg_.linear_acceleration.x = 0.0;
      msg_.linear_acceleration.y = 0.0;
      msg_.linear_acceleration.z = 9.81;
    }

  void publish_msg()
  {    
    msg_.header.stamp = this->now();
    publisher_->publish(msg_);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_;
  sensor_msgs::msg::Imu msg_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}