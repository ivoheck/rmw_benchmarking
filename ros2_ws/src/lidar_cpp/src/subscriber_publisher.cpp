#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

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

    publisher_ = this->create_publisher<sensor_msgs::msg::LaserScan>(output_topic, rclcpp::SensorDataQoS());

    auto topic_callback =
      [this](sensor_msgs::msg::LaserScan::UniquePtr msg) -> void {
      publisher_->publish(std::move(msg)); 
    };

    subscription_ =
      this->create_subscription<sensor_msgs::msg::LaserScan>(input_topic, rclcpp::SensorDataQoS(), topic_callback);
  }

private:
  rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscriberPublisher>());
  rclcpp::shutdown();
  return 0;
}