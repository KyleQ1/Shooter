#!/usr/bin/env python3

# Avoid needing display if plots aren't being shown
import sys

if "--noninteractive" in sys.argv:
    import matplotlib as mpl

    mpl.use("svg")

import frccontrol as frccnt
import matplotlib.pyplot as plt
import numpy as np


class Elevator(frccnt.System):
    def __init__(self, m, dt):
        """Elevator subsystem.

        Keyword arguments:
        m -- mass of the elevator carriage in kg
        dt -- time between model/controller updates
        """
        self.m = m
        state_labels = [("Position", "m"), ("Velocity", "m/s")]
        u_labels = [("Voltage", "V")]
        self.set_plot_labels(state_labels, u_labels)

        frccnt.System.__init__(
            self, np.zeros((2, 1)), np.array([[-12.0]]), np.array([[12.0]]), dt
        )

    def create_model(self, states):
        # Number of motors
        num_motors = 2.0
        # Radius of pulley in meters
        r = 0.0181864
        # Gear ratio
        G = 40 / 40
        return frccnt.models.elevator(
            frccnt.models.MOTOR_775PRO, num_motors, self.m, r, G
        )

    def design_controller_observer(self):
        q = [0.02, 0.4]
        r = [12.0]
        self.design_lqr(q, r)
        self.design_two_state_feedforward(q, r)

        q_pos = 0.05
        q_vel = 1.0
        r_pos = 0.0001
        self.design_kalman_filter([q_pos, q_vel], [r_pos])


def main():
    dt = 0.00505
    m = 5.0  # 6.803886
    elevator = Elevator(m, dt)
    elevator.export_cpp_coeffs("Elevator", "control/")
    m = 5.4  # 51.4
    elevator = Elevator(m, dt)
    elevator.export_cpp_coeffs("ElevatorClimb", "control/")

    if "--save-plots" in sys.argv or "--noninteractive" not in sys.argv:
        try:
            import slycot

            plt.figure(1)
            elevator.plot_pzmaps()
        except ImportError:  # Slycot unavailable. Can't show pzmaps.
            pass
    if "--save-plots" in sys.argv:
        plt.savefig("elevator_pzmaps.svg")

    # Set up graphing
    l0 = 0.1
    l1 = l0 + 5.0
    l2 = l1 + 0.1
    t = np.arange(0, l2 + 5.0, dt)

    refs = []

    # Generate references for simulation
    for i in range(len(t)):
        if t[i] < l0:
            r = np.matrix([[0.0], [0.0]])
        elif t[i] < l1:
            r = np.matrix([[1.524], [0.0]])
        else:
            r = np.matrix([[0.0], [0.0]])
        refs.append(r)

    if "--save-plots" in sys.argv or "--noninteractive" not in sys.argv:
        plt.figure(2)
        state_rec, ref_rec, u_rec = elevator.generate_time_responses(t, refs)
        elevator.plot_time_responses(t, state_rec, ref_rec, u_rec)
    if "--save-plots" in sys.argv:
        plt.savefig("elevator_response.svg")
    if "--noninteractive" not in sys.argv:
        plt.show()


if __name__ == "__main__":
    main()
