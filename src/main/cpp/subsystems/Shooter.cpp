// Copyright (c) 2019 FRC Team 3512. All Rights Reserved.

#include "subsystems/Shooter.hpp"

#include "Robot.hpp"

using namespace frc3512;

Shooter::Shooter() : PublishNode("Shooter") { m_grbx.Set(0.0); }

void Shooter::Enable() { m_thread.StartPeriodic(0.005); }

void Shooter::Disable() { m_thread.Stop(); }

void Shooter::Iterate() {}

void Shooter::Shoot() { m_grbx.Set(1.0); }

void Shooter::ProcessMessage(const ButtonPacket& message) {
    if (message.topic == "Robot/AppendageStick2" && message.button == 3 &&
        message.pressed) {
        CommandPacket message{"Climber/Down", true};
        Publish(message);
    }
}

void Shooter::ProcessMessage(const CommandPacket& message) {
    if (message.topic == "Shooter/Shoot") {
        Shoot();
    }
}
