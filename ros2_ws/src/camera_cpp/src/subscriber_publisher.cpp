#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

class SubscriberPublisher : public rclcpp::Node
{
public:
  SubscriberPublisher()
  : Node("subscriber_publisher")
  {
    this->declare_parameter<std::string>("input_topic", "camera");
    this->declare_parameter<std::string>("output_topic", "camera_1");

    std::string input_topic = this->get_parameter("input_topic").as_string();
    std::string output_topic = this->get_parameter("output_topic").as_string();

    rclcpp::QoS camera_image_qos = rclcpp::SensorDataQoS();
    camera_image_qos.keep_last(1).reliable();

    publisher_ = this->create_publisher<sensor_msgs::msg::Image>(output_topic, camera_image_qos);

    auto topic_callback = [this](const sensor_msgs::msg::Image::SharedPtr msg) -> void {
      publisher_->publish(*msg); 
    };

    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      input_topic, camera_image_qos, topic_callback);
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