function b=ZScan(a)
% 输入是一个8*8的矩阵，输出一个1*64的矩阵（行向量）
% 这是参照 University of California 提供的 MPEG 源代码的基础上编制的。
% Copyright (c) 1995 The Regents of the University of California.

[n,m]=size(a);
if(n~=8 && m~=8)
error('Input array is NOT 8-by-8');
end

% Set up array for fast conversion from row/column coordinates to
zigzag=[1 2 9 17 10 3 4 11
        18 25 33 26 19 12 5 6
        13 20 27 34 41 49 42 35 
        28 21 14 7 8 15 22 29
        36 43 50 57 58 51 44 37
        30 23 16 24 31 38 45 52
        59 60 53 46 39 32 40 47
        54 61 62 55 48 56 63 64];

aa = reshape(a',1,64); % 将输入块变成1x64的向量
zigzagR = reshape(zigzag',1,64);
b = aa(zigzagR); % 对 aa 按照查表方式取元素，得到 zig-zag 扫描结果
end
