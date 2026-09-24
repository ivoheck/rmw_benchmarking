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
    this->declare_parameter<std::string>("output_topic", "");
    std::string output_topic = this->get_parameter("output_topic").as_string();

    publisher_ = this->create_publisher<sensor_msgs::msg::Imu>(output_topic, rclcpp::SensorDataQoS());
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
    auto now_steady = std::chrono::steady_clock::now();
    uint64_t nanoseconds_since_epoch = std::chrono::duration_cast<std::chrono::nanoseconds>(
      now_steady.time_since_epoch()
    ).count();

    msg_.header.stamp.sec = static_cast<int32_t>(nanoseconds_since_epoch / 1'000'000'000ULL);
    msg_.header.stamp.nanosec = static_cast<uint32_t>(nanoseconds_since_epoch % 1'000'000'000ULL);
    
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