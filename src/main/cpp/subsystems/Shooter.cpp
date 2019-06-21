// Copyright (c) 2019 FRC Team 3512. All Rights Reserved.

#include "Shooter.hpp"
#include "Robot.hpp"

using namespace frc3512;

Shooter::Shooter() : PublishNode("Shooter") {
    m_grbx.Set(0.0);
}

void Shooter::Enable() {
    m_thread.StartPeriodic(0.005);
}

void Shooter::Disable() {
    m_thread.Stop();
}

void Shooter::ProcessMessage(const ButtonPacket& message) {
    if (message.topic == "Robot/AppendageStick2" && message.button == 7 &&
        message.pressed) {

        }
}