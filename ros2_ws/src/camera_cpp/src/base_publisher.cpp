#include <chrono>
#include <memory>
#include <cmath>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

using namespace std::chrono_literals;

class BasePublisher : public rclcpp::Node
{
public:
  BasePublisher()
  : Node("base_publisher")
  {
    rclcpp::QoS camera_image_qos(rclcpp::KeepLast(1));

    camera_image_qos
      .reliable()
      .durability_volatile();

    publisher_ = this->create_publisher<sensor_msgs::msg::Image>("/camera", camera_image_qos);
    auto period = std::chrono::duration<double>(1.0 / 1.0);

    prepare_image_msg();

    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_msg, this));
  }

private:
  void prepare_image_msg()
    {
      msg_.header.frame_id = "camera_link";
      
      msg_.width = 3840;  
      msg_.height = 2160; 

      msg_.encoding = "rgb8";
      msg_.is_bigendian = false;

      unsigned int bytes_per_pixel = 3;
      msg_.step = msg_.width * bytes_per_pixel;

      size_t data_size = msg_.step * msg_.height;
      msg_.data.resize(data_size, 0); 
    }
  void publish_msg()
  {
    msg_.header.stamp = this->now();
    publisher_->publish(msg_);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
  sensor_msgs::msg::Image msg_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}