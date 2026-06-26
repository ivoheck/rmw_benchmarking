#include <chrono>
#include <memory>
#include <cmath>
#include <vector>
#include <fstream> 
#include <cstdlib>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

const size_t MEASUREMENT_COUNT = 1000;

class FinalSubscriber : public rclcpp::Node
{
public:
  FinalSubscriber()
  : Node("final_subscriber"), count_(0), is_done_(false)
  {
    
    std::string rmw = rmw_get_implementation_identifier();
    file_path_ = "/home/ivo/PersonalData/UniKram/Haw_sem_2/Protocol Engineering/code/messurement/lidar_cpp_results_" + rmw + ".txt";

    auto listener_callback = [this](const sensor_msgs::msg::LaserScan::SharedPtr msg) -> void {
      if (this->is_done_) {
        return;
      }

      rclcpp::Time now = this->now();
      rclcpp::Time msg_time = msg->header.stamp;
      rclcpp::Duration diff = now - msg_time;

      if (this->count_ < MEASUREMENT_COUNT) {
        this->measurements_.push_back(diff.nanoseconds());
        
        RCLCPP_INFO(this->get_logger(), "Diff in Seconds: %f", diff.seconds());
        this->count_++;
      } else {
        RCLCPP_INFO(this->get_logger(), "Stop messurment");
        this->is_done_ = true;
        
        throw std::runtime_error("MEASUREMENT_DONE");
      }
    };

    subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
      "/scan_final", 
      rclcpp::SensorDataQoS(), 
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
      RCLCPP_ERROR(this->get_logger(), "Error with saving data at: %s", file_path_.c_str());
    }
  }

  bool has_data() const { return !measurements_.empty(); }

private:
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
  size_t count_;
  bool is_done_;
  std::vector<int64_t> measurements_;
  std::string file_path_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  
  auto node = std::make_shared<FinalSubscriber>();
  
  try {
    rclcpp::spin(node);
  } catch (const std::runtime_error& e) {
    if (std::string(e.what()) == "MEASUREMENT_DONE") {
      std::cout << "Spin kontrolliert beendet. Daten voll." << std::endl;
    } else {
      std::cerr << "Unerwarteter Fehler: " << e.what() << std::endl;
    }
  } catch (const std::exception& e) {}

  if (node->has_data()) {
    node->save_data();
  }

  rclcpp::shutdown();
  return 0;
}