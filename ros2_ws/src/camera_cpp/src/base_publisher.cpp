#include <chrono>
#include <memory>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

using namespace std::chrono_literals;

class BasePublisher : public rclcpp::Node
{
public:
  BasePublisher()
  : Node("base_publisher"), publish_count_(0)
  {
    this->declare_parameter<std::string>("output_topic", "");
    std::string output_topic = this->get_parameter("output_topic").as_string();

    rclcpp::QoS camera_image_qos = rclcpp::SensorDataQoS();
    camera_image_qos.keep_last(10).reliable();

    publisher_ = this->create_publisher<sensor_msgs::msg::Image>(output_topic, camera_image_qos);
    
    prepare_image_msg();

    auto period = std::chrono::duration<double>(1.0 / 1.0); // 1 Hz
    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_msg, this));
  }

private:
  void prepare_image_msg()
    {
      msg_.header.frame_id = "camera_link";
      msg_.width =  1920;  // Full HD
      msg_.height =  1080; 
      msg_.encoding = "rgb8";
      msg_.is_bigendian = false;

      unsigned int bytes_per_pixel = 3;
      msg_.step = msg_.width * bytes_per_pixel;

      size_t data_size = msg_.step * msg_.height;
      msg_.data.resize(data_size, 0); 
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

    publish_count_++;
    RCLCPP_INFO(
      this->get_logger(),
      "[SENT] Count: %zu | Stamp: %d.%09u",
      publish_count_,
      msg_.header.stamp.sec,
      msg_.header.stamp.nanosec
    );
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
  sensor_msgs::msg::Image msg_;
  size_t publish_count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}