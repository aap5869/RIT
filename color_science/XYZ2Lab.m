function Lab = XYZ2Lab(XYZ, XYZn)
%XYZ2Lab Calculates L* a* b* values given XYZ values
%   Lab = XYZ2Lab(XYZ, XYZn) Calculates L* a* b* values given the XYZ
%   values of some object and the XYZ values of the light source. Returns
%   Lab which is a 3 x N array.
%
%   XYZ: 3 x N array of XYZ values of the object
%   XYZn: 3 x 1 array of the XYZ values of the light source


    function fx = check(x)
        index = find(x > 0.008856);
        fx(index) = x(index).^(1/3);
        index = find(x <= 0.008856);
        fx(index) = 7.787 .* x(index) + 16/116;
    end

L = 116.*check(XYZ(2,:) ./ XYZn(2)) - 16;
a = 500 .* (check(XYZ(1,:) ./ XYZn(1)) - check(XYZ(2,:) ./ XYZn(2)));
b = 200.*(check(XYZ(2,:) ./ XYZn(2)) - check(XYZ(3,:) ./ XYZn(3)));

Lab = [L;a;b];

end