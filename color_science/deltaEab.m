function DEab = deltaEab(Lab1, Lab2)
%DEab = deltaEab(Lab1, Lab2) Calculates the Delta E between two sets of
%CIELab values
%
%   Calculates the Delta E between two sets of CIELab values. Returns DEab
%   as a 1 x N array
%
%   Lab1: 3 x N matrix
%   Lab2: 3 x N matrix
%
%

DEab = sqrt((Lab2(1,:) - Lab1(1,:)).^2 +...
            (Lab2(2,:) - Lab1(2,:)).^2 +...
            (Lab2(3,:) - Lab1(3,:)).^2);

end

