#include <chrono>
#include <memory>
#include <vector>
#include <fstream> 
#include <cstdlib>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "rmw/rmw.h"

class FinalSubscriber : public rclcpp::Node
{
public:
  FinalSubscriber()
  : Node("final_subscriber"), count_(0), is_done_(false)
  {
    this->declare_parameter<std::string>("input_topic", "camera_final");
    std::string input_topic = this->get_parameter("input_topic").as_string();

    this->declare_parameter<int64_t>("messurement_count", 0);
    this->measurement_count_ = static_cast<size_t>(this->get_parameter("messurement_count").as_int());

    this->declare_parameter<int64_t>("run_number", -1);
    int64_t run_num_int = this->get_parameter("run_number").as_int();
    this->run_number_ = std::to_string(run_num_int);

    const char* env_dir = std::getenv("MEASUREMENT_OUTPUT_DIR");
    std::string base_dir = (env_dir != nullptr) ? std::string(env_dir) : "/messurement";
    std::string rmw = rmw_get_implementation_identifier();
    file_path_ = base_dir + "/camera_cpp_results_" + rmw + "_nr_" + run_number_ + ".txt";

    if (measurement_count_ > 0) {
      measurements_.reserve(measurement_count_);
    }

    auto listener_callback = [this](const sensor_msgs::msg::Image::SharedPtr msg) -> void {
      uint64_t receive_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::steady_clock::now().time_since_epoch()
      ).count();

      if (this->is_done_) {
        return;
      }

      uint64_t send_ns = static_cast<uint64_t>(msg->header.stamp.sec) * 1'000'000'000ULL 
                        + msg->header.stamp.nanosec;

      uint64_t latency_ns = receive_ns - send_ns;

      if (this->count_ < measurement_count_) {
        this->measurements_.push_back(static_cast<int64_t>(latency_ns));
        RCLCPP_INFO(this->get_logger(), "Count: %zu | Latency: %ld ns", this->count_, static_cast<int64_t>(latency_ns));
        this->count_++;
      } 
      
      if (this->count_ >= measurement_count_) {
        RCLCPP_INFO(this->get_logger(), "Stop messurment");
        this->is_done_ = true;
        this->subscription_.reset();
        rclcpp::shutdown();
      }
    };

    rclcpp::QoS camera_image_qos = rclcpp::SensorDataQoS();
    camera_image_qos.keep_last(1).reliable();

    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      input_topic, 
      camera_image_qos, 
      listener_callback
    );
  }

  void save_data()
  {
    std::ofstream file(file_path_);
    if (file.is_open()) {
      for (const int64_t ts : measurements_) {
        file << ts << "\n";
      }
      file.close();
      RCLCPP_INFO(this->get_logger(), "Saved data at: %s", file_path_.c_str());
    } else {
      RCLCPP_ERROR(this->get_logger(), "Error saving data at: %s", file_path_.c_str());
    }
  }

  bool has_data() const { return !measurements_.empty(); }

private:
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
  size_t count_;
  bool is_done_;
  std::vector<int64_t> measurements_;
  size_t measurement_count_;
  std::string run_number_;
  std::string file_path_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<FinalSubscriber>();
  rclcpp::spin(node);

  if (node->has_data()) {
    node->save_data();
  }

  return 0;
}