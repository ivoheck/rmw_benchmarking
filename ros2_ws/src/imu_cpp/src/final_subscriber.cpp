#include <chrono>
#include <memory>
#include <cmath>
#include <vector>
#include <fstream> 
#include <cstdlib>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

class FinalSubscriber : public rclcpp::Node
{
public:
  FinalSubscriber()
  : Node("final_subscriber"), count_(0), is_done_(false)
  {
    this->declare_parameter<int64_t>("messurement_count", 0);
    this->measurement_count_ = static_cast<size_t>(this->get_parameter("messurement_count").as_int());

    this->declare_parameter<int64_t>("run_number", -1);
    int64_t run_num_int = this->get_parameter("run_number").as_int();
    this->run_number_ = std::to_string(run_num_int);

    std::string rmw = rmw_get_implementation_identifier();
    file_path_ = "/home/ivo/PersonalData/UniKram/Haw_sem_2/Protocol Engineering/code/messurement/imu_cpp_results_" + rmw + "_nr_" + run_number_ + ".txt";

    auto listener_callback = [this](const sensor_msgs::msg::Imu::SharedPtr msg) -> void {
      if (this->is_done_) {
        return;
      }

      rclcpp::Time now = this->now();
      rclcpp::Time msg_time = msg->header.stamp;
      rclcpp::Duration diff = now - msg_time;

      if (this->count_ < measurement_count_) {
        this->measurements_.push_back(diff.nanoseconds());
        
        RCLCPP_INFO(this->get_logger(), "Diff in Seconds: %f", diff.seconds());
        this->count_++;
      } else {
        RCLCPP_INFO(this->get_logger(), "Stop messurment");
        this->is_done_ = true;
        
        throw std::runtime_error("MEASUREMENT_DONE");
      }
    };

    subscription_ = this->create_subscription<sensor_msgs::msg::Imu>(
      "/imu_final", 
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
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr subscription_;
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