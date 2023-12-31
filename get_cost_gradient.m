function G_im = get_cost_gradient(im)
    
    [row,col,n] = size(im);
    if(n == 3)
        im = rgb2gray(im);
    end
    im = double(im)/255;

    [grad_x,grad_y] = gradient(im);
    G_im = grad_x + grad_y;
    G_im = abs(G_im);
end
