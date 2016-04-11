function XYZ = ref2XYZ(refs, cmfs, illum)
% REF2XYZ Calculates XYZ tristimulus values
%   XYZ = ref2XYZ(REFS, CMFS, ILLUM) Calculates XYZ tristimulus values from
%   the reflectance values REFS, the color matching functions of a CIE
%   standard observer CMFS, and the illuminant data ILLUM. Returns XYZ a
%   3xn matrix of tristimulus values.
% 
%   REFS: An N x M matrix
%   CMFS: An N x 3 matrix       
%   ILLUM: An N x 1 array
%

k = 100 ./ (cmfs(:,2)' * illum);

XYZ = k .* cmfs' * diag(illum) * refs;


end

