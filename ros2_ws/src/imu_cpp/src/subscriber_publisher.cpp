#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

using namespace std::chrono_literals;

class SubscriberPublisher : public rclcpp::Node
{
public:
  SubscriberPublisher()
  : Node("subscriber_publisher")
  {

    this->declare_parameter<std::string>("input_topic", "");
    this->declare_parameter<std::string>("output_topic", "");

    std::string input_topic = this->get_parameter("input_topic").as_string();
    std::string output_topic = this->get_parameter("output_topic").as_string();

    // TODO: use own Qos
    publisher_ = this->create_publisher<sensor_msgs::msg::Imu>(output_topic, rclcpp::SensorDataQoS());

    auto topic_callback =
      [this](sensor_msgs::msg::Imu::UniquePtr msg) -> void {
      publisher_->publish(std::move(msg)); 
    };
      // TODO: use own Qos
    subscription_ =
      this->create_subscription<sensor_msgs::msg::Imu>(input_topic, rclcpp::SensorDataQoS(), topic_callback);
  }

private:
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr subscription_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscriberPublisher>());
  rclcpp::shutdown();
  return 0;
}