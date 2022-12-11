% Projector-Camera Stereo calibration parameters:

% Intrinsic parameters of camera:
fc_left = [ 2411.595943 2411.604372 ]; % Focal Length
cc_left = [ 1219.308220 1017.828987 ]; % Principal point
alpha_c_left = [ 0.000000 ]; % Skew
kc_left = [ -0.125668 0.292667 -0.000462 -0.000214 0.000000 ]; % Distortion

% Intrinsic parameters of projector:
fc_right = [ 1715.269455 1720.496823 ]; % Focal Length
cc_right = [ 528.312869 386.554817 ]; % Principal point
alpha_c_right = [ 0.000000 ]; % Skew
kc_right = [ -0.115922 0.659060 -0.001445 0.001011 0.000000 ]; % Distortion

% Extrinsic parameters (position of projector wrt camera):
om = [ 0.003185 -0.267918 -0.001385 ]; % Rotation vector
T = [ 134.992996 27.493326 243.219560 ]; % Translation vector
