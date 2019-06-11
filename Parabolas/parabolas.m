global altura_red distancia_x_omni altura_omni
altura_red = 2.43;
distancia_x_omni = -9;
altura_omni = 1;

<<<<<<< HEAD
distancia_persona = 4.5;
altura_persona = 2.2;
altura_sobre_red = 2.5;
=======
distancia_persona = 3.5;
altura_persona = 0.5;
altura_sobre_red = 0.5;
>>>>>>> e177a3c3f2639a95c4e83eb9cd6b00ca4e6142a0
parabola = calcular_parabola(distancia_persona, altura_persona, altura_sobre_red);

x=distancia_x_omni:0.1:distancia_persona;
y = parabola(1)*x.^2 + parabola(2)*x + parabola(3);
%Variaciones de posicion
deltaY = y(2)-y(1);
deltaX = x(2)-x(1);
%Pendiente.
m = deltaY/deltaX;
%Angulo
angulo_rad = atan(m);
angulo = angulo_rad * 180/pi;

gravedad = -9.81;
v_0 = sqrt((0.5*gravedad*(distancia_persona-distancia_x_omni)^2)/...
    (cos(angulo_rad)^2*((altura_persona-altura_omni)-...
    tan(angulo_rad)*(distancia_persona-distancia_x_omni))));

velocidad = strcat('Velocidad necesaria (m/s):',string(v_0));
ang = strcat('Angulo necesario (°):',string(angulo));
disp(velocidad)
disp(ang)

figure()
hold on
xlim([-10,10])
<<<<<<< HEAD
ylim([-0.1,8])
bar([distancia_persona],[altura_persona],'r')
bar([0],[altura_red],'k')
bar([distancia_x_omni],[altura_omni],'g')
title("Velocidad: "+string(v_0)+" [m/s], ángulo: "+string(angulo)+"°")
=======
ylim([0,max(y)+0.3])
bar([distancia_persona],[altura_persona],'r','BarWidth', 0.3)
bar([0],[altura_red],'k','BarWidth', 0.2)
bar([distancia_x_omni],[altura_omni],'g','BarWidth', 0.3)
%Identificadores
txt1 = '\leftarrow Omniwrist'; text(distancia_x_omni,altura_omni,txt1)
txt2 = '\leftarrow Malla'; text(0,altura_red,txt2)
txt3 = char(strcat("\leftarrow Recepción.Distancia:",string(distancia_persona), 'm')); text(distancia_persona,altura_persona,txt3)
%Texto de velocidad y angulo
text(max(x),max(y),char(velocidad))
text(max(x),max(y)-0.14,char(ang))
>>>>>>> e177a3c3f2639a95c4e83eb9cd6b00ca4e6142a0
comet(x,y)
hold off



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