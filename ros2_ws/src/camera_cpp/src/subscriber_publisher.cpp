#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

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
    publisher_ = this->create_publisher<sensor_msgs::msg::Image>(output_topic, rclcpp::QoS(10));

    auto topic_callback =
      [this](sensor_msgs::msg::Image::UniquePtr msg) -> void {
      publisher_->publish(std::move(msg)); 
    };
      // TODO: use own Qos
    subscription_ =
      this->create_subscription<sensor_msgs::msg::Image>(input_topic, rclcpp::QoS(10), topic_callback);
  }

private:
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscriberPublisher>());
  rclcpp::shutdown();
  return 0;
}