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
    publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("/imu", rclcpp::SensorDataQoS());
    auto period = std::chrono::duration<double>(1.0 / 500.0);

    timer_ = this->create_wall_timer(period, std::bind(&BasePublisher::publish_msg, this));
  }

private:
  void publish_msg()
  {
    auto msg = sensor_msgs::msg::Imu();

    msg.header.frame_id = "imu_link";

    // 2. Orientierung (Quaternion) -> Hier flach/keine Rotation (w=1, x=0, y=0, z=0)
    msg.orientation.w = 1.0;
    msg.orientation.x = 0.0;
    msg.orientation.y = 0.0;
    msg.orientation.z = 0.0;

    // Optional: Kovarianz für Orientierung (-1 bedeutet "unbekannt")
    msg.orientation_covariance[0] = 0.01; // Leichtes Rauschen auf X-Achse

    // 3. Winkelgeschwindigkeit (in rad/s) -> z.B. leichte Drehung um die Z-Achse
    msg.angular_velocity.x = 0.0;
    msg.angular_velocity.y = 0.0;
    msg.angular_velocity.z = 0.1; // 0.1 rad (~5.7 Grad) pro Sekunde

    // 4. Linearbeschleunigung (in m/s²) 
    // Wenn der Sensor still liegt, misst er die Erdbeschleunigung (ca. 9.81) nach oben
    msg.linear_acceleration.x = 0.0;
    msg.linear_acceleration.y = 0.0;
    msg.linear_acceleration.z = 9.81;
    
    msg.header.stamp = this->now();
    publisher_->publish(msg);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BasePublisher>());
  rclcpp::shutdown();
  return 0;
}