# Notes

# Bidirectional Tracks

Add a route, then `center` its alignment and set it as `template route`. Then you can right-click and select `Edge Operations > Add Reverse Direction to Edge` to creare the reverse connected edge.
Always remember to hit F5 to re-render the scenario.

# Traffic Light Phases

All phases should either a Green XOR a Yellow Phase.
For example:
- rrrGGGrrrGGG
- rrryyyrrryyy
- GGGrrrGGGrrr
- yyyrrryyyrrr

This leads to a continous sequence of $1G -> 1y -> 2r$.

# Metriche

- step
- system_total_stopped
- system_total_waiting_time
- system_mean_waiting_time
- system_mean_speed
- J0_stopped
- J0_accumulated_waiting_time
- J0_average_speed
- J13_stopped
- J13_accumulated_waiting_time
- J13_average_speed
- J15_stopped
- J15_accumulated_waiting_time
- J15_average_speed
- J16_stopped
- J16_accumulated_waiting_time
- J16_average_speed
- J2_stopped
- J2_accumulated_waiting_time
- J2_average_speed
- J3_stopped
- J3_accumulated_waiting_time
- J3_average_speed
- J4_stopped
- J4_accumulated_waiting_time
- J4_average_speed
- J7_stopped
- J7_accumulated_waiting_time
- J7_average_speed
- agents_total_stopped
- agents_total_accumulated_waiting_time
