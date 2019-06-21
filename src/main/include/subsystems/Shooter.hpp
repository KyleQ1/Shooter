// Copyright (c) 2019 FRC Team 3512. All Rights Reserved.

#pragma once

#include "frc/Notifier.h"

#include "Constants.hpp"
#include "communications/PublishNode.hpp"
#include "subsystems/SubsystemBase.hpp"

namespace frc3512 {

class Shooter : public SubsystemBase, public PublishNode {
public: 
    Shooter();

    void Shoot();

    void Enable();
    void Disable();

    void Iterate();

    void ProcessMessage(const ButtonPacket& message) override;

    void ProcessMessage(const CommandPacket& message) override;

private:
    frc::Notifier m_thread{&Shooter::Iterate, this};

    frc::Spark m_grbx{kShooterPort};
};

} // namespace frc3512