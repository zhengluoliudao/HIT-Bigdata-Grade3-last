%程序功能：模拟DCT编码解码过程，生成带“块效应”的图像
%实验图片：lena.jpg(512*512)
%步骤：灰度图像→DCT→量化→反量化→IDCT
%下一步目标：实现对任意大小图象的处理。（判断图象大小，若不是2的整数次方，则补零）
close all;clear;clc;
I1=imread('1.bmp');%读取图像
figure(1);imshow(I1);title('原始图像');
%I1=rgb2gray(I);figure(1);imshow(I1);title('原始图像');%变成灰度图像，并显示
I=im2double(I1);%变换前的原始数据（分别跟I3,B做比较，看有何差别）---I3跟I跟接近，B仿佛放大了
%imwrite(I,'原始图像2.JPG');
%I2=zeros(64);I3=I2;%申请2个64×64的矩阵，I2存放DCT后的数据，I3存放IDCT后的数据
C= dctmtx(8);%生成标准DCT变化中的矩阵（8×8）。
          ...DCT变换公式: 正变换:Y=CPC';逆变换:P=C'YC;
%光亮度量化表
a1=[16 11 10 16 24  40  51  61;
    12 12 14 19 26  58  60  55;
    14 13 16 24 40  57  69  56;
    14 17 22 29 51  87  80  62;
    18 22 37 56 68  109 103 77;
    24 35 55 64 81  104 113 92;
    49 64 78 87 103 121 120 101;
    72 92 95 98 112 100 103 99 ];

%分块做DCT变换（8×8）
for i=1:8:505
    for j=1:8:505
        P=I(i:i+7,j:j+7);
        K=C*P*C';
        I2(i:i+7,j:j+7)=K;
        K=K./a1;%量化
        K(abs(K)<0.03)=0;
        I3(i:i+7,j:j+7)=K;
    end
end
figure;imshow(I2);title('DCT变换后的频域图像');%显示DCT变换后的频域图像

%分块做DCT反变换（8×8）
for i=1:8:505
    for j=1:8:505
        P=I3(i:i+7,j:j+7).*a1;%反量化
        K=C'*P*C;
        I4(i:i+7,j:j+7)=K;
    end
end
%I4=uint8(I4);
figure;imshow(I4);title('复原图像');
imwrite(I4,'复原图像6.jpg');
%sigma(I4);figure;imshow(I4);