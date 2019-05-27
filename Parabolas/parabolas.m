global altura_red distancia_x_omni altura_omni
altura_red = 2.43;
distancia_x_omni = -9;
altura_omni = 1;

distancia_persona = 4.5;
altura_persona = 1.9;
altura_sobre_red = 5;
parabola = calcular_parabola(distancia_persona, altura_persona, altura_sobre_red);

x=distancia_x_omni:0.1:distancia_persona;
y = parabola(1)*x.^2 + parabola(2)*x + parabola(3);
angulo_rad = 2*parabola(1)*distancia_x_omni + parabola(2);
angulo = angulo_rad * 180/pi

gravedad = -9.81;
v_0 = sqrt((0.5*gravedad*(distancia_persona-distancia_x_omni)^2)/...
    (cos(angulo_rad)^2*((altura_persona-altura_omni)-...
    tan(angulo_rad)*(distancia_persona-distancia_x_omni))))

figure(1)
hold on
xlim([-10,10])
ylim([-0.1,8])
bar([distancia_persona],[altura_persona],'r')
bar([0],[altura_red],'k')
bar([distancia_x_omni],[altura_omni],'g')
comet(x,y)


function parabola = calcular_parabola(distancia_persona, altura_persona, altura_sobre_red)
global altura_red distancia_x_omni altura_omni
punto_1 = [distancia_x_omni, altura_omni];
punto_2 = [0, altura_red+altura_sobre_red];
punto_3 = [distancia_persona, altura_persona];
puntos_x = [punto_1(1), punto_2(1), punto_3(1)];
puntos_y = [punto_1(2), punto_2(2), punto_3(2)];
p = polyfit(puntos_x, puntos_y, 2);
parabola = p;
end