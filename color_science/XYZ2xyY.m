function xyY = XYZ2xyY(XYZ)
%XYZ2xyY Calculates x and y chromaticity coordinates
%   xyY = XYZ2xyY(XYZ) Calculates x and y chromaticity coordiantes using
%   the provided XYZ tristimulus values. Returns xyY as a 3 x M matrix.
%
%   XYZ: A 3 x M matrix

x = XYZ(1,:) ./ (XYZ(1,:) + XYZ(2,:) + XYZ(3,:));

y = XYZ(2,:) ./ (XYZ(1,:) + XYZ(2,:) + XYZ(3,:));

xyY = [x; y; XYZ(2,:)];

end

